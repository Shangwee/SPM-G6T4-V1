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

        <!-- Filters and Staff Schedule Section -->
        <div class="staff-schedule-container">
            <!-- Team Filter Section -->
            <div class="filter-controls d-flex justify-content-between mb-4">
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
                <h5 class="schedule-title">Staff Schedule for {{ selectedDay }} {{ currentMonthName }} {{ currentYear }}</h5>
                <div class="row">
                    <div class="col-md-6">
                        <div class="card office-card">
                            <h6>In Office</h6>
                            <ul>
                                <li v-for="staff in filteredStaffInOffice" :key="staff.name">{{ staff.name }}</li>
                            </ul>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card home-card">
                            <h6>Working from Home</h6>
                            <ul>
                                <li v-for="staff in filteredStaffWorkingFromHome" :key="staff.name">{{ staff.name }}</li>
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
            selectedDay: null,
            staffId: null,
            teams: ['Team A', 'Team B', 'Team C'], // Mock team names
            selectedTeam: '', // Selected team for filtering
            staff: [
                { name: 'John Doe', team: 'Team A', location: 'office' },
                { name: 'Jane Smith', team: 'Team A', location: 'home' },
                { name: 'Mark Lee', team: 'Team B', location: 'office' },
                { name: 'Lisa Wong', team: 'Team B', location: 'home' },
                { name: 'Samuel Jackson', team: 'Team C', location: 'office' },
                { name: 'Sophia Brown', team: 'Team C', location: 'home' },
                { name: 'Michael Clark', team: 'Team C', location: 'office' },
                { name: 'Linda Johnson', team: 'Team A', location: 'home' },
                { name: 'Robert Miller', team: 'Team B', location: 'office' },
                { name: 'Emily Wilson', team: 'Team A', location: 'office' }
            ], // Mock staff data
            filteredStaffInOffice: [], // Filtered office staff
            filteredStaffWorkingFromHome: [], // Filtered work-from-home staff
        };
    },
    created() {
        this.staffId = sessionStorage.getItem('staffID');
        this.selectToday(); // Select today's date
        this.filterStaff(); // Initial filter on page load
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
            const today = new Date();
            this.selectedDay = today.getDate();
            this.filterStaff();
        },
        filterByTeam() {
            this.filterStaff(); // Filter staff based on selected team
        },
        filterStaff() {
            // Filter staff for those in office
            this.filteredStaffInOffice = this.staff.filter(
                (staff) =>
                    staff.location === 'office' &&
                    (this.selectedTeam === '' || staff.team === this.selectedTeam)
            );
            // Filter staff for those working from home
            this.filteredStaffWorkingFromHome = this.staff.filter(
                (staff) =>
                    staff.location === 'home' &&
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
    height: 70vh;
    padding-bottom: 0;
}

/* Adjusting the calendar width to match the Manager calendar (70%) */
.calendar {
    background-color: rgba(255, 255, 255, 0.9);
    width: 70%;
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

/* Highlight for the selected date */
.calendar-cell.selected-day {
    background-color: #e2e3e5;
    color: #495057;
    font-weight: bold;
    border-radius: 8px;
    border: 2px solid #495057;
}

/* Highlight for today's date */
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

/* Hover */
.calendar-cell:hover {
    background-color: #f8f9fa;
    transition: background-color 0.3s ease;
}

/* Empty day cells for padding */
.empty-day {
    background-color: #fafafa;
}

/* Adjust staff schedule and filters to match Manager view (40%) */
.staff-schedule-container {
    width: 70%;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}


.filter-controls {
    display: flex;
    justify-content: space-between;
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 15px;
}

.filter-controls .form-group {
    width: 100%;
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

/* Ensure the card elements within the schedule section also stretch */
.card {
    flex-grow: 1;
    /* Allow the card to stretch to fill the container */
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
    list-style-type: none; /* Remove bullet points */
    padding: 0;
}

.office-card ul li,
.home-card ul li {
    font-size: 0.85rem; /* Reduced font size for compactness */
    padding: 3px 0; /* Reduced padding between list items */
    color: #555;
}

.staff-list {
    list-style-type: none; /* Remove bullet points */
    padding: 0;
    margin: 0;
    max-height: 200px; /* Set a maximum height for long lists */
    overflow-y: auto; /* Enable vertical scrolling */
}

.staff-item {
    font-size: 0.85rem; /* Reduced font size for compactness */
    padding: 3px 0; /* Reduced padding between list items */
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
