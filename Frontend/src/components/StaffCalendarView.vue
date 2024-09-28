<template>
  <div class="calendar-container">
    <div class="calendar card shadow-sm" @click="deselectDay">
      <div
        class="calendar-header d-flex justify-content-between align-items-center p-3"
      >
        <button class="btn btn-outline-primary" @click.stop="previousMonth">
          <i class="bi bi-arrow-left-circle"></i> Previous
        </button>
        <h4 class="m-0">{{ currentMonthName }} {{ currentYear }}</h4>
        <button class="btn btn-outline-primary" @click.stop="nextMonth">
          Next <i class="bi bi-arrow-right-circle"></i>
        </button>
      </div>
      <div class="calendar-grid p-2">
        <div
          class="calendar-day fw-bold text-center"
          v-for="day in daysOfWeek"
          :key="day"
        >
          {{ day }}
        </div>
        <div
          v-for="(day, index) in daysInMonth"
          :key="index"
          class="calendar-cell text-center"
          @click.stop="selectDay(day)"
          :class="{
            'empty-day': day === '',
            'selected-day': day === selectedDay,
            today: isToday(day),
            active: this.ownSchedule.some((e) => {
              return (
                new Date(e.Date).toISOString().substring(0, 10) ==
                new Date(
                  this.currentDate.getFullYear(),
                  this.currentDate.getMonth(),
                  day + 1
                )
                  .toISOString()
                  .substring(0, 10)
              );
            }),
          }"
        >
          <span v-if="day">{{ day }}</span>
        </div>
      </div>
      <div class="legend">
        <div class="legend-item">
          <div class="wfh-color"></div>
          <span class="legend-text">WFH</span>
        </div>
      </div>
    </div>

    <!-- Section to show team schedule based on Reporting_Manager -->
    <div v-if="selectedDay" class="staff-schedule mt-4">
      <h5 class="schedule-title">
        Team Schedule for {{ selectedDay }} {{ currentMonthName }},
        {{ currentYear }}
      </h5>
      <div class="row">
        <!-- <div class="col-md-6">
          <div class="card office-card">
            <h6>In Office</h6>
            <ul>
              <li v-for="staff in officeStaff" :key="staff.id">
                {{ staff.name }}
              </li>
            </ul>
          </div>
        </div> -->
        <div class="col-md-6">
          <div class="card home-card">
            <h6>Working from Home</h6>
            <ul>
              <li v-for="staff in homeStaff" :key="staff.id">
                {{ staff.Staff_FName }}
                {{ staff.Staff_LName }} ({{ staff.Staff_ID }})
              </li>
            </ul>
          </div>
        </div>
        <!-- <div class="col-md-6">
          <div class="card office-card">
            <h6>My Upcoming Schedule</h6>
            <ul>
              <li v-for="staff in officeStaff" :key="staff.id">
                {{ staff.name }}
              </li>
            </ul>
          </div>
        </div> -->
      </div>
      <!-- <div class="col-md-6">
        <div class="card home-card">
          <div class="legend">
            Legend:
            <div class="legend-item">
              <div class="wfh-color"></div>
              <span class="legend-text">WFH</span>
            </div>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      currentDate: new Date(),
      selectedDay: null,
      staffId: null,
      reportingManager: null,
      ownSchedule: [],
      schedule: [],
      // officeStaff: [], // List of staff in the office
      homeStaff: [], // List of staff working from home
    };
  },
  created() {
    this.staffId = sessionStorage.getItem("staffID");

    if (this.staffId) {
      this.fetchOwnSchedule();
      this.fetchReportingManager(); // Fetch Reporting_Manager for the logged-in staff
    } else {
      console.error("No Staff ID found.");
    }

    this.selectToday(); // Automatically select today's date when the component is created
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
    fetchOwnSchedule() {
      axios
        .get(`http://localhost:5002/schedule/personal/${this.staffId}`)
        .then((response) => {
          console.log(response.data);
          this.ownSchedule = response.data;

          console.log(
            "check date: ",
            this.ownSchedule.some((e) => {
              console.log(
                new Date(e.Date).toISOString().substring(0, 10),
                "schedule"
              );
              console.log(
                new Date(
                  this.currentDate.getFullYear(),
                  this.currentDate.getMonth(),
                  28 + 1
                )
                  .toISOString()
                  .substring(0, 10)
              );
              return (
                new Date(e.Date).toISOString().substring(0, 10) ==
                new Date(
                  this.currentDate.getFullYear(),
                  this.currentDate.getMonth(),
                  28 + 1
                )
                  .toISOString()
                  .substring(0, 10)
              );
            })
          );
        })
        .catch((error) => {
          console.error("Error fetching own Schedule:", error);
        });
    },
    fetchTeamMembers() {
      // console.log(this.schedule);
      this.homeStaff = [];

      this.schedule.forEach((schedule) => {
        // console.log(schedule.Staff_ID);
        axios
          .get(`http://localhost:5001/user/${schedule.Staff_ID}`)
          .then((response) => {
            // console.log(response.data);
            this.homeStaff.push(response.data);
          })
          .catch((error) => {
            console.error("Error fetching Team Members info", error);
          });
      });
    },
    fetchReportingManager() {
      // console.log(this.staffId);
      axios
        .get(`http://localhost:5001/user/${this.staffId}`)
        .then((response) => {
          // console.log(response.data);
          this.reportingManager = response.data.Reporting_Manager;
          this.fetchTeamSchedule();
        })
        .catch((error) => {
          console.error("Error fetching Reporting Manager:", error);
        });
    },
    fetchTeamSchedule() {
      // console.log(
      //   `${this.currentDate.getFullYear()}-${
      //     this.currentDate.getMonth() + 1
      //   }-${this.currentDate.getDate()}`
      // );

      let params = {
        type: "Team",
        Reporting_Manager: this.reportingManager,
        start_date: `${this.currentDate.getFullYear()}-${
          this.currentDate.getMonth() + 1
        }-${this.currentDate.getDate()}`,
        end_date: `${this.currentDate.getFullYear()}-${
          this.currentDate.getMonth() + 1
        }-${this.currentDate.getDate()}`,
      };

      axios
        .get(`http://localhost:6003/aggregateSchedule`, { params: params })
        .then((response) => {
          // this.officeStaff = response.data.officeStaff;
          this.schedule = response.data;
          // console.log(response.data);
          this.fetchTeamMembers();
        })
        .catch((error) => {
          console.error("Error fetching team schedule:", error);
        });
    },
    selectDay(day) {
      if (day) {
        this.selectedDay = day;
        // Optionally, you can refetch the schedule for a specific day
        this.currentDate = new Date(
          this.currentYear,
          this.currentMonth,
          this.selectedDay
        );
        this.fetchReportingManager();
      }
    },
    deselectDay() {
      this.selectToday(); // Reset to today when deselected
    },
    nextMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1);
    },
    previousMonth() {
      this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1);
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
      const today = new Date();
      this.selectedDay = today.getDate();
    },
  },
};
</script>

