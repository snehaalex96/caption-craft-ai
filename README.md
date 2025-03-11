# Instagram Caption Generator

A multimodal AI application that analyzes images and generates contextually relevant Instagram captions with hashtag recommendations.

## Features

- **Image Analysis**: Uses CLIP to identify objects, scenes, and mood in uploaded images
- **Caption Generation**: Creates engaging captions in various styles (casual, professional, funny, etc.)
- **Hashtag Recommendations**: Suggests relevant hashtags based on image content
- **Multiple Style Options**: Choose from different caption styles to match your content
- **Copy Functionality**: Easily copy captions and hashtags to paste into Instagram

## Tech Stack

### Backend
- **FastAPI**: Modern, high-performance web framework for building APIs
- **CLIP**: OpenAI's Contrastive Language-Image Pre-Training model for image understanding
- **Transformers**: Hugging Face's transformers library for caption generation
- **PyTorch**: Deep learning framework for AI models

### Frontend
- **React**: JavaScript library for building user interfaces
- **CSS3**: Modern CSS with flexbox and grid for responsive design

## Project Structure

```
instagram-caption-generator/
├── backend/
│   ├── app.py                   # FastAPI main application
│   ├── requirements.txt         # Python dependencies
│   ├── models/
│   │   ├── image_analyzer.py    # Image analysis with CLIP
│   │   └── caption_generator.py # Caption generation with LLM
│   └── utils/
│       └── hashtag_utils.py     # Hashtag recommendation functions
└── frontend/
    ├── package.json             # Node dependencies
    ├── public/
    └── src/
        ├── App.js               # Main React component
        ├── components/          # React components
        └── styles/              # CSS styles
```

## Installation & Setup

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Start the backend server:
```bash
python app.py
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open your browser to `http://localhost:3000`

## Usage

1. Select a caption style from the available options
2. Upload an image by dragging and dropping or using the file browser
3. Wait for the AI to analyze your image
4. View the generated captions and hashtags
5. Copy the caption and hashtags you like best
6. Post to Instagram!

## Future Enhancements

- Video analysis capabilities
- User accounts for saving favorite captions
- Direct posting to Instagram via API
- Brand voice customization
- Caption performance analytics
- Fine-tuning models on Instagram data

## License

MIT

## Acknowledgments

- OpenAI for the CLIP model
- Hugging Face for Transformers
- The FastAPI and React communities

---

Created by Sneha - A  project showcasing multimodal AI capabilities
