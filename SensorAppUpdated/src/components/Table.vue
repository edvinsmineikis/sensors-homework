<template>
  <v-spacer></v-spacer>
  <v-text-field v-model="search" append-icon="mdi-magnify" label="Search for anything" single-line hide-details></v-text-field>
  <v-data-table :headers="tableHeaders" :items="tableData" :search="search">
  </v-data-table>
</template>

<script>

export default {
  props: {
    headersData: {
      type: Array,
      required: true
    },
    sensorData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      search: "",
      sortBy: "id",
      sortDesc: false
    }
  },
  computed: {
    tableHeaders() {
      let tableHeaders = [];
      tableHeaders.push({
        title: "Sensor name",
        align: "start",
        sortable: true,
        key: "name"
      })
      tableHeaders.push({
        title: "Sensor type ",
        align: "start",
        sortable: true,
        key: "typeName"
      })
      for (let header in this.headersData) {
        if (this.headersData[header]["enabled"] == true) {
          tableHeaders.push({
            title: this.headersData[header]["name"] + ", " + this.headersData[header]["unit"],
            align: "start",
            sortable: true,
            key: this.headersData[header]["name"]
          })
        }
      }
      return tableHeaders;
    },
    tableData() {
      let tableData = []
      for (let sensor in this.sensorData) {
        let data = {};
        data["name"] = this.sensorData[sensor]["name"];
        data["typeName"] = this.sensorData[sensor]["typeName"];
        for (let key in this.sensorData[sensor]["metrics"]) {
          data[key] = this.sensorData[sensor]["metrics"][key];
        }
        tableData.push(data);
      }
      return tableData;
    }
  },
}
</script>
