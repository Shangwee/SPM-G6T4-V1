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
        <div class="calendar-day fw-bold text-center" v-for="day in daysOfWeek" :key="day">{{ day }}</div>
        <div v-for="(day, index) in daysInMonth" :key="index" class="calendar-cell text-center"
          @click.stop="selectDay(day)" :class="{
            'empty-day': day === '',
            'selected-day': day === selectedDay,
            'today': isToday(day)
          }">
          <span v-if="day">{{ day }}</span>
        </div>
      </div>
    </div>

    <div v-if="scheduleType === 'team'" class="staff-schedule-container">
      <div class="filter-controls d-flex flex-column mb-4">
        <div class="filter-controls d-flex mb-4">
          <div v-if="userRole === 1" class="form-group mr-2" style="flex: 1;">
            <label for="department">Department</label>
            <select id="department" v-model="selectedDepartment" class="form-control" @change="filterByDepartment">
              <option value="">All Departments</option>
              <option v-for="department in departments" :key="department" :value="department">{{ department }}</option>
            </select>
          </div>
          <div v-if="userRole === 3 || userRole === 1" class="form-group" :class="{'full-width': userRole === 3}" style="flex: 1;">
            <label for="team">Team</label>
            <select id="team" v-model="selectedTeam" class="form-control" @change="filterByTeam">
              <option value="">All Teams</option>
              <option v-for="team in teams" :key="team" :value="team">{{ team }}</option>
            </select>
          </div>
        </div>

        <div v-if="selectedDay && (userRole === 3 || userRole === 1)" class="staff-schedule mt-4">
          <h5 class="schedule-title">Staff Schedule for {{ selectedDay }} {{ currentMonthName }}, {{ currentYear }}</h5>
          <div class="row">
            <div class="col-md-6 mb-3 full-width">
              <div class="card home-card">
                <h6>Working from Home</h6>
                <ul class="staff-list">
                  <li v-if="userRole === 2" v-for="staff in homeStaff" :key="staff.id">
                    {{ staff.Staff_FName }} {{ staff.Staff_LName }} ({{ staff.Staff_ID }})
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from "axios";

