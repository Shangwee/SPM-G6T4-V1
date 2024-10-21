<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&icon_names=notifications_active"
  />
  <div class="meeting-section" v-if="date == selectedDate">
    <span class="material-symbols-outlined icon">notifications_active</span>
    {{ meeting.Title }}
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      meeting: {},
      date: "",
      reportingManger: null,
    };
  },
  props: ["staffId", "selectedDate"],
  watch: {
    selectedDate(newDate, oldDate) {
      this.getMeeting();
    },
  },
  methods: {
    getMeeting() {
      let url = "http://localhost:5004/meeting";
      let params = {
        Date: this.selectedDate,
      };
      return axios
        .get(url, { params })
        .then((r) => {
          this.meeting = r.data[0];
          console.log(JSON.stringify(r.data[0]));
          if (
            r.data[0].meetingstaffs.some(
              (staff) => String(staff.Staff_ID) === this.staffId
            )
          ) {
            const date = new Date(r.data[0].Date);
            const formattedDate = `${date.getFullYear()}-${String(
              date.getMonth() + 1
            ).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
            this.date = formattedDate;
          }
        })
        .catch((e) => {
          this.date = "";
          this.meeting = {};
          console.log(e);
        });
    },
    getReportingManger() {
      return axios
        .get(`http://localhost:5001/user/${this.staffId}`)
        .then((response) => {
          this.reportingManager = response.data.Reporting_Manager;
        })
        .catch((error) => {
          console.error("Error fetching Reporting Manager:", error);
        });
    },
  },
  created() {
    this.getReportingManger();
    console.log("reporntingmanager" + this.reportingManager);
    this.getMeeting();
  },
  mounted() {},
};
</script>

<style scoped>
.meeting-section {
  padding: 16px;
  margin: 16px 16px;
  border-radius: 8px;
  background-color: #ffc494;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon {
  margin: 0px 8px;
}
</style>
