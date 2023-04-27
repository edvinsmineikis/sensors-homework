<script>
// This application uses Grid.vue from https://vuejs.org/examples/#grid
import DemoGrid from "./Grid.vue"

const API_URL = `http://localhost:5000/`

export default {
  components: {
    DemoGrid
  },
  data: () => ({
    searchQuery: "",
    gridColumns: [],
    gridData: [],
    metrics: null,
    sensors: null,
    sensorTypes: null,
    checkedUnits: []
  }),

  methods: {

    async fetchData() {
      this.gridData = [];
      this.metrics = await this.getJson("metrics.json");
      this.sensors = await this.getJson("sensors.json");
      this.sensorTypes = await this.getJson("sensorTypes.json");
      this.createGridColumns();
      this.updateGridData();
    },

    async getJson(endpoint) {
      const url = API_URL + endpoint;
      const response = await fetch(url);
      return response.json();
    },

    // Creates grid columns based on the metrics selected in checkboxes
    createGridColumns() {
      this.gridColumns = ["sensorName", "sensorType"];
      let items = this.metrics["data"]["items"];
      for (let item in items) {
        let metricDetails = this.getMetricDetails(items[item]["id"])
        console.log(metricDetails["name"]);
        if (this.checkedUnits.includes(metricDetails["name"])) {
          this.gridColumns.push(metricDetails["name"] + " " + metricDetails["unit"]);
        }
      }
    },

    // Unfortunately Grid.vue requires that value name == column name,
    // that's why it has to match exactly.
    updateGridData() {
      for (let key in this.sensors) {
        let sensor = this.sensors[key];
        let sensorDict = {};
        sensorDict["sensorName"] = sensor["name"];
        let type = sensor["type"];
        let variant = sensor["variant"];
        try {
          sensorDict["sensorType"] = this.sensorTypes[type][variant]["name"];
        } catch {
          ;
        }
        for (let metricId in sensor["metrics"]) {
          let metricDetails = this.getMetricDetails(metricId);
          let columnName = metricDetails["name"] + " " + metricDetails["unit"];
          sensorDict[columnName] = sensor["metrics"][metricId]["v"];
        }
        this.gridData.push(sensorDict);
      }
    },
    
    // Returns the metric name and unit symbol with "selected: true", based on metric ID
    getMetricDetails(metricId) {
      let items = this.metrics["data"]["items"];
      for (let item in items) {
        if (items[item]["id"] == metricId) {
          let units = items[item]["units"];
          let unitSymbol = "";
          for (let unit in items[item]["units"]) {
            if ("selected" in units[unit] && units[unit]["selected"] == true) {
              let unitSymbol = units[unit]["name"];
              return {
                "name": items[item]["name"],
                "unit": unitSymbol
              }
            }
          }
        }
      }
    }
  }
}
</script>


<template>
  <h2>Sensor table</h2><br>
  <div class="checkboxes">
      <div class="column">
          <input type="checkbox" id="temperature" value="Temperature" v-model="checkedUnits">
          <label for="temperature">Temperature</label><br>
          <input type="checkbox" id="humidity" value="Humidity" v-model="checkedUnits">
          <label for="humidity">Humidity</label><br>
          <input type="checkbox" id="co2" value="CO₂" v-model="checkedUnits">
          <label for="co2">CO₂</label><br>
          <input type="checkbox" id="pressure" value="Atmospheric Pressure" v-model="checkedUnits">
          <label for="pressure">Atmospheric Pressure</label><br>
          <input type="checkbox" id="voltage" value="Voltage" v-model="checkedUnits">
          <label for="voltage">Voltage</label><br>
      </div><br>
      <div class="column">
          <input type="checkbox" id="current" value="Current" v-model="checkedUnits">
          <label for="current">Current</label><br>
          <input type="checkbox" id="weight" value="Weight" v-model="checkedUnits">
          <label for="weight">Weight</label><br>
          <input type="checkbox" id="water" value="Volumetric Water Content" v-model="checkedUnits">
          <label for="water">Volumetric Water Content</label><br>
          <input type="checkbox" id="soilperm" value="Soil Dielectric Permittivity" v-model="checkedUnits">
          <label for="soilperm">Soil Dielectric Permittivity</label><br>
          <input type="checkbox" id="soilcond" value="Soil Electrical Condunctivity" v-model="checkedUnits">
          <label for="soilcond">Soil Electrical Conductivity</label><br>
      </div><br>
      <div class="column">
          <input type="checkbox" id="porecond" value="Pore Electrical Conductivity" v-model="checkedUnits">
          <label for="porcond">Pore Electrical Conductivity</label><br>
          <input type="checkbox" id="ppfd" value="PPFD" v-model="checkedUnits">
          <label for="ppfd">PPFD</label><br>
          <input type="checkbox" id="distance" value="Distance" v-model="checkedUnits">
          <label for="distance">Distance</label><br>
          <input type="checkbox" id="rssi" value="RSSI" v-model="checkedUnits">
          <label for="rssi">RSSI</label><br>
          <input type="checkbox" id="battery" value="Battery voltage" v-model="checkedUnits">
          <label for="battery">Battery voltage</label><br>
      </div>
  </div><br>
  <div class="searchbox">
      <form id="search">
          Search by sensor name or type <input name="query" v-model="searchQuery">
      </form>
      <button v-on:click="fetchData">Fetch data</button>
      <button v-on:click="debugKey">Debug</button>
  </div>
  <br><br>
  <DemoGrid :data="gridData" :columns="gridColumns" :filter-key="searchQuery">
  </DemoGrid>
</template>