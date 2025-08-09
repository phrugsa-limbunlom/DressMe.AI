<h1 align="center"> 👗 DressMe.AI </h1>

<img src="https://github.com/user-attachments/assets/f8444131-0a00-43e4-b499-31b734d4cff5" align="center">

<div align="center">
  <br>
  <b><i>DressMe.AI</i></b> is an AI-powered fashion assistant that provides <i> personalized style recommendations </i> based on a user's uploaded photo. It analyzes physical features and suggests styles that complement individual characteristics, generating realistic visuals and matching product links for online shopping. This application incorporates a <i> feedback mechanism </i> with vector database storage to continuously improve recommendations based on user preferences.
  <br>
  <br>
    🎬 <a href="https://www.youtube.com/watch?v=6ten78F3TmQ"> Watch DressMe.AI Demo </a> 💫 <a href="https://huggingface.co/spaces/Agents-MCP-Hackathon/DressMe.AI">Try DressMe.AI Demo </a> 
</div>

## 🚀 Purpose

To help users discover clothing styles tailored to their appearance using computer vision and language models — making fashion more personal, engaging, and AI-enhanced through continuous learning from user feedback.

## ✨ Key Features

- **📸 Image Analysis**: Upload a photo or use camera to get AI-generated fashion style descriptions
- **🎨 Visual Preview**: Receive high-resolution visual previews of recommended outfits using advanced image generation
- **🛍️ Smart Shopping**: Automatically fetch matching product links from online marketplaces
- **💬 Intelligent Feedback System**: Provide detailed feedback (likes/dislikes) with personalized analysis
- **🔄 Adaptive Learning**: "Generate Again" feature uses your feedback to refine future recommendations
- **📊 Persistent Memory**: ChromaDB vector database stores user preferences for improved personalization
- **🆔 User Sessions**: Unique user ID system tracks individual preferences across sessions

## 🧠 Models and APIs Used

| Task | Model / API | Purpose |
|:-----|:------------|:--------|
| **Vision Analysis & Style Recommendations** | `pixtral-12b-2409` (Mistral AI) | Analyzes physical features and generates personalized style recommendations |
| **Image Generation** | `black-forest-labs/flux-schnell` (Nebius API) | Creates realistic outfit visualizations based on style descriptions |
| **Query Processing** | `mistral-large-latest` (Mistral AI) | Processes style descriptions into searchable product queries |
| **Feedback Analysis** | `mistral-large-latest` (Mistral AI) | Analyzes user feedback and generates improvement insights |
| **Product Search** | [Tavily API](https://www.tavily.com/) | Searches online marketplaces for matching fashion products |
| **User Memory** | [ChromaDB](https://www.trychroma.com/) | Vector database for storing and retrieving user feedback and preferences |

## 🛠️ Core Functionality

### Main Processing Functions

- **`analyze_person(image, user_id)`**
  - Encodes uploaded image to base64
  - Retrieves user's previous feedback from vector database
  - Generates personalized style analysis using Mistral's vision model
  - Creates outfit visualization using Nebius image generation
  - Searches for matching products online
  - Returns style description, generated image, and product links

- **`generate_image(description)`**
  - Uses Nebius API with FLUX model for high-quality image generation
  - Generates realistic full-body outfit visualizations
  - Configured for 1024x1024 resolution with optimized inference steps

- **`search_recommended_products(info)`**
  - Converts style descriptions into targeted search queries using Mistral
  - Searches online marketplaces via Tavily API
  - Returns top 3 product matches with titles and links

### Feedback System Functions

- **`save_feedback_to_vector_db(user_id, feedback_text, style_output, analysis)`**
  - Stores user feedback in ChromaDB with metadata
  - Associates feedback with specific style recommendations
  - Enables persistent learning across user sessions

- **`retrieve_user_feedback(user_id)`**
  - Retrieves user's historical feedback from vector database
  - Provides context for personalized future recommendations

- **`analyze_feedback(feedback_text, style_output)`**
  - Processes user feedback using Mistral's language model
  - Generates reward scores (+1 for likes, -1 for dislikes)
  - Provides detailed analysis of user preferences
  - Suggests improvements for future recommendations

### User Interface Functions

- **`handle_yes_feedback()` / `handle_no_feedback()`**
  - Manages positive and negative feedback workflows
  - Updates UI components based on feedback type

- **`handle_submit_feedback()`**
  - Processes submitted feedback through AI analysis
  - Saves feedback to vector database
  - Updates UI with analysis results

- **`handle_generate_again()`**
  - Regenerates recommendations incorporating user feedback
  - Uses stored preferences for improved personalization

## 🔧 Technical Architecture

### Dependencies

```bash
gradio>=5.33.1
Pillow
openai
mistralai
tavily-python
chromadb
python-dotenv
```

### Environment Variables Required

```bash
MISTRAL_API_KEY=your_mistral_api_key
NEBIUS_API_KEY=your_nebius_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### Database Schema

The ChromaDB collection stores:
- **Documents**: User feedback text
- **Metadata**: User ID, original style output, feedback analysis, timestamp
- **Embeddings**: Automatic vector embeddings for similarity search

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DressMe.AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Add your API keys to .env file
   ```
4. **Run the application**
   ```bash
   python app.py
   ```

## 🎯 Usage Flow

1. **Upload Photo**: Users upload their photo or use camera
2. **AI Analysis**: System analyzes physical features and generates style recommendations
3. **Visual Preview**: AI creates realistic outfit visualizations
4. **Product Matching**: System finds matching products from online stores
5. **Feedback Collection**: Users provide feedback (👍/👎) with detailed comments
6. **Continuous Learning**: Feedback is analyzed and stored for future personalization
7. **Regeneration**: Users can generate new recommendations incorporating their feedback

## 🧪 Example Outputs

### Style Analysis
The system provides detailed analysis including:
- Physical feature assessment (facial structure, hair, skin tone)
- Top 3 recommended clothing styles
- Color palette suggestions
- Specific outfit recommendations

### Feedback Analysis
AI-generated feedback analysis includes:
- Reward scoring system (+1/-1)
- Preference identification
- Improvement suggestions
- Personalized recommendations

## 🔮 Future Enhancements

- **Multi-language Support**: Expand to support multiple languages
- **Advanced Filtering**: Add filters for occasion, season, budget
- **Social Features**: Enable sharing and community recommendations
- **Mobile App**: Develop dedicated mobile application
- **AR Integration**: Virtual try-on capabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/phrugsa-limbunlom/DressMe.AI/blob/main/LICENSE) file for details.

## 👨‍💻 Author

**Phrugsa Limbunlom**
- GitHub: [phrugsa-limbunlom](https://github.com/phrugsa-limbunlom)
- LinkedIn: [Phrugsa Limbunlom](https://www.linkedin.com/in/phrugsa-limbunlom-5b8995117/)

---

Made with 🧠 & ❤️ using Gradio, Mistral AI, Nebius, Tavily APIs, and ChromaDB.
