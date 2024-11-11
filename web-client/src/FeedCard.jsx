import React from 'react';
import './Card.css';

function FeedCard({ type, message }) {
  const timestamp = new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
  return (
    <div className="card">
      <p>{message} {type === 'bike_return' ? '⬆️' : '⬇️'}</p>
      <span style={{marginLeft: '10px'}}>{timestamp}</span>
    </div>
  );
}

export default FeedCard;
