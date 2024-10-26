<template>
  <div class="calendar-container">
    <div class="calendar card shadow-sm" @click="deselectDay">
      <div class="calendar-header d-flex justify-content-between align-items-center p-3">
        <button class="btn btn-outline-primary" @click.stop="previousMonth">
          <i class="bi bi-arrow-left-circle"></i> Previous
        </button>
        <h4 class="m-0">{{ currentMonthName }} {{ currentYear }}</h4>
        <button class="btn btn-outline-primary" @click.stop="nextMonth">
          Next <i class="bi bi-arrow-right-circle"></i>
        </button>
      </div>
      <div class="calendar-grid p-2">
        <div class="calendar-day fw-bold text-center" v-for="day in daysOfWeek" :key="day">
          {{ day }}
        </div>
        <div v-for="day of daysInMonth" class="calendar-cell text-center" @click.stop="
          selectDay(day);
        filteredStaffWorkingFromHome = [];
        " :class="{
          'empty-day': day === '',
          'selected-day': day === selectedDay,
          today: isToday(day),
          active: this.ownSchedule.some((e) => {
            const scheduleDate = new Date(e.Date);
            const currentDay = new Date(
              this.currentDate.getFullYear(),
              this.currentDate.getMonth(),
              day
            );
            return (
              scheduleDate.getFullYear() === currentDay.getFullYear() &&
              scheduleDate.getMonth() === currentDay.getMonth() &&
              scheduleDate.getDate() === currentDay.getDate()
            );
          }),
          meeting: this.myMeetings.some((meeting) => {
            const meetingDate = new Date(meeting.Date);
            const currentDay = new Date(
              this.currentDate.getFullYear(),
              this.currentDate.getMonth(),
              day
            );

            return (
              meeting.meetingstaffs.some(
                (staff) => String(staff.Staff_ID) === this.staffId
              ) &&
              meetingDate.getFullYear() === currentDay.getFullYear() &&
              meetingDate.getMonth() === currentDay.getMonth() &&
              meetingDate.getDate() === currentDay.getDate()
            );
          }),
          // conflict:
          //   this.ownSchedule.some((e) => {
          //     const scheduleDate = new Date(e.Date);
          //     const currentDay = new Date(
          //       this.currentDate.getFullYear(),
          //       this.currentDate.getMonth(),
          //       day
          //     );
          //     return (
          //       scheduleDate.getFullYear() === currentDay.getFullYear() &&
          //       scheduleDate.getMonth() === currentDay.getMonth() &&
          //       scheduleDate.getDate() === currentDay.getDate()
          //     );
          //   }) &&
          //   this.myMeetings.some((meeting) => {
          //     const meetingDate = new Date(meeting.Date);
          //     const currentDay = new Date(
          //       this.currentDate.getFullYear(),
          //       this.currentDate.getMonth(),
          //       day
          //     );

          //     return (
          //       meeting.meetingstaffs.some(
          //         (staff) => String(staff.Staff_ID) === this.staffId
          //       ) &&
          //       meetingDate.getFullYear() === currentDay.getFullYear() &&
          //       meetingDate.getMonth() === currentDay.getMonth() &&
          //       meetingDate.getDate() === currentDay.getDate()
          //     );
          //   }),
        }">
          <span v-if="day">{{ day }}</span>
        </div>
      </div>
      <!-- Legend -->
      <div v-if="scheduleType === 'team'" class="legend">
        <div class="legend-item">
          <div class="wfh-color"></div>
          <span class="legend-text">Personal WFH</span>
        </div>
        <div class="legend-item">
          <div class="meeting-color"></div>
          <span class="legend-text">Team Meeting</span>
        </div>
        <!-- <div class="legend-item">
          <div class="conflict-color"></div>
          <span class="legend-text">Schedule Conflict</span>
        </div> -->
      </div>
    </div>

    <!-- Team or personal schedule section -->
    <div v-if="scheduleType === 'team'" class="staff-schedule-container">
      <Meeting :staffId="staffId" :selectedDate="selectedDate"></Meeting>
      <div class="filter-controls d-flex flex-column mb-4">
        <div v-if="userRole === 3 || userRole === 1" class="filter-controls d-flex mb-4">
          <div class="form-group mr-2" style="flex: 1;">
            <label for="department">Department</label>
            <select id="department" v-model="selectedDepartment" class="form-control" @change="filterByDepartment">
              <option value="">Select Department</option>
              <option v-for="department in depts" :key="department" :value="department">
                {{ department }}
              </option>
            </select>
          </div>

          <div class="form-group" style="flex: 1;">
            <label for="team">Team</label>
            <select id="team" v-model="selectedTeam" class="form-control" @change="filterByTeam">
              <option value="">Select Teams</option>
              <option v-for="team in teams" :key="team" :value="team">
                {{ team }}
              </option>
            </select>
          </div>
        </div>


        <div v-show="selectedDay" class="staff-schedule mt-4">
          <h5 class="schedule-title">
            Staff Schedule for {{ selectedDay }} {{ currentMonthName }},
            {{ currentYear }}
          </h5>
        </div>

        <!-- Team members list -->
        <div class="row" v-if="schedule.length > 0">
          <div class="col-md-6 mb-3 full-width">
            <div class="card home-card">
              <h6>Working from Home</h6>
              <ul class="staff-list">
                <div v-if="userRole === 2">
                  <li v-for="staff in filteredStaffWorkingFromHome" :key="staff.id">
                    {{ staff.Staff_FName }} {{ staff.Staff_LName }} ({{
                      staff.Staff_ID
                    }})
                  </li>
                </div>
                <div v-if="userRole === 3">
                  <li v-for="staff in filteredStaffWorkingFromHome" :key="staff.id">
                    {{ staff.Staff_FName }} {{ staff.Staff_LName }} ({{
                      staff.Staff_ID
                    }}) - {{ staff.Position }}
                  </li>
                </div>
                <div v-if="userRole === 1">
                  <li v-for="staff in filteredStaffWorkingFromHome">
                    {{ staff.Staff_FName }} {{ staff.Staff_LName }} ({{
                      staff.Staff_ID
                    }}) - {{ staff.Position }}
                  </li>
                </div>
              </ul>
            </div>
            <div>
              <h6>Users Not in Schedule</h6>
              <ul>
                <li v-for="user in usersNotInSchedule" :key="user.id">{{ user.Staff_FName }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Meeting from "./Meeting.vue";

export default {
  components: {
    Meeting,
  },
  data() {
    return {
      currentDate: new Date(),
      selectedDay: null,
      staffId: null,
      reportingManager: null,
      userRole: null,
      userDept: null,
      ownSchedule: [],
      schedule: [],
      staffs: [],
      teams: [],
      depts: [],
      scheduleDept: [],
      staffsDept: [],
      selectedDepartment: "",
      selectedTeam: "",
      // scheduleType: "", // Define this according to your application logic
      // selectedFilter: 'Personal Team',
      // filter: ['Personal Team', 'Personal Department'],
      filteredStaffWorkingFromHome: [],
      selectedDate: "",
      myMeetings: [],

      allUsers: [], // Array to hold all users
      scheduledUsers: [], // Array to hold scheduled users
      usersNotInSchedule: [], // Array to hold users not in schedule
    };
  },

  props: {
    scheduleType: {
      type: String,
      required: true,
      validator: (value) => ["user", "team"].includes(value),
    },
  },

  async created() {
    this.staffId = sessionStorage.getItem("staffID"); // Retrieve Staff_ID
    // this.fetchReportingManager();

    if (this.staffId) {
      try {
        this.fetchAllUsers();
        this.fetchUserRole(); // Wait for user role to be fetched
        this.fetchUserDept();
        this.fetchOwnSchedule();
        this.selectToday(); // Automatically select today's date
        this.filterStaff();
        this.fetchReportingManager(); // Fetch Reporting_Manager for the logged-in staff

        this.getMeetings();

        // Wait for reportingManager to be set before checking userRole
        if (this.userRole === 2) {
          console.log("Fetching staff team schedule for user role 2");
          this.fetchStaffTeamSchedule();
        } else if (this.userRole === 3) {
          this.fetchbyOwnDept();
          this.fetchManageTeamSchedule();
        } else if (this.userRole === 1) {
          // this.fetchbyOwnDept();
          this.fetchALLSchedule();
        }
      } catch (error) {
        console.error("Error in created lifecycle:", error);
      }
    } else {
      console.error("No Staff ID found.");
    }
  },

  watch: {
    schedule(newSchedule, oldSchedule) {
      // this.schedule = [];
      // this.fetchAllMembers();
      if (this.schedule == []) {
        this.filteredStaffWorkingFromHome = [];
      } else {
        this.fetchStaffTeamMembers();
      }
    },
  },

  

  computed: {
    currentYear() {
      return this.currentDate.getFullYear();
    },
    currentMonth() {
      return this.currentDate.getMonth();
    },
    currentMonthName() {
      return this.currentDate.toLocaleString("default", { month: "long" });
    },
    daysOfWeek() {
      return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    },
    daysInMonth() {
      const days = [];
      const firstDay = new Date(
        this.currentYear,
        this.currentMonth,
        1
      ).getDay();
      const lastDate = new Date(
        this.currentYear,
        this.currentMonth + 1,
        0
      ).getDate();

      for (let i = 0; i < firstDay; i++) {
        days.push("");
      }

      for (let day = 1; day <= lastDate; day++) {
        days.push(day);
      }

      return days;
    },
  },
  
  methods: {
    mounted() {
      this.fetchAllUsers();
    },

    async fetchAllUsers() {
      try {
        const response = await axios.get("http://localhost:5001/users"); // Adjust the endpoint as necessary
        this.allUsers = response.data; // Assuming the response is an array of users
      } catch (error) {
        console.error("Error fetching all users:", error);
      }
    },

    fetchUsersNotInSchedule() {
      const scheduleDates = this.schedule.map((s) => new Date(s.Date).toDateString());
      console.log("asfasfasfa");
      this.usersNotInSchedule = this.allUsers.filter((user) => {
        const userDate = new Date(user.date).toDateString();
        return !scheduleDates.includes(userDate);
      });
    },

    getMeetings() {
      let url = "http://localhost:5004/meeting";
      let params = {
        // Created_By: this.reportingManager,
      };
      return axios
        .get(url, { params })
        .then((r) => {
          this.myMeetings = r.data;
        })
        .catch((e) => {
          console.log(e);
        });
    },
    fetchUserRole() {
      return axios
        .get(`http://localhost:5001/user/${this.staffId}`)
        .then((response) => {
          this.userRole = response.data.Role; // Set the userRole based on response
        })
        .catch((error) => {
          console.error("Failed to fetch user role:", error);
          throw error; // Re-throw the error to catch it in created()
        });
    },
    fetchUserDept() {
      return axios
        .get(`http://localhost:5001/user/${this.staffId}`)
        .then((response) => {
          this.userDept = response.data.Dept; // Set the userRole based on response
        })
        .catch((error) => {
          console.error("Failed to fetch user dept:", error);
          throw error; // Re-throw the error to catch it in created()
        });
    },
    fetchOwnSchedule() {
      axios
        .get(`http://localhost:5002/schedule/personal/${this.staffId}`)
        .then((response) => {
          console.log(response.data);
          this.ownSchedule = response.data;
        })
        .catch((error) => {
          console.error("Error fetching own Schedule:", error);
        });
    },

    fetchStaffTeamMembers() {
      this.staffs = [];
      this.schedule.forEach((schedule) => {
        axios
          .get(`http://localhost:5001/user/${schedule.Staff_ID}`)
          .then((response) => {
            this.staffs.push(response.data);
            // get all teams
            if (!this.teams.includes(response.data.Position)) {
              this.teams.push(response.data.Position);
            }
            this.filterStaff();
          })
          .catch((error) => {
            console.error("Error fetching Team Members info", error);
          });
      });
    },
    fetchReportingManager() {
      axios
        .get(`http://localhost:5001/user/${this.staffId}`)
        .then((response) => {
          this.reportingManager = response.data.Reporting_Manager;
          // this.fetchStaffTeamSchedule();
        })
        .catch((error) => {
          console.error("Error fetching Reporting Manager:", error);
        });
    },
    fetchStaffTeamSchedule() {
      try {
        const params = {
          type: "Team",
          // staffId: sessionStorage.getItem('staffID'),
          reporting_manager: this.reportingManager,
          start_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()
            }`,
          end_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()
            }`,
        };

        axios
          .get(`http://localhost:6003/aggregateSchedule`, {
            params,
          })
          .then((response) => {
            this.schedule = response.data;
            // this.fetchStaffTeamMembers(); // ** running before this.schedule retrieves
          });
          this.filterUsersNotInSchedule();
      } catch (error) {
        this.schedule = [];
        console.error("Error fetching team schedule:", error);
      }
    },

    fetchManageTeamMembers() {
      this.staffs = [];
      this.schedule.forEach((schedule) => {
        axios
          .get(`http://localhost:5001/user/${schedule.Staff_ID}`)
          .then((response) => {
            this.staffs.push(response.data);
            // get all teams
            if (!this.teams.includes(response.data.Position)) {
              this.teams.push(response.data.Position);
            }
          })
          .catch((error) => {
            console.error("Error fetching Reporting Manager:", error);
          });
        console.log(this.staffs);
      });
    },

    async fetchManageTeamSchedule() {
      try {
        const params = {
          type: "Team",
          // staffId: sessionStorage.getItem('staffID'),
          reporting_manager: parseInt(this.staffId, 10),
          start_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()
            }`,
          end_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()
            }`,
        };

        axios
          .get(`http://localhost:6003/aggregateSchedule`, {
            params,
          })
          .then((response) => {
            this.schedule = response.data;
            // this.fetchStaffTeamMembers(); // ** running before this.schedule retrieves
          });
      } catch (error) {
        this.schedule = [];
        console.error("Error fetching team schedule:", error);
      }
    },

    fetchbyOwnDept() {
      let params = {
        type: "Dept",
        dept: this.userDept,
        start_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()
          }`,
        end_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()
          }`,
      };
      axios
        .get(`http://localhost:6003/aggregateSchedule`, { params: params })
        .then((response) => {
          this.scheduleDept = response.data;
          this.fetchManageDeptMembers();
        })
        .catch((error) => {
          console.error("Error fetching team schedule:", error);
        });
    },

    fetchManageDeptMembers() {
      this.staffsDept = [];
      this.scheduleDept.forEach((schedule) => {
        axios
          .get(`http://localhost:5001/user/${schedule.Staff_ID}`)
          .then((response) => {
            this.staffsDept.push(response.data);
            // get all depts
            if (!this.depts.includes(response.data.Dept)) {
              this.depts.push(response.data.Dept);
            }
          })
          .catch((error) => {
            console.error("Error fetching Reporting Manager:", error);
          });
        // console.log(this.staffsDept);
      });
    },

    filterByDepartment() {
      this.filterStaff();
    },
    filterByTeam() {
      this.filterStaff();
    },
    filterStaff() {
      // Filter staff based on selected department and team
      this.filteredStaffWorkingFromHome = this.staffs.filter((staff) => {
        return (
          (!this.selectedDepartment ||
            staff.Dept === this.selectedDepartment) &&
          (!this.selectedTeam || staff.Position === this.selectedTeam)
        );
      });
    },

    fetchAllMembers() {
      this.staffs = [];
      this.schedule.forEach((schedule) => {
        axios
          .get(`http://localhost:5001/user/${schedule.Staff_ID}`)
          .then((response) => {
            this.staffs.push(response.data);
            // get all teams
            if (!this.teams.includes(response.data.Position)) {
              this.teams.push(response.data.Position);
            }
          })
          .catch((error) => {
            console.error("Error fetching Reporting Manager:", error);
          });
      });
    },

    async fetchALLSchedule() {
      try {
        const params = {
          type: "All",
          staff_id: parseInt(this.staffId, 10), // Ensures staff_id is parsed as an integer
          start_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()}`,
          end_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()}`,
        };

        const response = await axios.get(`http://localhost:6003/aggregateSchedule`, { params });

        this.schedule = response.data;
        // this.fetchAllMembers();
        this.staffsDept.push(response.data);

        for (const staff of response.data) {
          if (!this.teams.includes(staff.Position)) {
            this.teams.push(staff.Position);
          }
          if (!this.depts.includes(staff.Dept)) {
            this.depts.push(staff.Dept);
          }
        }

        console.log(this.depts);
      } catch (error) {
        this.schedule = [];
        console.error("Error fetching schedule:", error);
      }
    },


    selectDay(day) {
    if (this.selectedDay === day) {
      this.deselectDay(); // Call deselectDay if the same day is selected
    } else {
      this.deselectDay();

      // Reset filters and clear dropdown options when a new day is selected
      this.selectedDepartment = "";  // Reset department filter
      this.selectedTeam = "";        // Reset team filter
      this.depts = [];               // Clear department options
      this.teams = [];               // Clear team options

      this.filteredStaffWorkingFromHome = []; // Clear WFH staff list for the new day

      this.selectedDay = day; // Set the new day
      this.selectedDate = `${this.currentYear}-${this.currentMonth + 1}-${
        this.selectedDay.toString().length === 1
          ? "0" + this.selectedDay
          : this.selectedDay
      }`;

      // Only fetch or update schedule if the day has WFH requests
      this.fetchAllUsers();
      this.updateScheduleBasedOnRole();
      this.filterStaff(); // Reapply staff filtering logic
      this.fetchUsersNotInSchedule();

      // Log state for debugging
      console.log({
        userRole: this.userRole,
        staffId: this.staffId,
        selectedDay: this.selectedDay,
        schedule: this.schedule,
        filteredStaffWorkingFromHome: this.filteredStaffWorkingFromHome,
        depts: this.depts,
        teams: this.teams
      });
    }
  },

    deselectDay() {
      this.selectedDay = null; // Deselect day
      this.schedule = [];
      this.filteredStaffWorkingFromHome = [];
    },

    updateScheduleBasedOnRole() {
      // Fetch schedule based on user role
      if (this.userRole === 2) {
        // this.fetchReportingManager();
        this.fetchStaffTeamSchedule();
      } else if (this.userRole === 3) {
        this.fetchbyOwnDept();
        this.fetchManageTeamSchedule();
      } else if (this.userRole === 1) {
        // this.fetchbyOwnDept();
        this.fetchALLSchedule();
      }
    },

    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
      this.deselectDay(); // Deselect day when month changes
    },

    previousMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
      this.deselectDay(); // Deselect day when month changes
    },

    isToday(day) {
      const today = new Date();
      return (
        day === today.getDate() &&
        this.currentMonth === today.getMonth() &&
        this.currentYear === today.getFullYear()
      );
    },

    selectToday() {
      this.selectedDay = this.currentDate.getDate(); // Automatically select today
      this.selectedDate = `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay
        }`;
      this.filterStaff();
    },
  },
};
</script>

