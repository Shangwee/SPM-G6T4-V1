<template>
  <div class="calendar-container">
    <!-- Calendar Section -->
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
        <div
          v-for="(day, index) in daysInMonth"
          :key="index"
          class="calendar-cell text-center"
          @click.stop="selectDay(day)"
          :class="{
            'empty-day': day === '',
            'selected-day': day === selectedDay,
            'today': isToday(day)
          }"
        >
          <span v-if="day">{{ day }}</span>
        </div>
      </div>
    </div>

    <!-- Filters and Staff Schedule Section -->
    <div class="staff-schedule-container">
      <!-- Filters Section -->
      <div class="filter-controls d-flex justify-content-between mb-4">
        <div class="form-group mr-2">
          <label for="department">Department</label>
          <select id="department" v-model="selectedDepartment" class="form-control" @change="filterByDepartment">
            <option value="">All Departments</option>
            <option v-for="department in departments" :key="department" :value="department">{{ department }}</option>
          </select>
        </div>
        <div class="form-group">
          <label for="team">Team</label>
          <select id="team" v-model="selectedTeam" class="form-control" @change="filterByTeam">
            <option value="">All Teams</option>
            <option v-for="team in teams" :key="team" :value="team">{{ team }}</option>
          </select>
        </div>
      </div>

      <!-- Staff Schedule Section -->
      <div v-if="selectedDay" class="staff-schedule">
        <h5 class="schedule-title">Staff Schedule for {{ selectedDay }} {{ currentMonthName }}, {{ currentYear }}</h5>
        <div class="row">
          <div class="col-md-6">
            <div class="card office-card">
              <h6>In Office</h6>
              <ul>
                <li v-for="staff in filteredStaffInOffice" :key="staff">{{ staff }}</li>
              </ul>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card home-card">
              <h6>Working from Home</h6>
              <ul>
                <li v-for="staff in filteredStaffWorkingFromHome" :key="staff">{{ staff }}</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentDate: new Date(),
      selectedDay: null, // This will hold the day number
      staffId: null,
      departments: ['HR', 'Finance', 'IT', 'Marketing'], // Example departments
      teams: ['Team A', 'Team B', 'Team C'], // Example teams
      selectedDepartment: '',
      selectedTeam: '',
      staff: [
        { name: 'John Doe', department: 'HR', team: 'Team A', location: 'office' },
        { name: 'Emily Davis', department: 'Finance', team: 'Team B', location: 'office' },
        { name: 'Jane Smith', department: 'IT', team: 'Team A', location: 'home' },
        { name: 'Michael Lee', department: 'Marketing', team: 'Team C', location: 'home' },
      ],
      filteredStaffInOffice: [],
      filteredStaffWorkingFromHome: [],
    };
  },
  created() {
    this.staffId = sessionStorage.getItem('staffID');
    this.selectToday(); // Automatically select today's date when the component is created
    this.filterStaff();
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
    selectDay(day) {
      if (day) {
        this.selectedDay = day;
      }
    },
    deselectDay() {
      // Automatically select today's date when clicking outside of a day (white space)
      this.selectToday();
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
      // Automatically select today's date when the component is created or when deselected
      const today = new Date();
      this.selectedDay = today.getDate();
      this.filterStaff(); // Ensure filtering happens when selecting today
    },
    filterByDepartment() {
      this.filterStaff();
    },
    filterByTeam() {
      this.filterStaff();
    },
    filterStaff() {
      // Filter staff by selected department and team
      this.filteredStaffInOffice = this.staff.filter(
        (staff) =>
          staff.location === 'office' &&
          (this.selectedDepartment === '' || staff.department === this.selectedDepartment) &&
          (this.selectedTeam === '' || staff.team === this.selectedTeam)
      );
      this.filteredStaffWorkingFromHome = this.staff.filter(
        (staff) =>
          staff.location === 'home' &&
          (this.selectedDepartment === '' || staff.department === this.selectedDepartment) &&
          (this.selectedTeam === '' || staff.team === this.selectedTeam)
      );
    },
  },
};
</script>

  

<style scoped>
.calendar-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  height: 80vh; /* Increase height to give more space */
  padding-bottom: 0;
}

.calendar {
  background-color: rgba(255, 255, 255, 0.9);
  width: 65%; /* Keep the calendar width */
  margin: 0 auto;
  border-radius: 8px;
  padding: 10px;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr); /* Ensure 7 columns for the days of the week */
  gap: 1px;
  width: 100%; /* Ensure the grid takes full width */
}

.calendar-cell {
  height: 80px; /* Adjust height to make sure the grid cells are tall enough */
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid #e0e0e0;
  cursor: pointer;
  transition: background-color 0.3s ease;
  background-color: white;
}

.calendar-day {
  padding: 10px 0;
  background-color: #f1f3f4;
  color: #5f6368;
  font-weight: bold;
  text-align: center;
}

/* Style today and selected day */
.calendar-cell.today {
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.calendar-cell.selected-day {
  background-color: #0d6efd;
  color: white;
  border: 2px solid #004085;
}

/* Empty day cells for padding */
.empty-day {
  background-color: #fafafa;
}

.staff-schedule-container {
  width: 33%; /* Adjust the filter and staff schedule width */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.filter-controls {
  display: flex; /* Align filters in a row */
  justify-content: space-between;
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 15px;
}

.filter-controls .form-group {
  width: 48%;
}

.filter-controls select {
  width: 100%;
  padding: 5px;
  font-size: 0.9rem;
  border-radius: 4px;
  border: 1px solid #ced4da;
}

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

.office-card ul,
.home-card ul {
  list-style-type: none;
  padding: 0;
}

.office-card ul li,
.home-card ul li {
  font-size: 0.95rem;
  padding: 5px 0;
  color: #555;
}

@media (max-width: 768px) {
  .calendar-container {
    flex-direction: column;
    height: auto;
  }

  .calendar, .staff-schedule-container {
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