import { useEffect, useState } from 'react'
import { socket } from './socket'
import './App.css'
import BarChart from './components/BarChart'
import Information from './components/Information'

function App() {
  const [probability, setProbability] = useState([0, 0, 0]);

  // Initialize exercise repetition count as state variables
  const [curl, setCurl] = useState(0);
  const [press, setPress] = useState(0);
  const [raise, setRaise] = useState(0);
  
  // Establishes events for socket
  useEffect(() => {
    function onDataEvent(value) {
      setProbability(value['probability']);

      switch (value['name']) {
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
    }

    socket.on('data', onDataEvent);
    return () => {
      socket.off('data', onDataEvent);
    };
  });

  return (
    <div>
      <h1 style={{display: 'block', textAlign: 'center', marginBottom: '1.5em', fontSize: '2.5em'}}>Exercise Motion Detector 💪</h1>
      <Information curl={curl} press={press} raise={raise}></Information>
      <BarChart probabilities={probability}></BarChart>
    </div>
  )
}

export default App
