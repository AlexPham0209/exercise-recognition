import '../App.css'
import Repetition from './Repetition';
export default function Information({curl, raise, press}) {
    return (
        <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly', marginBottom: '10vh'}}>
            <Repetition exercise={"Curls"} count={curl}></Repetition>
            <Repetition exercise={"Raises"} count={raise}></Repetition>
            <Repetition exercise={"Presses"} count={press}></Repetition>
        </div>
    );
}