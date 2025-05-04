export default function Card(props) {
    return (
        <div class="card" style={{color: "white", borderRadius: '5px', boxShadow: `2px 0px 5px 2px rgba(168, 168, 208, 0.3)`, blockSize: 'fit-content'}}>
            {props.children}
        </div>
    );
}