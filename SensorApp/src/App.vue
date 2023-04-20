<script>
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

  //created() {
  //  // fetch on init
  //  this.fetchData();
  //},

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
    updateGridData() {
      for (let key in this.sensors) {
        let sensorDict = {};
        for (let i in this.gridColumns) {
          sensorDict[this.gridColumns[i]] = "";
        }
        let sensor = this.sensors[key];
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
    },

    debugKey() {
      console.log(this.checkedUnits);
      console.log(this.checkedUnits.includes("Battery Voltage"));

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

<style>
.checkboxes {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}

.column {
  flex-basis: calc(33.33% - 10px);
  margin-right: 10px;
}
</style>