<style scoped>
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

.legend-text {
  margin: 8px 8px;
}

.calendar-cell.active {
  background-color: #b6c6fd;
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
  margin: 0 auto;
  border-radius: 8px;
  padding: 10px;
}

.calendar-header h4 {
  font-weight: bold;
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

.calendar-cell.today {
  background-color: #d1e7ff;
  color: #0d6efd;
  font-weight: bold;
  border-radius: 8px;
  border: 1px solid #0d6efd;
}

.calendar-cell.selected-day {
  background-color: #e2e3e5;
  color: #495057;
  font-weight: bold;
  border-radius: 8px;
  border: 2px solid #495057;
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

.staff-schedule {
  width: 70%;
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.schedule-title {
  font-weight: bold;
  text-align: center;
  font-size: 1.25rem;
  margin-bottom: 20px;
}

.card {
  background-color: #fff;
  border: 1px solid #e0e0e0;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 15px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

.office-card h6,
.home-card h6 {
  font-size: 1.1rem;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.office-card ul,
.home-card ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
  max-height: 200px;
  overflow-y: auto;
}

.office-card ul li,
.home-card ul li {
  font-size: 0.85rem;
  padding: 3px 0;
  color: #555;
}

@media (max-width: 768px) {
  .calendar-container {
    flex-direction: column;
    height: auto;
  }

  .calendar,
  .staff-schedule {
    width: 100%;
    margin-bottom: 20px;
  }

  .calendar-cell {
    height: 40px;
  }

  .card {
    margin-bottom: 10px;
  }
}

@media (max-width: 576px) {
  .calendar-cell {
    height: 30px;
  }
}
</style>
