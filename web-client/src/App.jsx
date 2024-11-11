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
  const [stations, setStations] = useState([{name: '서울역', address: '서울역 주소'}, {name: '용산역', address: '용산역 주소'}]);


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

  useEffect(() => {
    if (searchQ === '') {
      setMatches([]);
    }

  }, [searchQ]);

  useEffect(() => {
    socket.on('stn_list', (message) => {
      setStations(JSON.parse(message));
      console.log("SET STATION")
    });

    socket.on('bike_return', (message) => {
      message.type = 'bike_return';
      setFeed((prevFeed) => [message, ...prevFeed]);
    });

    socket.on('bike_rent', (message) => {
      message.type = 'bike_return';
      setFeed((prevFeed) => [message, ...prevFeed]);
    })

    socket.emit('stn_list', {});

    return () => {
      socket.disconnect()
    };
  }, []);

  return (
    <div className="container">
      <div className="left-pane">
        <h2>List</h2>
        <input className="search" placeholder={'대여소 이름으로 검색하기'} onKeyPress={handleKeyPress} ref={inputRef} onChange={handleSearchQChange}/>
        <div className="card-container">
          {matches.length === 0 ? stations.map(station => (StationCard({ station }))) : matches.map(station => (StationCard({ station })))}
        </div>
      </div>
      <div className="right-pane">
        <h2>Feed</h2>
        <div className="card-container">
          {feed.length !== 0 ? feed.map(f => (FeedCard(f))) : '피드가 없습니다.'}
        </div>
      </div>
    </div>
  )
}

export default App
