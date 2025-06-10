import base64
import io
import json
import os
import uuid
from http.client import HTTPException

import gradio as gr
from PIL import Image
from dotenv import load_dotenv, find_dotenv
from mistralai import Mistral
from openai import OpenAI
from tavily import TavilyClient
import chromadb
from chromadb.utils import embedding_functions

# ========== VectorDB Initialization ==========
chroma_client = chromadb.Client()
embedding_function = embedding_functions.DefaultEmbeddingFunction()

try:
    feedback_collection = chroma_client.get_collection("user_feedback", embedding_function=embedding_function)
except:
    feedback_collection = chroma_client.create_collection("user_feedback", embedding_function=embedding_function)


# ========== Utility Functions ==========
def encode_image(pil_image):
    try:
        buffered = io.BytesIO()
        pil_image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None


def generate_image(description):
    prompt = ("Generate 3 realistic images (with the full body) of a person dressed in each style described below, "
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

    response = tavily_client.search(
        query=f"Search online products from online marketplaces from this information: {query}")

    if len(response['results']) >= 3:
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

def save_feedback_to_vector_db(user_id, feedback_text, style_output, analysis):
    """Save user feedback to vector database with unique ID"""
    try:
        feedback_collection.add(
            documents=[feedback_text],
            metadatas=[{
                "user_id": user_id,
                "style_output": style_output,
                "analysis": analysis,
                "timestamp": str(gr.State())
            }],
            ids=[user_id]
        )
        return True
    except Exception as e:
        print(f"Error saving feedback: {e}")
        return False


def retrieve_user_feedback(user_id):
    """Retrieve user's previous feedback from vector database"""
    try:
        results = feedback_collection.get(
            ids=[user_id],
            include=["documents", "metadatas"]
        )
        if results['documents']:
            return {
                'feedback': results['documents'][0],
                'metadata': results['metadatas'][0]
            }
        return None
    except Exception as e:
        print(f"Error retrieving feedback: {e}")
        return None

def analyze_feedback(feedback_text, style_output):
    if not feedback_text.strip():
        return "No feedback provided.", style_output

    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    model = "mistral-large-latest"

    messages = [{
        "role": "user",
        "content": (
            "You're an AI system that analyzes user feedback to improve style recommendations. "
            "Given the original style recommendation and user feedback, provide the following:\n"
            "1. Reward score: +1 (liked), -1 (disliked)\n"
            "2. Why was it liked or disliked?\n"
            "3. Improved version of the recommendation (max 800 characters) (if applicable).\n\n"
            f"Original Recommendation:\n{style_output}\n\nUser Feedback:\n{feedback_text}"
        )
    }]

    chat_response = client.chat.complete(model=model, messages=messages)
    analysis = chat_response.choices[0].message.content

    return analysis, style_output

# ========== Processing ==========
def analyze_person(image, user_id=None):
    # Generate unique user ID if not provided
    if not user_id:
        user_id = str(uuid.uuid4())

    encoded = encode_image(image)
    if not encoded:
        return "Error encoding image", None, "", "", "", user_id

    # Check if user has previous feedback in database
    previous_feedback = retrieve_user_feedback(user_id)

    base_prompt = ("You are an AI agent tasked with analyzing the characteristics of the person in the photo. "
                   "Analyze physical features such as facial structure, hairstyle, hair color, and skin tone. "
                   "Recommend the top 3 styles of dressing that best suit based on analysis.")

    # Incorporate previous feedback if it exists
    if previous_feedback:
        feedback_prompt = (f"\n\nIMPORTANT: This user has provided previous feedback. "
                           f"User's feedback: '{previous_feedback['feedback']}' "
                           f"Previous analysis: '{previous_feedback['metadata']['analysis']}' "
                           f"Keep this feedback in mind and avoid repeating the same mistakes. "
                           f"Incorporate these insights to provide better, more personalized recommendations.")
        base_prompt += feedback_prompt

    base_prompt += "\nGenerate only 1,800 maximum characters."

    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": base_prompt},
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

        product_url1, product_url2, product_url3, product_title1, product_title2, product_title3 = search_recommended_products(
            message)

        if product_url1:
            return message, generated_image, create_product_button(product_title1, product_url1), create_product_button(
                product_title2, product_url2), create_product_button(product_title3, product_url3), user_id
        else:
            return message, generated_image, "No product found", "No product found", "No product found", user_id

    except HTTPException as e:
        return "Error analyzing person : {}".format(e), None, "", "", "", user_id


# ========== Feedback Processing ==========
def handle_yes_feedback():
    return {
        feedback_type_state: gr.update(value="like"),
        feedback_output: gr.update(visible=False),
        feedback_text: gr.update(label="Tell me what you like", visible=True),
        submit_feedback_btn: gr.update(visible=True),
        generate_again_btn: gr.update(visible=False)
    }


def handle_no_feedback():
    return {
        feedback_type_state: gr.update(value="dislike"),
        feedback_output: gr.update(visible=False),
        feedback_text: gr.update(label="Tell us what went wrong", visible=True),
        submit_feedback_btn: gr.update(visible=True),
        generate_again_btn: gr.update(visible=False)
    }


def handle_submit_feedback(feedback_text_value, style_output_value, user_id, feedback_type):
    analysis, _ = analyze_feedback(feedback_text_value, style_output_value)

    # Save feedback to vector database
    success = save_feedback_to_vector_db(user_id, feedback_text_value, style_output_value, analysis)

    is_generate = feedback_type == "dislike"

    if success:
        return {
            feedback_output: gr.update(
                value=f"Thank you for your feedback!\n\nFeedback saved successfully!\n\n{analysis}",
                visible=True),
            feedback_text: gr.update(visible=False),
            submit_feedback_btn: gr.update(visible=False),
            generate_again_btn: gr.update(visible=is_generate)
        }
    else:
        return {
            feedback_output: gr.update(value=f"Error saving feedback, but here's the analysis:\n\n{analysis}",
                                       visible=True),
            feedback_text: gr.update(visible=False),
            submit_feedback_btn: gr.update(visible=False),
            generate_again_btn: gr.update(visible=False)
        }


def handle_generate_again(image, user_id):
    if image is None:
        return "Please upload an image first.", None, "", "", "", {
            feedback_output: gr.update(visible=False),
            generate_again_btn: gr.update(visible=False)
        }

    style, img, prod1, prod2, prod3, _ = analyze_person(image, user_id)

    return style, img, prod1, prod2, prod3, {
        feedback_output: gr.update(visible=False),
        generate_again_btn: gr.update(visible=False)
    }


if __name__ == "__main__":
    load_dotenv(find_dotenv())

    with gr.Blocks() as demo:
        gr.Markdown("## 👗 DressMe.AI — Personalized Fashion Style Recommendations")

        # Hidden state to store user ID
        user_id_state = gr.State()

        # Feedback type state (like or dislike)
        feedback_type_state = gr.State()
        print(feedback_type_state)

        with gr.Row():
            with gr.Column():
                image_input = gr.Image(type="pil", label="Upload your photo")
                with gr.Row():
                    analyze_btn = gr.Button("Submit", variant="primary")
                    clear_btn = gr.Button("Clear", variant="secondary")
                gr.Examples(
                    examples=["./images/person1.jpg", "./images/person2.jpg"],
                    inputs=image_input,
                    label="Try Examples"
                )
                gr.Markdown("##  🛍️ Product Recommendations")
                product1_output = gr.HTML()
                product2_output = gr.HTML()
                product3_output = gr.HTML()
            with gr.Column():
                style_output = gr.Textbox(label="Style Description", lines=6)
                image_output = gr.Image(label="Recommended Style Image")

        analyze_btn.click(
            fn=analyze_person,
            inputs=[image_input, user_id_state],
            outputs=[style_output, image_output, product1_output, product2_output, product3_output, user_id_state]
        )

        clear_btn.click(
            fn=lambda: (None, "", None, "", "", "", str(uuid.uuid4())),
            inputs=None,
            outputs=[image_input, style_output, image_output, product1_output, product2_output, product3_output,
                     user_id_state]
        )

        # Feedback area
        with gr.Row():
            gr.Markdown("### 🤔 Did you like the recommendations?")
            yes_btn = gr.Button("👍 Yes")
            no_btn = gr.Button("👎 No")

        feedback_text = gr.Textbox(visible=False, lines=2)
        submit_feedback_btn = gr.Button("Submit Feedback", visible=False)
        feedback_output = gr.Textbox(label="Feedback Analysis", visible=False, lines=6)

        generate_again_btn = gr.Button("🔄 Generate Again with Your Feedback", visible=False, variant="primary")

        yes_btn.click(
            fn=handle_yes_feedback,
            inputs=None,
            outputs=[feedback_output, feedback_text, submit_feedback_btn, generate_again_btn, feedback_type_state]
        )

        no_btn.click(
            fn=handle_no_feedback,
            inputs=None,
            outputs=[feedback_output, feedback_text, submit_feedback_btn, generate_again_btn, feedback_type_state]
        )

        submit_feedback_btn.click(
            fn=handle_submit_feedback,
            inputs=[feedback_text, style_output, user_id_state, feedback_type_state],
            outputs=[feedback_output, feedback_text, submit_feedback_btn, generate_again_btn]
        )

        generate_again_btn.click(
            fn=handle_generate_again,
            inputs=[image_input, user_id_state],
            outputs=[style_output, image_output, product1_output, product2_output, product3_output, feedback_output,
                     generate_again_btn]
        )

    demo.launch(show_error=True)