<style scoped>
.full-width {
  width: 100%;
  /* Expand to full width */
}

.filter-controls.full-width {
  justify-content: flex-start;
  /* Prevent misalignment */
}

.filter-controls .form-group.full-width {
  width: 100%;
  /* Ensure full width for form-group */
}

.filter-controls select {
  width: 100%;
  /* Ensure select element is also full width */
}

.calendar-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 70vh;
  padding-bottom: 0;
  overflow-y: auto;
}

.calendar {
  background-color: rgba(255, 255, 255, 0.9);
  width: 70%;
  /* Increased width from 58% to 65% */
  margin: 0 auto;
  border-radius: 8px;
  padding: 10px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 1px;
  width: 100%;
}

.calendar-cell {
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #e0e0e0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  background-color: white;
}

.calendar-cell.selected-day {
  background-color: #e2e3e5;
  color: #495057;
  font-weight: bold;
  border-radius: 8px;
  border: 2px solid #495057;
}

.calendar-cell.today {
  background-color: #d1e7ff;
  color: #0d6efd;
  font-weight: bold;
  border-radius: 8px;
  border: 1px solid #0d6efd;
}

.calendar-cell.active {
  background-color: #b6c6fd;
}

.calendar-cell.meeting {
  background-color: #ffc494;
}

