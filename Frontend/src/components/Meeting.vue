<template>
  <link
    rel="stylesheet"
    href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0"
  />
  <div class="meeting-row" v-if="date == selectedDate">
    <div class="meeting-section meeting">
      <span class="material-symbols-outlined"> calendar_month </span>
      {{ meeting.Title }}
    </div>
    <div
      class="delete"
      v-if="meeting.Created_By == this.staffId"
      @click="deleteMeeting"
    >
      <span class="material-symbols-outlined"> delete </span>
    </div>
  </div>

  <div v-if="date != selectedDate && team.length > 0">
    <div class="meeting-section button" @click="showTeam = !showTeam">
      <span class="material-symbols-outlined"> calendar_add_on </span>
      Create a Meeting
    </div>
    <div class="staff-list" v-show="showTeam">
      <div class="title">Select Staff</div>
      <table>
        <tr>
          <th><input type="checkbox" class="checkbox" @click="checkAll" /></th>
          <th>Staff_ID</th>
          <th>Name</th>
        </tr>
        <tr v-for="staff in team">
          <td>
            <input
              type="checkbox"
              class="checkbox"
              @change="updateSelectedStaff(staff.Staff_ID)"
            />
          </td>
          <td>
            {{ staff.Staff_ID }}
          </td>
          <td>
            {{ staff.Staff_FName }}
            {{ staff.Staff_LName }}
          </td>
        </tr>
      </table>
      <div class="align-row">
        <input
          type="text"
          placeholder="Enter meeting title.."
          v-model="title"
        />
      </div>
      <div class="align-row">
        <div>
          Meeting Date: <span class="date">{{ selectedDate }}</span>
        </div>
        <div class="create-btn button" @click="createMeeting">Create</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const ACCOUNT_API = import.meta.env.VITE_ACCOUNT_API;
const SCHEDULE_API = import.meta.env.VITE_SCHEDULE_API;
const REQUEST_API = import.meta.env.VITE_REQUEST_API;
const MEETING_API = import.meta.env.VITE_MEETING_API;
const NOTIFICATION_API = import.meta.env.VITE_NOTIFICATION_API;

