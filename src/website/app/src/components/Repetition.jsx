import '../App.css'
import Card from "./Card";

export default function Repetition({exercise, count}) {
    return (
        <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', color: "white", borderRadius: '5px', boxShadow: `2px 0px 5px 2px rgba(168, 168, 208, 0.3)`, width: '130px', height: '170px', verticalAlign: 'middle'}}>
            <h3 style={{textAlign: 'center', color: 'black'}}>{exercise}</h3>
            <p style={{textAlign: 'center', color: 'black'}}>{count}</p>
        </div>
    );
}