.calendar-cell.conflict {
  background-color: #ff564a;
  color: white;
}

.calendar-cell.today.selected-day {
  background-color: #b6d4fe;
  color: #0d6efd;
  border: 2px solid #0d6efd;
}

.calendar-cell:hover {
  background-color: #f8f9fa;
  transition: background-color 0.3s ease;
}

.empty-day {
  background-color: #fafafa;
}

.staff-schedule-container {
  width: 70%;
  /* Increased width from 40% to 50% */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.filter-controls {
  display: flex;
  justify-content: space-between;
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

.filter-controls .form-group {
  width: 48%;
}

.filter-controls select {
  width: 100%;
  padding: 8px;
  font-size: 0.95rem;
  border-radius: 4px;
  border: 1px solid #ced4da;
}

/* Staff Schedule Styling */
.staff-schedule {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.schedule-title {
  font-weight: bold;
  text-align: center;
  font-size: 1.25rem;
  margin-bottom: 20px;
}

.card {
  flex-grow: 1;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.office-card h6,
.home-card h6 {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

/* Updated staff list to be more compact */
.staff-list {
  list-style-type: none;
  /* Removed bullet points */
  padding-left: 0;
  /* Removed extra padding */
  margin: 0;
}

.staff-item {
  font-size: 0.85rem;
  /* Reduced font size for compactness */
  padding: 3px 0;
  /* Reduced padding between list items */
  color: #555;
}

@media (max-width: 768px) {
  .calendar-container {
    flex-direction: column;
    height: auto;
  }

  .calendar,
  .staff-schedule-container {
    width: 100%;
    margin-bottom: 20px;
  }

  .calendar-cell {
    height: 60px;
  }

  .card {
    margin-bottom: 10px;
  }
}

@media (max-width: 576px) {
  .calendar-cell {
    height: 50px;
  }
}

.legend {
  display: flex;
  flex-direction: column;
}

.legend-item {
  display: flex;
  justify-content: center;
  align-items: center;
}

.legend .wfh-color {
  width: 20px;
  height: 20px;
  background-color: #b6c6fd;
}

.legend .meeting-color {
  width: 20px;
  height: 20px;
  background-color: #ffc494;
}

.legend .conflict-color {
  width: 20px;
  height: 20px;
  background-color: #ff564a;
}

.legend-text {
  margin: 8px 8px;
}
</style>
