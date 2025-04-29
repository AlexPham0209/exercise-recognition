import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import { socket } from './socket'
import './App.css'

function App() {
  const [count, setCount] = useState(0);

  const [data, setData] = useState({});
  const [curl, setCurl] = useState(0);
  const [press, setPress] = useState(0);
  const [raise, setRaise] = useState(0);
  
  const [isConnected, setIsConnected] = useState(socket.connected);
  
  useEffect(() => {
    function onConnect() {
      setIsConnected(true);
    }

    function onDisconnect() {
      setIsConnected(false);
    }

    function onDataEvent(value) {
      setData(value);
    }

    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('data', onDataEvent);

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('data', onDataEvent);
    };
  });

  useEffect(() => {
    switch (data['name']) {
      case "CURL":
        setCurl(current => current + 1);
        break;
  
      case "PRESS":
        setPress(current => current + 1);
        break;
      
      case "RAISE":
        setRaise(current => current + 1);
        break;
    }
  }, [data]);
  
  console.log(curl);
  console.log(press);
  console.log(raise + "\n\n");

  return (
    <>
      
    </>
  )
}

export default App
