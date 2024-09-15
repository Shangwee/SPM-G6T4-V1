<template>
    <div class="weather-analysis">
      <h1>Past Weather Analysis</h1>
      <p>These charts show the weather condition for each month and the month that has the most number of winter storms.</p>
      <div class="charts">
        <img src="../assets/weather_heatmap.PNG" alt="Weather Heatmap" class="chart">
        <img src="../assets/weather_barchart.PNG" alt="Winter Storm Prediction" class="chart">
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'WeatherAnalysis'
  };
  </script>
  
  <style scoped>
  .weather-analysis {
    text-align: center;
    margin-top: 20px;
    background-color: #ECECEC; 
  }
  
  .charts {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
  }
  
  .chart {
    max-width: 50%; 
    margin: 0 10px; 
  }
  </style>
  