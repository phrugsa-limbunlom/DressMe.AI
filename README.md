---
tag: agent-demo-track
title: DressMe.AI
emoji: 👗
colorFrom: purple
colorTo: pink
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: mit
short_description: 👗 DressMe.AI — Personalized Fashion Style Recommendations
thumbnail: >-
  https://cdn-uploads.huggingface.co/production/uploads/66265a84af5c20bdffef0120/y6FywE76xt5_n4vWEf_7K.jpeg
---

# 👗 DressMe.AI

**DressMe.AI** is an AI-powered fashion assistant that provides **personalized style recommendations** based on a user's uploaded photo. It analyzes physical features and suggests styles that complement individual characteristics, generating realistic visuals and matching product links for online shopping.

## 🚀 Purpose

To help users discover clothing styles tailored to their appearance using computer vision and language models — making fashion more personal, engaging, and AI-enhanced.

## ✨ Key Features

- Upload a photo or take your photo with the camera and get an AI-generated fashion style description.
- Receive a **visual preview** of the recommended outfit using image generation.
- Automatically fetch **product links** that match the suggested style from online marketplaces.

## 🧠 Models and APIs Used

| Task                                     | Model / API                                                              |
|------------------------------------------|--------------------------------------------------------------------------|
| **Vision Capability for Style Analysis** | `pixtral-12b-2409` (via [Mistral](https://mistral.ai))                   |
| **Image Generation**                     | `black-forest-labs/flux-schnell` (via [Nebius API](https://nebius.com/)) |
| **Query Analysis for Product Search**    | `mistral-large-latest` (via Mistral)                                     |
| **Marketplace Search**                   | [Tavily API](https://www.tavily.com/)                                    |

## 🛠️ Functionality Overview

- `analyze_person(image)`  
  → Encodes the uploaded image, generates a fashion analysis and description, synthesizes an outfit image, and retrieves matching product URLs.

- `generate_image(description)`  
  → Calls the Nebius API to produce a high-resolution image of the suggested fashion style.

- `search_recommended_products(info)`  
  → Uses Mistral to turn descriptions into product search queries and fetches results from online stores using Tavily.

## 📦 Dependencies

- `gradio`
- `PIL`
- `openai`
- `mistralai`
- `tavily`
- `python-dotenv`

Install dependencies with:

```bash
pip install -r requirements.txt
``` 

Made with ❤️ using Gradio, Mistral, Nebius, and Tavily APIs.

GitHub: https://github.com/phrugsa-limbunlom

Linkedln: https://www.linkedin.com/in/phrugsa-limbunlom-5b8995117/