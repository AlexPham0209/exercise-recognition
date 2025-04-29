import { Bar } from "react-chartjs-2"
import { Chart as ChartJS, CategoryScale, Tooltip, Legend, LinearScale, BarElement} from "chart.js";
ChartJS.register(CategoryScale, LinearScale, Tooltip, Legend, BarElement);

export default function BarChart({ probabilities }) {
    // Define the data structure
    const dataset = {
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
    <Bar data={dataset}></Bar>
  );
}