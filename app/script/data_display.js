//using module functions in js file to import data.js file
//  cannot import .json file & thus must format json as .js file
import data from "./data.js";

//assign all values from data to variables
//is there a better way to iterate through the array? lol
let data_arr = [];
data_arr[0] = data.temperature;
data_arr[1] = data.humidity;
data_arr[2] = data.moisture;
data_arr[3] = parseInt(data.light_intensity);
data_arr[4] = data.time;


//TIMESTAMP REPLACEMENT
//  note: potentially need to implement individual timestamp controls?

//get all elements in html file with class name "timestamp"
var times = document.getElementsByClassName("timestamp");

//iterate through # of elements grabbed & replace text with timestamp value
for(var x = 0; x < times.length; x++) {
    times.item(x).innerText = data_arr[4];
}

//DATA REPLACEMENT
//  note: potentially need to implement distinguishing diff sensors
//  just using sensor 1 for now

//get all elements in html file with the class name "value"
var values = document.getElementsByClassName("value");

//iterate through # of elements grabbed & replace text with corresponding data array value
for(let y = 0; y < 4; y++) {
    values.item(y).innerText = data_arr[y];
    values.item(y+4).innerText = data_arr[y];
}
