import React from 'react';

const StyleSelector = ({ styles, selectedStyle, onStyleChange }) => {
  return (
    <div className="style-selector">
      <h2>Caption Style</h2>
      <div className="style-options">
        {styles.map(style => (
          <button
            key={style.id}
            className={`style-button ${selectedStyle === style.id ? 'active' : ''}`}
            onClick={() => onStyleChange(style.id)}
          >
            {style.name}
          </button>
        ))}
      </div>
      <div className="style-description">
        {selectedStyle === 'casual' && (
          <p>Friendly, conversational captions that feel natural and relatable.</p>
        )}
        {selectedStyle === 'professional' && (
          <p>Polished, business-appropriate captions for your professional content.</p>
        )}
        {selectedStyle === 'funny' && (
          <p>Humorous, witty captions to make your audience smile or laugh.</p>
        )}
        {selectedStyle === 'inspirational' && (
          <p>Motivational captions to inspire and encourage your followers.</p>
        )}
        {selectedStyle === 'minimalist' && (
          <p>Short, simple captions that let your image do the talking.</p>
        )}
        {selectedStyle === 'poetic' && (
          <p>Artistic, flowery language that adds a touch of poetry to your posts.</p>
        )}
      </div>
    </div>
  );
};

export default StyleSelector;