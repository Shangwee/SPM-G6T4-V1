import { createRouter, createWebHistory } from "vue-router";
import Home from '@/components/HomePage.vue'
import PassengerReassignment from "@/components/PassengerReassignment.vue";
import LiveChat from "@/components/LiveChat.vue";
import Login  from "@/components/Login.vue";
import FlightReassignment from "@/components/OwnSchedule.vue";
import CrewList from "@/components/CrewList.vue"; 
import UpdatedFlightReassignment from "@/components/UpdatedFlightReassignment.vue"; 
import Weather from "@/components/Weather.vue";
import Flight from "@/components/Flight.vue"; 
import Dashboards from "@/components/Dashboards.vue"; 
import OwnSchedule from "@/components/OwnSchedule.vue";



const routes = [
    {
        path: '/',
        name: 'Login',
        component: Login
    },
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/passengerreassignment',
        name: 'PassengerReassignment',
        component: PassengerReassignment
    },
    {
        path: '/livechat',
        name: 'LiveChat',
        component: LiveChat
    },
    {
        path: '/ownschedule',
        name: 'OwnSchedule',
        component: OwnSchedule
    },
    {
        path: '/crewlist', 
        name: 'CrewList',
        component: CrewList,
      },
      {
        path: '/updatedflightreassignment', 
        name: 'UpdatedFlightReassignment',
        component: UpdatedFlightReassignment,
      },

      {
        path: '/weather', 
        name: 'Weather',
        component: Weather,
      },

      {
        path: '/flight', 
        name: 'Flight',
        component: Flight,
      },
      

      {
        path: '/dashboards', 
        name: 'Dashboards',
        component: Dashboards,
      }


]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;