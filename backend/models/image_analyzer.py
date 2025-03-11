import torch
import clip
from PIL import Image
import numpy as np
from typing import List, Dict, Any

class ImageAnalyzer:
    def __init__(self):
        """Initialize the CLIP model for image analysis"""
        # Load the CLIP model
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess = clip.load("ViT-B/32", device=self.device)
        
        # Define categories for classification
        self.scene_categories = [
            "indoors", "outdoors", "beach", "mountains", "city", "forest", 
            "desert", "snow", "restaurant", "home", "office", "street"
        ]
        
        self.object_categories = [
            "person", "people", "group", "pet", "dog", "cat", "food", "drink",
            "building", "landmark", "vehicle", "sunset", "plants", "flowers",
            "technology", "book", "art", "fashion", "product", "sports equipment"
        ]
        
        self.activity_categories = [
            "eating", "drinking", "working", "exercising", "traveling", "reading",
            "gaming", "shopping", "celebrating", "relaxing", "playing", "hiking",
            "swimming", "dancing", "cooking", "meeting", "presenting", "performing"
        ]
        
        self.mood_categories = [
            "happy", "sad", "excited", "peaceful", "romantic", "energetic",
            "professional", "casual", "serious", "playful", "elegant", "rustic"
        ]
        
        # Tokenize all categories
        self.scene_tokens = clip.tokenize(["a photo of " + c for c in self.scene_categories]).to(self.device)
        self.object_tokens = clip.tokenize(["a photo of " + c for c in self.object_categories]).to(self.device)
        self.activity_tokens = clip.tokenize(["a photo of people " + c for c in self.activity_categories]).to(self.device)
        self.mood_tokens = clip.tokenize(["a photo with a " + c + " mood" for c in self.mood_categories]).to(self.device)

    def analyze(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze an image and return a description and other attributes
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary with image analysis results
        """
        # Preprocess the image
        image_input = self.preprocess(image).unsqueeze(0).to(self.device)
        
        # Get image features
        with torch.no_grad():
            image_features = self.model.encode_image(image_input)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            
            # Get scores for each category
            scene_scores = 100.0 * image_features @ self.model.encode_text(self.scene_tokens).T
            object_scores = 100.0 * image_features @ self.model.encode_text(self.object_tokens).T
            activity_scores = 100.0 * image_features @ self.model.encode_text(self.activity_tokens).T
            mood_scores = 100.0 * image_features @ self.model.encode_text(self.mood_tokens).T
            
        # Get top results
        top_scenes = self._get_top_results(scene_scores[0], self.scene_categories, 2)
        top_objects = self._get_top_results(object_scores[0], self.object_categories, 3)
        top_activities = self._get_top_results(activity_scores[0], self.activity_categories, 1)
        top_moods = self._get_top_results(mood_scores[0], self.mood_categories, 2)
        
        # Generate a structured description
        description = self._generate_description(top_scenes, top_objects, top_activities, top_moods)
        
        return {
            "description": description,
            "scenes": top_scenes,
            "objects": top_objects, 
            "activities": top_activities,
            "moods": top_moods
        }
        
    def _get_top_results(self, scores, categories, n=3):
        """Get top n results from scores"""
        values, indices = scores.topk(n)
        return [{"category": categories[idx], "score": values[i].item()} 
                for i, idx in enumerate(indices)]
        
    def _generate_description(self, scenes, objects, activities, moods):
        """Generate a textual description from the detected elements"""
        # Build description parts
        scene_desc = f"a {scenes[0]['category']} scene" if scenes else ""
        
        # Object description
        if objects:
            obj_list = [obj["category"] for obj in objects]
            if len(obj_list) == 1:
                obj_desc = f"showing {obj_list[0]}"
            else:
                obj_desc = f"showing {', '.join(obj_list[:-1])} and {obj_list[-1]}"
        else:
            obj_desc = ""
        
        # Activity description
        activity_desc = f"with {activities[0]['category']} activity" if activities else ""
        
        # Mood description
        mood_desc = f"in a {moods[0]['category']} mood" if moods else ""
        
        # Combine all parts, filtering out empty ones
        parts = [p for p in [scene_desc, obj_desc, activity_desc, mood_desc] if p]
        if parts:
            description = " ".join(parts)
            return description.capitalize()
        else:
            return "An image"