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
    <tr  v-for="data in table_data">
      <td>
        {{ data.account_type }}
      </td>
      <td>
        {{ data.customers_cid }}
      </td>
      <td>
        {{ data.customers_date_added }}
      </td>
      <td>
        {{ data.customers_default_address_id }}
      </td>
      <td>
        {{ data.customers_dob }}
      </td>
      <td>
        {{ data.customers_email_address }}
      </td>
      <td>
        {{ data.customers_fax }}
      </td>
      <td>
        {{ data.customers_fid }}
      </td>
      <td>
        {{ data.customers_firstname }}
      </td>
      <td>
        {{ data.customers_gender }}
      </td>
      <td>
        {{ data.customers_id }}
      </td>
      <td>
        {{ data.customers_last_modified }}
      </td>
      <td>
        {{ data.customers_lastname }}
      </td>
      <td>
        {{ data.customers_newsletter }}
      </td>
      <td>
        {{ data.customers_newsletter_mode }}
      </td>
      <td>
        {{ data.customers_password }}
      </td>
      <td>
        {{ data.customers_personal_discount }}
      </td>
      <td>
        {{ data.customers_secondname }}
      </td>
      <td>
        {{ data.customers_sid }}
      </td>
      <td>
        {{ data.customers_status }}
      </td>
      <td>
        {{ data.customers_telephone }}
      </td>
      <td>
        {{ data.customers_username }}
      </td>
      <td>
        {{ data.customers_vat_id }}
      </td>
      <td>
        {{ data.customers_vat_id_status }}
      </td>
      <td>
        {{ data.customers_warning }}
      </td>
      <td>
        {{ data.delete_user}}
      </td>
      <td>
        {{ data.login_reference}}
      </td>
      <td>
        {{ data.login_time}}
      </td>
      <td>
        {{ data.login_tries}}
      </td>
      <td>
        {{ data.member_flag}}
      </td>
      <td>
        {{ data.orig_reference}}
      </td>
      <td>
        {{ data.password_request_key}}
      </td>
      <td>
        {{ data.payment_unallowed}}
      </td>
      <td>
        {{ data.refferers_id}}
      </td>
      <td>
        {{ data.shipping_unallowed}}
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
                console.log(element[key], key)
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