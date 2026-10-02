import React from 'react';
import './LoadingOverlay.css';

interface LoadingProps {
  size?: number;
  text?: string;
}

export default function LoadingOverlay({ size = 48, text }: LoadingProps) {
  const style = { width: size, height: size };
  return (
    <div className="loading-container">
      <div className="loading-wrapper">
        <div className="spinner" style={style} />
        {text && <div className="loading-text">{text}</div>}
      </div>
    </div>
  );
}
