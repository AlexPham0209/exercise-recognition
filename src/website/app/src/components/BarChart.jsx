import { Bar } from "react-chartjs-2"
import { Chart as ChartJS, CategoryScale, Tooltip, Legend, LinearScale, BarElement} from "chart.js";
import Card from "./Card";
ChartJS.register(CategoryScale, LinearScale, Tooltip, Legend, BarElement);

export default function BarChart({probabilities}) {
    // Define the data structure
    const data = {
        labels: ["Curl", "Press", "Raise"],
        datasets: [{
            label: "Probability",
            backgroundColor: [
                "rgba(43, 63, 229, 0.8)",
                "rgba(250, 192, 19, 0.8)",
                "rgba(253, 135, 135, 0.8)",
            ],
            borderRadius: 5,
            data: probabilities
        }]
    } 

    // Define bar options
    const options =  {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true, 
                suggestedMax: 1.0
            }
        }
    }

    return (
        <Card>
            <Bar data={data} options={options} width="500px" height="250px"></Bar>
        </Card>
    );
}