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
    <tr v-for="data in table_data">
      <td v-for="value in Object.values(data)">
        {{ value }}
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
            this.table_data = res.data
            for (let element of res.data) {
              for (let key of Object.keys(element)) {
                if (String(element[key]).includes('0000-00-00')) {
                  element[key] = '1970-01-01 00:00:00'
                }
                if (element[key].length === 0) {
                  element[key] = 'None data'
                }
              }
            }
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