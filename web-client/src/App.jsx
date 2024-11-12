import { useState, useRef, useEffect } from 'react'
import StationCard from './StationCard'
import FeedCard from './FeedCard'
import './App.css';
import socket from "./socket.js";

function App() {
  const [searchQ, setSearchQ] = useState('')
  const [matches, setMatches] = useState([])
  const inputRef = useRef();
  const [feed, setFeed] = useState([]);
  const [stations, setStations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);


  const searchByName = () => {
    if (searchQ === '') {
      return alert('전송할 메시지를 입력해주세요:)');
    }
    const matches = stations.filter(station => station.stnName.includes(searchQ));
    setMatches(matches);
  };

  const handleKeyPress = e => {
    if (e.key === 'Enter') {
      searchByName();
    }
  };

  const handleSearchQChange = (e) => {
    setSearchQ(e.target.value);
  }

  const refreshFeed = () => {
    socket.emit('feed', {});
    setIsLoading(true);

  }

  useEffect(() => {
    if (searchQ === '') {
      setMatches([]);
    }

  }, [searchQ]);

  useEffect(() => {
    socket.on('stn_list', (message) => {
      setStations(message);
    });

    socket.on('bike_return', (message) => {
      if (isLoading === true) {
        setIsLoading(false);
      }
      message.type = 'bike_return';
      setFeed((prevFeed) => [message, ...prevFeed]);
      setStations((prevStations) =>
        prevStations.map(station =>
          station.stnId === message.stn_id ? { ...station, parkedBikeCnt: message.parked_bike_cnt } : station
        )
      );
    });

    socket.on('bike_rent', (message) => {
      if (isLoading === true) {
        setIsLoading(false);
      }
      message.type = 'bike_return';
      setFeed((prevFeed) => [message, ...prevFeed]);

      setStations((prevStations) =>
        prevStations.map(station =>
          station.stnId === message.stn_id ? { ...station, parkedBikeCnt: message.parked_bike_cnt } : station
        )
      );
    })

    socket.emit('stn_list', {});
    socket.emit('feed', {});

    return () => {
      socket.off('stn_list');
      socket.off('bike_return');
      socket.off('bike_rent');
    };
  }, [isLoading]);

  return (
    <div className="container">
      <div className="left-pane">
        <h2>List</h2>
        <input className="search" placeholder={'대여소 이름으로 검색하기'} onKeyPress={handleKeyPress} ref={inputRef} onChange={handleSearchQChange}/>
        <div className="card-container">
          {matches.length === 0 ? stations.map(station => <StationCard key={station.stnId} station={station} />) : matches.map(station => <StationCard key={station.stnId} station={station} />)}
        </div>
      </div>
      <div className="right-pane">
        <h2>Feed</h2>
        <button onClick={refreshFeed}>즉시 새로고침</button>
        {isLoading === true && <p>새로고침 중...</p>}
        <div className="card-container">
          {feed.length !== 0 ? feed.map(f => (FeedCard(f))) : '피드가 없습니다.'}
        </div>
      </div>
    </div>
  )
}

export default App