export default {
  data() {
    return {
      meeting: {},
      date: "",
      reportingManager: null,
      userRole: null,
      team: [],
      showTeam: false,
      selectedStaff: [],
      checked: false,
      title: "",
      cell: null,
    };
  },
  props: ["staffId", "selectedDate", "selectedDay", "daysInMonth"],
  watch: {
    selectedDate(newDate, oldDate) {
      this.getMeeting();
      this.showTeam = false;
      this.selectedStaff = [];
      const checkboxes = document.querySelectorAll(".checkbox");
      checkboxes.forEach((checkbox) => {
        checkbox.checked = false; // Uncheck each checkbox
      });
    },
  },
  methods: {
    checkAll() {
      this.checked = !this.checked;
      const checkboxes = document.querySelectorAll(".checkbox");
      checkboxes.forEach((checkbox) => {
        checkbox.checked = this.checked;
      });
      if (this.checked == false) {
        this.selectedStaff = [];
        console.log(this.selectedStaff);
      } else {
        this.selectedStaff = [];
        for (let staff of this.team) {
          this.updateSelectedStaff(staff.Staff_ID);
        }
      }
    },
    updateSelectedStaff(id) {
      if (this.selectedStaff.includes(id)) {
        let index = this.selectedStaff.indexOf(id);
        if (index !== -1) {
          this.selectedStaff.splice(index, 1);
          console.log(this.selectedStaff);
        }
      } else {
        this.selectedStaff.push(id);
        console.log(this.selectedStaff);
      }
    },
    createMeeting() {
      let url = `${MEETING_API}/meeting`;
      let params = {
        Created_By: this.staffId,
        Date: this.selectedDate,
        Title: this.title,
      };

      return axios
        .post(url, params)
        .then((r) => {
          console.log(r.data);
          const meetingId = r.data.data.Meeting_ID;
          if (this.selectedStaff != []) {
            this.selectedStaff.push(parseInt(this.staffId));
            for (let staff of this.selectedStaff) {
              // send notification to all selected staffs
              let url = `${MEETING_API}/meetingstaffs`;
              let params = {
                Meeting_ID: parseInt(meetingId),
                Staff_ID: staff,
              };
              axios
                .post(url, params)
                .then((r) => {
                  console.log(r.data);
                })
                .catch((e) => {
                  console.log(e);
                });
              // Send notification to staff
              let notifiurl = `${NOTIFICATION_API}/api/notifications/create`;
              let notifiparams = {
                user_id: staff,
                message: `You have a meeting on ${this.selectedDate}`,
                notification_type: "meeting",
                request_id: null,
              };
              axios.post(notifiurl, notifiparams).then((r) => {
                console.log(r.data);
              });
            }
          }
          // this.getMeeting();
          // location.reload();
          this.cell =
            document.getElementsByClassName("calendar-cell")[
              this.daysInMonth.indexOf(this.selectedDay)
            ].classList;
          this.cell.add("meeting");
          this.$emit("getMyMeeting");
          this.getMeeting();
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getMeeting() {
      let url = `${MEETING_API}/meeting`;
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
    deleteMeeting() {
      let url = `${MEETING_API}/meeting/` + this.meeting.Meeting_ID;

      return axios
        .delete(url)
        .then((r) => {
          console.log(r.data);
          // TODO: send notification to all staffs that meeting is cancelled
          for (let staff of this.meeting.meetingstaffs) {
            let meetingstaffid = staff.Staff_ID;
            let notifiurl = `${NOTIFICATION_API}/api/notifications/create`;
            let notifiparams = {
              user_id: meetingstaffid,
              message: `Meeting have been cancelled on ${this.selectedDate}`,
              notification_type: "meeting",
              request_id: null,
            };
            axios.post(notifiurl, notifiparams).then((r) => {
              console.log(r.data);
            });
          }
          location.reload();
        })
        .catch((e) => {
          console.log(e);
        });
    },
    getReportingManager() {
      return axios
        .get(`${ACCOUNT_API}/user/${this.staffId}`)
        .then((response) => {
          this.reportingManager = response.data.Reporting_Manager;
          console.log("reporting Manager: " + this.reportingManager);
        })
        .catch((error) => {
          console.error("Error fetching Reporting Manager:", error);
        });
    },
    getUserRole() {
      return axios
        .get(`${ACCOUNT_API}/user/${this.staffId}`)
        .then((response) => {
          this.userRole = response.data.Role; // Set the userRole based on response
          console.log(this.userRole);
        })
        .catch((error) => {
          console.error("Failed to fetch user role:", error);
          throw error; // Re-throw the error to catch it in created()
        });
    },
    getTeam() {
      let params = {
        Reporting_Manager: this.staffId,
      };
      return axios
        .get(`${ACCOUNT_API}/users`, { params: params })
        .then((response) => {
          this.team = response.data; // Set the userRole based on response
          console.log("Team:" + JSON.stringify(this.team));
        })
        .catch((error) => {
          console.error("Failed to fetch user role:", error);
          throw error; // Re-throw the error to catch it in created()
        });
    },
  },
  created() {
    this.getUserRole();
    this.getReportingManager();
    this.getTeam();
    this.getMeeting();
  },
  mounted() {},
};
</script>

<style scoped>
.meeting-section {
  /* width: 100%; */
  flex-grow: 1;
  padding: 16px;
  margin: 16px 16px;
  border-radius: 8px;
  gap: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.meeting-row {
  display: flex;
  width: 100%;
}

.meeting {
  background-color: #ffc494;
  font-weight: bold;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.delete {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  margin: 16px 16px 16px 0px;
  border-radius: 8px;
  background-color: lightcoral;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.delete:hover {
  background-color: #ff5454;
  cursor: pointer;
}

.button {
  background-color: lightblue;
  font-weight: bold;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.button:hover {
  background-color: lightcyan;
  cursor: pointer;
}

.staff-list {
  padding: 16px;
  margin: 16px 16px;
  border-radius: 8px;
  gap: 16px;
  /* display: flex;
  align-items: center;
  justify-content: center; */
  background-color: white;
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}

.staff-list .title {
  font-weight: bold;
  margin: 16px 0px;
}

.align-row {
  margin: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.staff-list .align-row .date {
  font-weight: bold;
}

.staff-list .align-row input[type="text"] {
  width: 100%;
  box-sizing: border-box;
  border: 2px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  background-color: white;
  background-position: 10px 10px;
  background-repeat: no-repeat;
  padding: 12px 20px 12px 40px;
}

.staff-list .create-btn {
  border-radius: 8px;
  padding: 8px;
}

.icon {
  margin: 0px 8px;
}

table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
}

th {
  font-weight: bold;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 4px;
}
</style>
