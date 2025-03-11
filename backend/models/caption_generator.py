from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Dict, Any

class CaptionGenerator:
    def __init__(self):
        """Initialize the caption generation model"""
        # Load pretrained model and tokenizer
        # Using a smaller model for demonstration, but you can replace with larger models
        model_name = "facebook/opt-350m"  # You can use larger models like "facebook/opt-2.7b" for better results
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
        
        # Move model to GPU if available
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
        
        # Define style templates
        self.style_templates = {
            "casual": "Write a casual and friendly Instagram caption for {image_description}:",
            "professional": "Create a professional and polished Instagram caption for {image_description}:",
            "funny": "Generate a humorous and witty Instagram caption for {image_description}:",
            "inspirational": "Compose an inspirational and motivational Instagram caption for {image_description}:",
            "minimalist": "Create a short, minimal Instagram caption for {image_description}. Keep it under 5 words:",
            "poetic": "Write a poetic and artistic Instagram caption for {image_description}:"
        }
        
    def generate(self, image_description: str, style: str = "casual", num_captions: int = 3) -> List[str]:
        """
        Generate Instagram captions based on image description
        
        Args:
            image_description: Description of the image
            style: Style of caption to generate
            num_captions: Number of different captions to generate
            
        Returns:
            List of generated captions
        """
        # Get the appropriate prompt template for the style
        template = self.style_templates.get(style, self.style_templates["casual"])
        
        # Create the prompt
        prompt = template.format(image_description=image_description)
        
        captions = []
        for _ in range(num_captions):
            # Tokenize the prompt
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            
            # Generate text
            with torch.no_grad():
                output = self.model.generate(
                    **inputs,
                    max_new_tokens=50,
                    temperature=0.9,  # Higher temperature for more variety
                    top_p=0.92,
                    top_k=50,
                    no_repeat_ngram_size=2,
                    do_sample=True,
                    num_return_sequences=1
                )
            
            # Decode the output
            generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Extract just the caption (remove the prompt)
            caption = self._extract_caption(generated_text, prompt)
            
            # Clean up the caption
            caption = self._clean_caption(caption)
            
            captions.append(caption)
            
        return captions
    
    def _extract_caption(self, generated_text: str, prompt: str) -> str:
        """Extract the generated caption from the full text"""
        # Remove the prompt from the generated text
        if generated_text.startswith(prompt):
            caption = generated_text[len(prompt):].strip()
        else:
            # If for some reason the prompt is not at the beginning
            caption = generated_text.replace(prompt, "").strip()
            
        return caption
    
    def _clean_caption(self, caption: str) -> str:
        """Clean up the generated caption"""
        # Remove any trailing incomplete sentences
        if caption and not any(caption.endswith(p) for p in [".", "!", "?"]):
            # Find the last complete sentence
            last_period = max(caption.rfind("."), caption.rfind("!"), caption.rfind("?"))
            if last_period > 0:
                caption = caption[:last_period+1]
                
        # Remove any quotes that might be around the caption
        caption = caption.strip('"\'')
        
        return caption

    # Fallback method for when API models aren't available
    def generate_fallback(self, image_description: str, style: str = "casual", num_captions: int = 3) -> List[str]:
        """Fallback caption generation with predefined templates"""
        templates = {
            "casual": [
                "Just another day with {image_objects} ✌️ #goodvibes",
                "Living for moments like these! {image_mood} 💯",
                "This {image_scene} vibe though... 🙌"
            ],
            "professional": [
                "Exploring the intersection of {image_objects} and {image_scene} in today's project.",
                "Showcasing the beauty of {image_objects} in a professional context.",
                "New {image_scene} composition featuring {image_objects}. Thoughts?"
            ],
            "funny": [
                "When the {image_objects} is too good not to share 😂",
                "Plot twist: {image_objects} was the main character all along 🤣",
                "Tell me you love {image_scene} without telling me you love {image_scene}"
            ],
            "inspirational": [
                "Find your {image_mood} even in the midst of chaos. #inspiration",
                "Every {image_scene} has a story to tell. What's yours?",
                "Embrace the journey through every {image_scene} life takes you."
            ],
            "minimalist": [
                "{image_objects}.",
                "{image_mood} vibes.",
                "Just {image_scene} things."
            ],
            "poetic": [
                "Whispers of {image_objects} dance through the {image_scene}, painting dreams.",
                "{image_mood} moments captured in time, forever etched in memory.",
                "Between shadows and light, {image_objects} tells its story."
            ]
        }
        
        # Get templates for the requested style, or default to casual
        style_templates = templates.get(style, templates["casual"])
        
        # Extract elements from image description
        elements = image_description.lower().split()
        image_scene = next((word for word in elements if word in ["beach", "mountains", "city", "forest", "sunset", "home", "office"]), "moment")
        image_objects = next((word for word in elements if word in ["people", "food", "nature", "buildings", "sunset", "technology"]), "view")
        image_mood = next((word for word in elements if word in ["happy", "peaceful", "energetic", "calm", "exciting"]), "amazing")
        
        # Generate captions
        captions = []
        for i in range(min(num_captions, len(style_templates))):
            template = style_templates[i]
            caption = template.format(
                image_scene=image_scene,
                image_objects=image_objects,
                image_mood=image_mood
            )
            captions.append(caption)
            
        # If we need more captions than templates, repeat with variations
        while len(captions) < num_captions:
            template = style_templates[len(captions) % len(style_templates)]
            caption = template.format(
                image_scene=image_scene,
                image_objects=image_objects,
                image_mood=image_mood
            ) + " ✨"  # Add a small variation
            captions.append(caption)
            
        return captions