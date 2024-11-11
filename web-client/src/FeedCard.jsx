import React from 'react';
import './Card.css';

function FeedCard({ type, message, timestamp }) {
  return (
    <div className="card">
      <p>{message} {type === 'bike_return' ? '⬆️' : '⬇️'}</p>
      <span style={{marginLeft: '10px'}}>{timestamp}</span>
    </div>
  );
}

export default FeedCard;
