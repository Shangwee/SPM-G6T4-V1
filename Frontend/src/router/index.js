import { createRouter, createWebHistory } from "vue-router";
import Home from '@/components/HomePage.vue'
import Login  from "@/components/Login.vue";
import OwnSchedule from "@/components/OwnSchedule.vue";
import TeamSchedule from "@/components/TeamSchedule.vue";
import Arrangements from "@/components/Arrangements.vue";
import Requests from "@/components/Requests.vue";
import Notifications from "@/components/Notifications.vue";
import DirectorCalendarView from '@/components/DirectorCalendarView.vue';
import ManagerCalendarView from '@/components/ManagerCalendarView.vue';
import StaffCalendarView from '@/components/StaffCalendarView.vue';


const routes = [
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/teamschedule',
        name: 'TeamSchedule',
        component: TeamSchedule
    },
    {
        path: '/ownschedule',
        name: 'OwnSchedule',
        component: OwnSchedule
    },
    {
        path: '/requests',
        name: 'Requests',
        component: Requests
    },

    {
        path: '/arrangements', 
        name: 'Arrangements',
        component: Arrangements,
    },
    {
        path: '/notifications',
        name: 'Notifications',
        component: Notifications,
    },

      {
        path: '/DirectorCalendarView', // Add a path for the test page
        name: 'DirectorCalendarView',
        component: DirectorCalendarView, // Assign the TestPage component to this route
      },

      {
        path: '/StaffCalendarView', // Add a path for the test page
        name: 'StaffCalendarView',
        component: StaffCalendarView, // Assign the TestPage component to this route
      },

      {
        path: '/ManagerCalendarView', // Add a path for the test page
        name: 'ManagerCalendarView',
        component: ManagerCalendarView, // Assign the TestPage component to this route
      },


]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;