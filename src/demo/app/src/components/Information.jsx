import '../App.css'
import Repetition from './Repetition';
export default function Information({curl, press, raise}) {
    return (
        <div style={{display: 'flex', flexDirection: 'row', justifyContent: 'space-evenly', marginBottom: '10vh'}}>
            <Repetition exercise={"Curls"} count={curl}></Repetition>
            <Repetition exercise={"Presses"} count={press}></Repetition>
            <Repetition exercise={"Raises"} count={raise}></Repetition>
        </div>
    );
}