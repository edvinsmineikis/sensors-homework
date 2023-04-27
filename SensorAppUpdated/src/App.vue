<template>
  <div>
    <ColumnSelector :metrics="this.metrics"/>
  </div>
  <div>
    <Table :headers-data="this.metrics" :sensor-data="this.sensors"/>
  </div>
</template>

<script>
import Table from "./components/Table.vue"
import ColumnSelector from "./components/ColumnSelector.vue"

const API_URL = `http://localhost:5000/`

export default {
  components: {
    Table,
    ColumnSelector,
  },
  data() {
    return {
      metrics: {},
      sensors: {}
    }
  },
  // Adding a new field to all metrics to know if they have to be shown or not
  created() {
    this.fetchData().then(() => {
      for (let key in this.metrics) {
        this.metrics[key]["enabled"] = true;
      }
    });
  },
  methods: {
    async fetchData() {
      this.sensors = await this.getJson("sensors.json");
      this.metrics = await this.getJson("metrics.json");
    },

    async getJson(endpoint) {
      const url = API_URL + endpoint;
      const response = await fetch(url);
      return response.json();
    }
  }
}
</script>

