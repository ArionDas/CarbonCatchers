// section--1
const co = document.querySelector(".co span");
const nh3 = document.querySelector(".nh3 span");
const no = document.querySelector(".no span");
const no2 = document.querySelector(".no2 span");
const o3 = document.querySelector(".o3 span");
const pm2 = document.querySelector(".pm2 span");
const pm10 = document.querySelector(".pm10 span");
const so2 = document.querySelector(".so2 span");

// Store your API key securely (consider using a separate file or environment variable)
const apiKey = "2329ee405f2d857e44f4106497f84b00";

// Function to update AQI data in the DOM
function updateAqiData(data) {
  co.textContent = Math.round(data.co);
  nh3.textContent = Math.round(data.nh3);
  no.textContent = Math.round(data.no);
  no2.textContent = Math.round(data.no2);
  o3.textContent = Math.round(data.o3);
  pm2.textContent = Math.round(data.pm2_5);
  pm10.textContent = Math.round(data.pm10);
  so2.textContent = Math.round(data.so2);
}

// Function to fetch and update AQI data
async function fetchAndSetAqiData(lat, long) {
  try {
    const response = await fetch(
      `http://api.openweathermap.org/data/2.5/air_pollution?lat=${lat}&lon=${long}&appid=${apiKey}`
    );
    if (!response.ok) {
      throw new Error("API request failed");
    }
    const data = await response.json();
    const aqiComponents = data.list[0].components;
    updateAqiData(aqiComponents);

    // Convert aqiComponents object to an array
    const aqiComponentsArray = convertToList(aqiComponents);

    // Update the chart data
    dataChart.data.datasets[0].data = aqiComponentsArray;
    dataChart.update();
  } catch (error) {
    console.error(error);
  }
}
// Get geolocation and fetch AQI data
navigator.geolocation.getCurrentPosition(
  (position) => {
    const { latitude, longitude } = position.coords;
    fetchAndSetAqiData(latitude, longitude);
  },
  (error) => {
    console.error(error);
  }
);

// section--2--graphs
function convertToList(obj) {
  return Object.values(obj);
}
let myChart = document.getElementById("myChart").getContext("2d");
let dataChart = new Chart(myChart, {
  type: "doughnut",
  data: {
    labels: ["CO2", "NH3", "NO", "NO2", "O3", "PM2.5", "PM10", "SO2"],
    datasets: [
      {
        label: "Population",
        data: [], // Initialize with an empty array
        backgroundColor: [
          "rgba(255, 99, 132, 0.8)", // Background color for the bars
          "rgba(54, 162, 235, 0.8)",
          "rgba(255, 206, 86, 0.8)",
          "rgba(75, 192, 192, 0.8)",
          "rgba(153, 102, 255, 0.8)",
          "rgba(255, 159, 64, 0.8)",
          "rgba(255, 99, 132, 0.8)",
          "rgba(54, 162, 235, 0.8)",
        ],
        borderColor: "black",
        borderWidth: 1, // Border width for the bars
      },
    ],
  },
  options: {
    responsive: true,
    legend: {
      labels: {
        fontColor: "white",
        fontSize: 18,
      },
    },
  },
});

// section--3 map

var OSM_URL = "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
var OSM_ATTRIB =
  '&copy;  <a  href="http://openstreetmap.org/copyright">OpenStreetMap</a>  contributors';
var osmLayer = L.tileLayer(OSM_URL, { attribution: OSM_ATTRIB });

var WAQI_URL =
  "https://tiles.waqi.info/tiles/usepa-aqi/{z}/{x}/{y}.png?token=1efc09cf3e09e8066d64dc5844d4852ec7920ef5";
var WAQI_ATTR =
  'Air  Quality  Tiles  &copy;  <a  href="http://waqi.info">waqi.info</a>';
var waqiLayer = L.tileLayer(WAQI_URL, { attribution: WAQI_ATTR });

navigator.geolocation.getCurrentPosition(
  (position) => {
    var map = L.map("map").setView(
      [position.coords.latitude, position.coords.longitude],
      11
    );
    map.addLayer(osmLayer).addLayer(waqiLayer);
  },
  (error) => {
    console.log(error);
  }
);
var map = L.map("map").setView([0, 0], 11);
// submit button
const input_area = document.querySelector(".input-area");
const submit = document
  .querySelector(".submit")
  .addEventListener("click", () => {
    document.querySelector("#map").style.display = "block";
    document.querySelector(".scale").style.display = "none";
    const apiKey = "2329ee405f2d857e44f4106497f84b00";

    // Construct the API URL
    const apiUrl = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(
      input_area.value
    )}&appid=${apiKey}`;

    // Make an HTTP request to the API
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        if (data.coord) {
          const lat = data.coord.lat;
          const lon = data.coord.lon;
          fetchAndSetAqiData(lat, lon);
          map.setView([lat, lon], 11);
          map.eachLayer(function (layer) {
            map.removeLayer(layer);
          });
          map.addLayer(osmLayer).addLayer(waqiLayer);
        } else {
          console.error("Geocoding request failed or no results found.");
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
    document.querySelector(
      ".search--bar .place"
    ).textContent = `${input_area.value}`;
  });
