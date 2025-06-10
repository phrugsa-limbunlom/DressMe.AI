---
tag: agent-demo-track
title: DressMe.AI
emoji: 👗
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 5.33.1
app_file: app.py
pinned: false
license: mit
short_description: 👗 DressMe.AI — Personalized Fashion Style Recommendations
thumbnail: >-
  https://cdn-uploads.huggingface.co/production/uploads/66265a84af5c20bdffef0120/y6FywE76xt5_n4vWEf_7K.jpeg
---
# 👗 DressMe.AI

**DressMe.AI** is an AI-powered fashion assistant that provides **personalized style recommendations** based on a user's uploaded photo. It analyzes physical features and suggests styles that complement individual characteristics, generating realistic visuals and matching product links for online shopping. This application also incorporates a **feedback mechanism** to continuously improve its recommendations based on user preferences.

[Watch DressMe.AI Demo](https://www.youtube.com/watch?v=6ten78F3TmQ)

## 🚀 Purpose

To help users discover clothing styles tailored to their appearance using computer vision and language models — making fashion more personal, engaging, and AI-enhanced.

## ✨ Key Features

-   Upload a photo or take your photo with the camera and get an AI-generated fashion style description.
-   Receive a **visual preview** of the recommended outfit.
-   Automatically fetch **product links** that match the suggested style from online marketplaces.
-   **Provide feedback** on recommendations to help the AI learn and provide more personalized suggestions in the future.
-   **"Generate Again"** feature allows users to refine recommendations based on their feedback.

## 🧠 Models and APIs Used

| Task                              | Model / API                                                                      |
| :-------------------------------- |:---------------------------------------------------------------------------------|
| **Vision Capability for Style Analysis** | `pixtral-12b-2409` (via [Mistral](https://mistral.ai))                           |
| **Image Generation** | `black-forest-labs/flux-schnell` (via [Nebius API](https://nebius.com/)) (currently disabled) |
| **Query Analysis for Product Search** | `mistral-large-latest` (via Mistral)                                             |
| **Feedback Analysis** | `mistral-large-latest` (via Mistral) |
| **Marketplace Search** | [Tavily API](https://www.tavily.com/)                                            |
| **User Feedback Storage** | [ChromaDB](https://www.trychroma.com/)                                           |

## 🛠️ Functionality Overview

-   `analyze_person(image, user_id)`
    → Encodes the uploaded image, generates a fashion analysis and description (optionally considering previous feedback), and retrieves matching product URLs. The image generation is currently disabled.
-   `generate_image(description)`
    → Calls the Nebius API to produce a high-resolution image of the suggested fashion style.
-   `search_recommended_products(info)`
    → Uses Mistral to turn descriptions into product search queries and fetches results from online stores using Tavily.
-   `save_feedback_to_vector_db(user_id, feedback_text, style_output, analysis)`
    → Stores user feedback, the original style output, and the analysis of the feedback in ChromaDB.
-   `retrieve_user_feedback(user_id)`
    → Retrieves a user's past feedback from ChromaDB to inform future recommendations.
-   `analyze_feedback(feedback_text, style_output)`
    → Uses Mistral to analyze user feedback against the original recommendation, providing a reward score, reasons for liking/disliking, and an improved recommendation.

## 📦 Dependencies

- `gradio`
- `PIL`
- `openai`
- `mistralai`
- `tavily`
- `chromadb`
- `python-dotenv`

Install dependencies with:

```bash
pip install -r requirements.txt
``` 

Made with 🧠 & ❤️ using Gradio, Mistral, Nebius, and Tavily APIs.

GitHub: [phrugsa-limbunlom](https://github.com/phrugsa-limbunlom)

Linkedln: [Phrugsa Limbunlom](https://www.linkedin.com/in/phrugsa-limbunlom-5b8995117/)