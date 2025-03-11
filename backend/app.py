import os
import io
import base64
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
from typing import List, Optional

# Import project modules
from models.image_analyzer import ImageAnalyzer
from models.caption_generator import CaptionGenerator
from utils.hashtag_utils import generate_hashtags

# Initialize FastAPI app
app = FastAPI(title="Instagram Caption Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
image_analyzer = ImageAnalyzer()
caption_generator = CaptionGenerator()

@app.get("/")
def read_root():
    return {"message": "Instagram Caption Generator API"}

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    style: str = Form("casual"),
    num_captions: int = Form(3),
    num_hashtags: int = Form(5)
):
    # Read and process the image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    # Get image description
    image_description = image_analyzer.analyze(image)
    
    # Generate captions based on image analysis
    captions = caption_generator.generate(
        image_description=image_description,
        style=style,
        num_captions=num_captions
    )
    
    # Generate hashtags
    hashtags = generate_hashtags(image_description, count=num_hashtags)
    
    # Encode image to base64 for response
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return JSONResponse({
        "image": f"data:image/jpeg;base64,{img_str}",
        "description": image_description,
        "captions": captions,
        "hashtags": hashtags,
        "style": style
    })

@app.get("/styles")
def get_available_styles():
    """Return available caption styles"""
    return {
        "styles": [
            "casual",
            "professional",
            "funny",
            "inspirational",
            "minimalist",
            "poetic"
        ]
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)