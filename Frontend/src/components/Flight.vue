<template>
    <div class="flight-analysis">
      <h1>Past Flight Operation Analysis</h1>
      <div class="charts">
        <img src="../assets/flightcharts.jpg" class="chart">
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'FlightAnalysis'
  };
  </script>
  
  <style scoped>
  .flight-analysis {
    text-align: center;
    margin-top: 20px;
    background-color: #ECECEC; 
    
  }
  
  .charts {
    display: flex;
    justify-content: space-around;
    margin-top: 20px;
    
  }
  
  </style>
  