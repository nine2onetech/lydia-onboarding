import React from 'react';
import './Card.css';

function StationCard({ station }) {
  return (
    <div className="card">
      <span>{station.stnName} | {station.stnGrpName}</span>
      <p>{station.stnAddr1} {station.stnAddr2}</p>
    </div>
  );
}

export default StationCard
