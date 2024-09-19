<template>
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
        currentDate: new Date(), // Current date initialized
        selectedDay: null,
        staffId: null,
      };
    },
    created() {
        this.staffId = sessionStorage.getItem('staffID'); // Retrieve Staff_ID
        if (this.staffId) {
        console.log('Staff ID:', this.staffId); // Example usage
        } else {
        console.error('No Staff ID found.'); // Handle the case when Staff_ID is not found
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
  
        // Add blank cells for days from the previous month
        for (let i = 0; i < firstDay; i++) {
          days.push('');
        }
  
        // Add the days of the current month
        for (let day = 1; day <= lastDate; day++) {
          days.push(day);
        }
  
        return days;
      },
    },
    mounted() {
    // Add a global click event listener
        document.addEventListener('click', this.handleOutsideClick);
    },
    beforeUnmount() {
        // Clean up the event listener when the component is destroyed
        document.removeEventListener('click', this.handleOutsideClick);
    },
    methods: {
        // SECTION TO EDIT FOR BACKEND
        fetchUserSchedule() {
        // Logic to fetch user's schedule using this.staffId
        console.log('Fetching user schedule for Staff ID:', this.staffId);
        },
        fetchTeamSchedule() {
        // Logic to fetch team's schedule using this.staffId
        console.log('Fetching team schedule for Staff ID:', this.staffId);
        },

      selectDay(day) {
        if (day) {
          this.selectedDay = day;
        //   alert(`You selected: ${day} ${this.currentMonthName}, ${this.currentYear}`);
        }
      },
        // Method to deselect the day if clicked outside of the calendar
        handleOutsideClick(event) {
        const calendar = this.$el;
        if (!calendar.contains(event.target)) {
            this.deselectDay();
        }
        },
      deselectDay() {
        this.selectedDay = null; // Clear the selected day
      },
      nextMonth() {
        this.currentDate = new Date(this.currentYear, this.currentMonth + 1, 1); // Set to the first day of next month
      },
      previousMonth() {
        this.currentDate = new Date(this.currentYear, this.currentMonth - 1, 1); // Set to the first day of previous month
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
  .calendar {
    background-color: rgba(255, 255, 255, 0.9);
    max-width: 100%;
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
  
  .calendar-day {
    padding: 5px 0;
    background-color: #f1f3f4;
    color: #5f6368;
  }
  
  .calendar-cell {
    height: 80px;
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
  
  /* Responsiveness */
  @media (max-width: 768px) {
    .calendar-cell {
      height: 40px;
    }
  }
  
  @media (max-width: 576px) {
    .calendar-cell {
      height: 30px;
    }
  }
  </style>
  