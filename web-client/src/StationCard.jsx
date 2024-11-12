import React from 'react';
import './Card.css';

function StationCard({ station }) {
  return (
    <div className="station" style={{display: 'flex', flexDirection: 'row'}}>
      <div className="card">
        <span>{station.stnName} | {station.stnGrpName}</span>
        <p>{station.stnAddr1} {station.stnAddr2}</p>
      </div>
      <span style={{alignContent: 'center'}}>대여 가능 자전거 수: {station.parkedBikeCnt !== undefined ? station.parkedBikeCnt : '정보 없음'}</span>
    </div>
  );
}

export default StationCard
