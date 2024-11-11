import { io } from 'socket.io-client';

const socket = io('http://localhost:8080', {transports: ["websocket", "polling"]}); // Replace with your server URL

// 이벤트 등록
socket.on('connect', () => {
  console.log('Connected to server');
});

socket.on('message', (message) => {
  console.log('New message:', message);
});

export default socket;
