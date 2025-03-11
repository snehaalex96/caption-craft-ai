import random
from typing import List, Dict, Any

# Dictionary of common hashtags by category
HASHTAG_CATEGORIES = {
    "nature": ["nature", "naturelovers", "naturephotography", "outdoors", "landscape", 
               "mountains", "beach", "ocean", "sunset", "sunrise", "sky", "clouds", 
               "forest", "hiking", "wildlife", "wilderness", "earthpix", "naturegram"],
    
    "urban": ["city", "cityscape", "architecture", "urban", "street", "building", 
              "skyscraper", "downtown", "citylife", "cityview", "citylights", 
              "streetphotography", "urbanphotography", "explore", "travel"],
    
    "food": ["food", "foodporn", "foodie", "instafood", "foodphotography", "yummy", 
             "delicious", "homemade", "breakfast", "lunch", "dinner", "dessert", 
             "cooking", "baking", "healthyfood", "foodblogger", "foodlover", "foodgram"],
    
    "portrait": ["portrait", "portraitphotography", "selfie", "model", "fashion", 
                "beauty", "makeup", "style", "outfit", "ootd", "fashionblogger", 
                "portraitmood", "portraiture", "face", "smile", "eyes"],
    
    "lifestyle": ["lifestyle", "life", "happy", "love", "instagood", "beautiful", 
                 "photooftheday", "inspiration", "motivation", "positivevibes", 
                 "goodvibes", "mindfulness", "selflove", "gratitude", "blessed"],
    
    "travel": ["travel", "travelgram", "wanderlust", "adventure", "explore", 
               "traveling", "holiday", "vacation", "tourism", "travelphotography", 
               "instatravel", "trip", "journey", "travelblogger", "destination", 
               "globetrotter", "traveltheworld"],
    
    "fitness": ["fitness", "gym", "workout", "fit", "training", "exercise", "health", 
                "healthy", "bodybuilding", "fitnessmotivation", "sport", "running", 
                "yoga", "strength", "fitlife", "fitnessjourney", "gains"],
    
    "pets": ["pet", "dog", "cat", "puppy", "kitten", "dogsofinstagram", "catsofinstagram", 
             "animals", "petsofinstagram", "dogstagram", "catstagram", "instadog", 
             "instacat", "petstagram", "cuteanimals", "adoptdontshop"],
    
    "creative": ["art", "artist", "artwork", "design", "drawing", "painting", "sketch", 
                "illustration", "creative", "creativity", "artistsoninstagram", 
                "instaart", "digitalart", "handmade", "artistic", "contemporaryart"],
    
    "technology": ["technology", "tech", "gadgets", "innovation", "programming", "coding", 
                  "developer", "computer", "smartphone", "software", "hardware", 
                  "electronics", "science", "engineering", "future", "digital"],
    
    "events": ["party", "celebration", "wedding", "birthday", "concert", "festival", 
              "event", "music", "dance", "nightlife", "fun", "friends", "ceremony", 
              "reception", "celebration", "congrats", "cheers"],
    
    "business": ["business", "entrepreneur", "startup", "success", "motivation", 
                "leadership", "marketing", "smallbusiness", "entrepreneurship", 
                "businessowner", "hustle", "work", "career", "goals", "boss"],
    
    "popular": ["instagood", "photooftheday", "beautiful", "photography", "instagram", 
               "picoftheday", "follow", "followme", "like4like", "instadaily", 
               "bestoftheday", "amazing", "instalike", "igers", "likeforlike", 
               "20likes", "nofilter", "style", "swag", "instamood"]
}

# Trending or seasonal hashtags
TRENDING_HASHTAGS = [
    "trending", "viral", "challenge", "mondaymotivation", "tuesdayvibe", "wednesdaywisdom", 
    "throwbackthursday", "tbt", "flashbackfriday", "weekendvibes", "sundayfunday"
]

def map_description_to_categories(description: str) -> List[str]:
    """
    Map image description to relevant hashtag categories
    
    Args:
        description: Image description
        
    Returns:
        List of relevant hashtag categories
    """
    # Convert description to lowercase for easier matching
    desc_lower = description.lower()
    
    # Keywords to category mapping
    keyword_mapping = {
        "nature": ["nature", "outdoor", "landscape", "mountain", "beach", "ocean", "sunset", "sunrise", 
                  "sky", "cloud", "forest", "hiking", "wildlife", "wilderness", "tree", "flower", "plant"],
        "urban": ["city", "urban", "street", "building", "skyscraper", "downtown", "architecture"],
        "food": ["food", "eat", "drink", "meal", "breakfast", "lunch", "dinner", "dessert", "restaurant", "cafe"],
        "portrait": ["person", "people", "portrait", "selfie", "face", "smile", "model", "fashion"],
        "lifestyle": ["lifestyle", "home", "living", "happy", "relax", "mindful", "positive"],
        "travel": ["travel", "adventure", "explore", "journey", "destination", "vacation", "holiday", "tourism"],
        "fitness": ["fitness", "gym", "workout", "exercise", "training", "sport", "run", "yoga"],
        "pets": ["pet", "dog", "cat", "animal"],
        "creative": ["art", "creative", "design", "drawing", "painting", "artistic"],
        "technology": ["technology", "tech", "gadget", "device", "computer", "phone", "digital"],
        "events": ["party", "celebration", "wedding", "birthday", "concert", "festival", "event"],
        "business": ["business", "work", "professional", "office", "meeting", "presentation"]
    }
    
    # Find matching categories
    matching_categories = []
    for category, keywords in keyword_mapping.items():
        if any(keyword in desc_lower for keyword in keywords):
            matching_categories.append(category)
    
    # Always include popular hashtags
    matching_categories.append("popular")
    
    # If no specific categories matched, default to lifestyle and popular
    if len(matching_categories) <= 1:  # Just "popular" means no specific matches
        matching_categories = ["lifestyle", "popular"]
    
    return matching_categories

def generate_hashtags(description: str, count: int = 10) -> List[str]:
    """
    Generate Instagram hashtags based on image description
    
    Args:
        description: Image description
        count: Number of hashtags to generate
        
    Returns:
        List of hashtags
    """
    # Map description to relevant categories
    categories = map_description_to_categories(description)
    
    # Collect hashtags from matching categories
    all_hashtags = []
    for category in categories:
        if category in HASHTAG_CATEGORIES:
            all_hashtags.extend(HASHTAG_CATEGORIES[category])
    
    # Add some trending hashtags
    all_hashtags.extend(random.sample(TRENDING_HASHTAGS, min(3, len(TRENDING_HASHTAGS))))
    
    # Remove duplicates and shuffle
    unique_hashtags = list(set(all_hashtags))
    random.shuffle(unique_hashtags)
    
    # Return the requested number of hashtags with # prefix
    selected_hashtags = unique_hashtags[:count]
    return [f"#{tag}" for tag in selected_hashtags]