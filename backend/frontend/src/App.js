import React, { useState } from 'react';
import './styles/main.css';
import ImageUploader from './components/ImageUploader';
import CaptionDisplay from './components/CaptionDisplay';
import StyleSelector from './components/StyleSelector';

function App() {
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState('casual');
  const [error, setError] = useState(null);
  
  // Available caption styles
  const styles = [
    { id: 'casual', name: 'Casual' },
    { id: 'professional', name: 'Professional' },
    { id: 'funny', name: 'Funny' },
    { id: 'inspirational', name: 'Inspirational' },
    { id: 'minimalist', name: 'Minimalist' },
    { id: 'poetic', name: 'Poetic' }
  ];
  
  const handleStyleChange = (style) => {
    setSelectedStyle(style);
    
    // If we already have results, regenerate captions with new style
    if (result) {
      handleImageUpload(image, style);
    }
  };
  
  const handleImageUpload = async (imageFile, style = selectedStyle) => {
    setLoading(true);
    setError(null);
    
    try {
      // Create form data for API request
      const formData = new FormData();
      formData.append('file', imageFile);
      formData.append('style', style);
      formData.append('num_captions', 3);
      formData.append('num_hashtags', 10);
      
      // Make API request
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }
      
      const data = await response.json();
      setResult(data);
      setImage(imageFile);
    } catch (err) {
      console.error('Error uploading image:', err);
      setError('Failed to analyze image. Please try again.');
    } finally {
      setLoading(false);
    }
  };
  
  const handleRetry = () => {
    if (image) {
      handleImageUpload(image);
    }
  };
  
  return (
    <div className="app-container">
      <header>
        <h1>Instagram Caption Generator</h1>
        <p>Upload an image to get AI-generated captions and hashtags</p>
      </header>
      
      {error && (
        <div className="error-message">
          <p>{error}</p>
          <button onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}
      <main>
        <div className="app-content">
          <div className="app-left-panel">
            <StyleSelector 
              styles={styles} 
              selectedStyle={selectedStyle} 
              onStyleChange={handleStyleChange} 
            />
            <ImageUploader 
              onImageUpload={handleImageUpload} 
              loading={loading} 
            />
          </div>
          
          {result && (
            <div className="app-right-panel">
              <CaptionDisplay 
                result={result} 
                onRetry={handleRetry} 
                loading={loading}
              />
            </div>
          )}
        </div>
      </main>
      
      <footer>
        <p>© 2025 Instagram Caption Generator | AI Powered</p>
      </footer>
    </div>
  );
}

export default App;