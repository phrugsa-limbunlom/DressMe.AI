import base64
import io
import json
import os
from http.client import HTTPException

import gradio as gr
from PIL import Image
from dotenv import load_dotenv, find_dotenv
from mistralai import Mistral
from openai import OpenAI
from tavily import TavilyClient


def encode_image(pil_image):
    try:
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None


def generate_image(description):
    prompt = ("Generate 3 realistic images of a person dressed in each style described below, "
              "accurately reflecting the clothing, colors, and accessories mentioned. "
              "**Do not include any text in those images.**\n\n") + description

    client = OpenAI(
        base_url="https://api.studio.nebius.com/v1/",
        api_key=os.environ.get("NEBIUS_API_KEY")
    )

    try:
        response = client.images.generate(
            model="black-forest-labs/flux-schnell",
            response_format="b64_json",
            extra_body={
                "response_extension": "png",
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 4,
                "negative_prompt": "",
                "seed": -1
            },
            prompt=prompt
        )
        return response.to_json()
    except HTTPException as e:
        return "Error generating image: {}".format(e)


def search_recommended_products(info):
    tavily_client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    model = "mistral-large-latest"

    messages = [{
        "role": "user",
        "content": ("Review the following style analysis and transform each style recommendation into a concise, "
                    "searchable query in 50 characters that could be used to find relevant fashion products online. "
                    "Do not include any explanation. Style information: {}".format(info))
    }]

    chat_response = client.chat.complete(model=model, messages=messages)
    query = chat_response.choices[0].message.content

    response = tavily_client.search(query=f"Search online products from online marketplaces from this information: {query}")

    if len(response['results']) != 0:

        title1 = response['results'][0]['title']
        title2 = response['results'][1]['title']
        title3 = response['results'][2]['title']

        link1 = response['results'][0]['url']
        link2 = response['results'][1]['url']
        link3 = response['results'][2]['url']

        return link1, link2, link3, title1, title2, title3

    return None, None, None, None, None, None

def create_product_button(label, link):
    return f"""
    <a href="{link}" target="_blank" style="text-decoration: none;">
        <button style="
            background-color: #ff6600;
            color: white;
            padding: 12px 24px;
            font-size: 16px;
            font-style: italic;
            font-family: inherit;
            border: none;
            border-radius: 6px;
            width: 100%;
            text-align: center;
            margin-top: 10px;
            cursor: pointer;
            transition: background-color 0.3s ease;">
            {label}
        </button>
    </a>
    """

def analyze_person(image):
    encoded = encode_image(image)
    if not encoded:
        return "Error encoding image", None, "", "", ""

    messages = [{
        "role": "user",
        "content": [
            {"type": "text",
             "text": "You are an AI agent tasked with analyzing the characteristics of the person in the photo. "
                     "Recommend the top 3 styles of dressing that best suit"},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encoded}"}
        ]
    }]

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    model = "pixtral-12b-2409"

    try:
        chat_response = client.chat.complete(model=model, messages=messages)
        message = chat_response.choices[0].message.content

        response = generate_image(message)
        data = json.loads(response)
        b64_string = data["data"][0]["b64_json"]
        image_bytes = base64.b64decode(b64_string)
        generated_image = Image.open(io.BytesIO(image_bytes))

        product_url1, product_url2, product_url3, product_title1, product_title2, product_title3 = search_recommended_products(message)

        if product_url1 is not None and product_url2 is not None and product_url3 is not None and product_title1 is not None and product_title2 is not None and product_title3 is not None:

            product1_html = create_product_button(product_title1, product_url1)
            product2_html = create_product_button(product_title2, product_url2)
            product3_html = create_product_button(product_title3, product_url3)

            return message, generated_image, product1_html, product2_html, product3_html
        else:
            return message, generated_image, "No product found", "No product found", "No product found"

    except HTTPException as e:
        return "Error analyzing person : {}".format(e), None, "", "", ""


if __name__ == "__main__":
    load_dotenv(find_dotenv())

    with gr.Blocks() as demo:
        gr.Markdown("## 👗 DressMe.AI — Personalized Fashion Style Recommendations")

        with gr.Row():
            with gr.Column():
                image_input = gr.Image(type="pil", label="Upload your photo")
                with gr.Row():
                    analyze_btn = gr.Button("Submit", variant="primary")
                    clear_btn = gr.Button("Clear", variant="secondary")
                gr.Examples(
                    examples=["person1.jpg", "person2.jpg"],
                    inputs=image_input,
                    label="Try Examples"
                )
                gr.Markdown("##  🛍️ Product Recommendations")
                product1_output = gr.HTML()
                product2_output = gr.HTML()
                product3_output = gr.HTML()
            with gr.Column():
                style_output = gr.Textbox(label="Style Description")
                image_output = gr.Image(label="Recommended Style Image")

        analyze_btn.click(
            fn=analyze_person,
            inputs=image_input,
            outputs=[style_output, image_output, product1_output, product2_output, product3_output]
        )

        clear_btn.click(fn=lambda: None, inputs=None, outputs=image_input)

    demo.launch(show_error=True)
