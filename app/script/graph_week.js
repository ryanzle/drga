import { temperature } from "./week_temp.js";
import { humidity } from "./week_hum.js";
import { moisture } from "./week_moist.js";
import { light } from "./week_light.js";
import { 
    Chart, ScatterController, Colors, Legend, PointElement, CategoryScale, LinearScale, LineElement, Tooltip
}
from "../node_modules/chart.js/dist/chart.js";
Chart.register(ScatterController, Colors, Legend, PointElement, CategoryScale, LinearScale, LineElement, Tooltip);

var chartType = document.getElementsByClassName("chart");
var chClass = chartType.item(1).classList[1];
var chartClass = chClass.toUpperCase();
var chartID = chartType.item(1).id;
var chartData;
var measure;

var ctx = document.getElementById(chartID).getContext("2d");

/*grab correct data from json*/
if(chartClass == "HUMEDAD") {
    chartData = humidity;
    measure = "%";
}
else if(chartClass == "TEMPERATURA") {
    chartData = temperature;
    measure = "°C";
}
else if (chartClass == "SUELO") {
    chartData = moisture;
    measure = "%";
}
else if (chartClass == "LUZ") {
    chartData = light;
    measure = "";
}

/* transform object of obejcts --> array of objects */
chartData = Object.values(chartData);

new Chart(
ctx, 
{
    type: "scatter",
    data: {
        labels: ["00:00", "01:00"],
        datasets: [{
            label: "POR SEMANA",
            data: chartData,
            showLine: true,
        }],
    },
        options: {
            plugins: {
                tooltip: {
                    enabled: true,
                },
            },
            scales: {
                x: {
                    ticks: {
                        callback: value => `2023-5-${value}`
                    }
                },
                y: {
                    min: 0,
                    ticks: {
                        callback: value => `${value}${measure}`
                    }
                },
            },
        },
});