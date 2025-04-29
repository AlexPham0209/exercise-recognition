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
            data: probabilities
        }]
    } 

    // Define bar options
    const options =  {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true }
        }
    }

  return (
    <Card>
        <Bar data={data}></Bar>
    </Card>
  );
}