import { useEffect, useState } from 'react'
import { socket } from './socket'
import './App.css'
import BarChart from './components/BarChart'
import Information from './components/Information'

function App() {
  const [data, setData] = useState({'name': 'NONE', 'probability': [0, 0, 0]});

  // Initialize exercise repetition count as state variables
  const [curl, setCurl] = useState(0);
  const [press, setPress] = useState(0);
  const [raise, setRaise] = useState(0);
  
  const [isConnected, setIsConnected] = useState(socket.connected);
  
  // Establishes events for socket
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

  // Runs if Arduino data has changed
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

  return (
    <div>
      <Information curl={curl} press={press} raise={raise}></Information>
      <BarChart probabilities={data['probability']}></BarChart>
    </div>
  )
}

export default App
