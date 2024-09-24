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
      <!-- Section to show staff schedule -->
      <div v-if="selectedDay" class="staff-schedule mt-4">
        <h5 class="schedule-title">Staff Schedule for {{ selectedDay }} {{ currentMonthName }}, {{ currentYear }}</h5>
        <div class="row">
          <div class="col-md-6">
            <div class="card office-card">
              <h6>In Office</h6>
              <ul>
                <li>John Doe</li>
                <li>Emily Davis</li>
              </ul>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card home-card">
              <h6>Working from Home</h6>
              <ul>
                <li>Jane Smith</li>
                <li>Michael Lee</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      scheduleType: {
        type: String,
        required: true,
        validator: value => ['user', 'team'].includes(value),
      },
    },
    data() {
      return {
        currentDate: new Date(),
        selectedDay: null,
        staffId: null,
      };
    },
    created() {
      this.staffId = sessionStorage.getItem('staffID');
      if (this.staffId) {
        console.log('Staff ID:', this.staffId);
      } else {
        console.error('No Staff ID found.');
      }
      if (this.scheduleType === 'user') {
        this.fetchUserSchedule();
      } else {
        this.fetchTeamSchedule();
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
      fetchUserSchedule() {
        console.log('Fetching user schedule for Staff ID:', this.staffId);
      },
      fetchTeamSchedule() {
        console.log('Fetching team schedule for Staff ID:', this.staffId);
      },
      selectDay(day) {
        if (day) {
          this.selectedDay = day;
        }
      },
      deselectDay() {
        this.selectedDay = null;
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
    },
  };
  </script>
  
  <style scoped>
  .calendar-container {
    display: flex;
    justify-content: space-between; /* Align calendar and staff schedule side by side */
    align-items: flex-start; /* Align items to the top */
    height: 70vh; /* Adjusted height to ensure it fits within the viewport */
    padding-bottom: 0;
  }
  
  .calendar {
    background-color: rgba(255, 255, 255, 0.9);
    width: 58%; /* The calendar takes 58% of the available width */
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
    height: 60px; /* Adjust the calendar height */
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #e0e0e0;
    cursor: pointer;
    transition: background-color 0.3s ease;
    background-color: white;
  }
  
  .calendar-cell:hover {
    background-color: #f0f0f0;
  }
  
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
  
  .empty-day {
    background-color: #fafafa;
  }
  
  /* Improved Staff Schedule Styling */
  .staff-schedule {
    width: 40%; /* Staff schedule takes 40% of the available width */
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 20px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* Align content to the top */
  }
  
  .schedule-title {
    font-weight: bold;
    text-align: center;
    font-size: 1.25rem;
    margin-bottom: 20px;
  }
  
  /* Cards for In Office and Working from Home */
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
  }
  
  .office-card ul li,
  .home-card ul li {
    font-size: 0.95rem;
    padding: 5px 0;
    color: #555;
  }
  
  /* Responsive adjustments */
  @media (max-width: 768px) {
    .calendar-container {
      flex-direction: column; /* Stack vertically on smaller screens */
      height: auto;
    }
  
    .calendar, .staff-schedule {
      width: 100%; /* Make both full-width on small screens */
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
  