export default {
  // setup() {
  //   const userRole = ref(null);
  //   const staffID = ref(null);

  //   const fetchUserRole = async () => {
  //     try {
  //       staffID.value = JSON.parse(sessionStorage.getItem('staffID'));
  //       const response = await fetch(`http://localhost:5001/user/${staffID.value}`, {
  //         method: 'GET',
  //         headers: { 'Content-Type': 'application/json' },
  //       });

  //       const data = await response.json();
  //       userRole.value = data.Role;
  //     } catch (error) {
  //       console.error('Failed to fetch user role:', error);
  //     }
  //   };

  //   onMounted(() => {
  //     fetchUserRole();
  //   });

  //   return { userRole, staffID };
  // },

  data() {
    return {
      currentDate: new Date(),
      selectedDay: null,
      staffId: null,
      reportingManager: null,
      userRole: null,
      ownSchedule: [],
      scheduleStaff: [],
      scheduleManage: [],
      homeStaff: [],
      teams: [],
      staff: [],
      selectedDepartment: '',
      selectedTeam: '',
      scheduleType: '', // Define this according to your application logic
    };
  },
  
  props: {
    scheduleType: {
      type: String,
      required: true,
      validator: value => ['user', 'team'].includes(value),
    },
  },

  async created() {
  this.staffId = sessionStorage.getItem('staffID'); // Retrieve Staff_ID

  if (this.staffId) {
    try {
      await this.fetchUserRole(); // Wait for user role to be fetched
      this.fetchOwnSchedule(); 
      this.selectToday(); // Automatically select today's date
      this.fetchReportingManager(); // Fetch Reporting_Manager for the logged-in staff
      
      // Wait for reportingManager to be set before checking userRole
      if (this.userRole === 2) {
        console.log("Fetching staff team schedule for user role 2");
        await this.fetchStaffTeamSchedule();
      } else {
        await this.fetchManageTeamSchedule();
      }
    } catch (error) {
      console.error("Error in created lifecycle:", error);
    }
  } else {
    console.error("No Staff ID found.");
  }
},

  computed: {
    currentYear() {
      return this.currentDate.getFullYear();
    },
    currentMonth() {
      return this.currentDate.getMonth();
    },
    currentMonthName() {
      return this.currentDate.toLocaleString('default', { month: 'long' });
    },
    daysOfWeek() {
      return ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    },
    daysInMonth() {
      const days = [];
      const firstDay = new Date(this.currentYear, this.currentMonth, 1).getDay();
      const lastDate = new Date(this.currentYear, this.currentMonth + 1, 0).getDate();

      for (let i = 0; i < firstDay; i++) {
        days.push('');
      }

      for (let day = 1; day <= lastDate; day++) {
        days.push(day);
      }

      return days;
    },
  },

  methods: {
    fetchUserRole() {
    return axios.get(`http://localhost:5001/user/${this.staffId}`)
      .then(response => {
        this.userRole = response.data.Role; // Set the userRole based on response
      })
      .catch(error => {
        console.error("Failed to fetch user role:", error);
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
      this.homeStaff = [];
      this.scheduleStaff.forEach((schedule) => {
        axios
          .get(`http://localhost:5001/user/${schedule.Staff_ID}`)
          .then((response) => {
            this.homeStaff.push(response.data);
            // get all teams
            if (!this.teams.includes(response.data.Position)) {
              this.teams.push(response.data.Position);
            }
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
          this.fetchStaffTeamSchedule();
        })
        .catch((error) => {
          console.error("Error fetching Reporting Manager:", error);
        });
    },
    fetchStaffTeamSchedule() {
      let params = {
        type: "Team",
        Reporting_Manager: this.reportingManager,
        start_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()}`,
        end_date: `${this.currentYear}-${this.currentMonth + 1}-${this.selectedDay || this.currentDate.getDate()}`,
      };

      axios
        .get(`http://localhost:6003/aggregateSchedule`, { params: params })
        .then((response) => {
          this.scheduleStaff = response.data;
          this.fetchStaffTeamMembers();
        })
        .catch((error) => {
          console.error("Error fetching team schedule:", error);
        });
    },

    fetchManageTeamMembers() {
        this.scheduleManage.forEach((schedule) => {
          axios
            .get(`http://localhost:5001/user/${schedule.Staff_ID}`)
            .then((response) => {
              this.staff.push(response.data);
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
    
    fetchManageTeamSchedule() {
        let params = {
          type: "Team",
          Reporting_Manager: this.staffId,
          start_date: `${this.currentDate.getFullYear()}-${
            this.currentDate.getMonth() + 1
          }-${this.currentDate.getDate()}`,
          end_date: `${this.currentDate.getFullYear()}-${
            this.currentDate.getMonth() + 1
          }-${this.currentDate.getDate()}`,
        };
        
        axios .get(`http://localhost:6003/aggregateSchedule`, { params: params })
        .then((response) => {
          this.scheduleManage = response.data;
          this.fetchManageTeamMembers();
        })
        .catch((error) => {
          console.error("Error fetching team schedule:", error);
        });
      },

    selectDay(day) {
      if (this.selectedDay === day) {
        this.selectedDay = null; // Deselect if the day is already selected
      } else {
        this.selectedDay = day; // Select the new day
      }
      this.fetchReportingManager();
      this.fetchManageTeamSchedule();
    },
    
    deselectDay() {
      this.selectedDay = null; // Deselect day
    },
    
    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
      this.selectedDay = null; // Deselect day when month changes
    },
    
    previousMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
      this.selectedDay = null; // Deselect day when month changes
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
    },
  },
};
</script>

<style scoped>
.full-width {
  width: 100%; /* Expand to full width */
}

.filter-controls.full-width {
  justify-content: flex-start; /* Prevent misalignment */
}

.filter-controls .form-group.full-width {
  width: 100%; /* Ensure full width for form-group */
}

.filter-controls select {
  width: 100%; /* Ensure select element is also full width */
}
.calendar-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 70vh;
  padding-bottom: 0;
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
</style>
