import React, { useState, useRef } from 'react';

const ImageUploader = ({ onImageUpload, loading }) => {
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);
  
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      processFile(file);
    }
  };
  
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        processFile(file);
      }
    }
  };
  
  const processFile = (file) => {
    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreview(e.target.result);
    };
    reader.readAsDataURL(file);
    
    // Send to parent component
    onImageUpload(file);
  };
  
  const handleButtonClick = () => {
    fileInputRef.current.click();
  };
  
  return (
    <div className="image-uploader">
      <h2>Upload Image</h2>
      
      <div 
        className={`upload-area ${dragActive ? 'drag-active' : ''} ${preview ? 'has-preview' : ''}`}
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={preview ? null : handleButtonClick}
      >
        {loading ? (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>Analyzing image...</p>
          </div>
        ) : preview ? (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="image-preview" />
            <button 
              className="change-image-btn"
              onClick={handleButtonClick}
              disabled={loading}
            >
              Change Image
            </button>
          </div>
        ) : (
          <div className="upload-prompt">
            <div className="upload-icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 5V19M12 5L6 11M12 5L18 11" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <p>Drag and drop an image here, or click to browse</p>
            <span>Supports JPG, PNG, WEBP (Max 5MB)</span>
          </div>
        )}
      </div>
      
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: 'none' }}
      />
    </div>
  );
};

export default ImageUploader;