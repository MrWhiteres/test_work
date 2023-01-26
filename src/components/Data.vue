<template>
  <table class="table table-bordered table-striped">
    <thead>
    <tr>
      <th
          v-for="head in tableHead"
          :key="head"
      >
        {{ head }}
      </th>
    </tr>
    </thead>
    <tbody>
    <tr>
      <td
          v-for="data in table_data"
          :key="data"
      >
        {{ data }}
      </td>
    </tr>
    </tbody>
  </table>

</template>

<script>
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import axios from "axios";

export default {
  name: "Data",
  data() {
    return {
      table_data: [],
      tableHead: []
    }
  },
  methods: {
    getData() {
      const path = 'http://127.0.0.1:5000/'
      axios.get(path)
          .then((res) => {
            this.tableHead = Object.keys(res.data[0])
            let dataTable = {}
            for (let key of Object.keys(res.data[0])) {
              dataTable[key] = []
            }
            for (let data of res.data) {
              for (let key of Object.keys(data)) {
                console.log(data[key])
                dataTable[key].push(data[key])
              }
            }
            this.table_data = dataTable
          })
          .catch((error) => {
            console.error(error)
          })
    }
  },
  created() {
    this.getData()
  }
}
</script>

<style scoped>

</style>