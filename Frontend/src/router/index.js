import { createRouter, createWebHistory } from "vue-router";
import Home from '@/components/HomePage.vue'
import Login  from "@/components/Login.vue";
import OwnSchedule from "@/components/OwnSchedule.vue";
import TeamSchedule from "@/components/TeamSchedule.vue";
import Arrangements from "@/components/Arrangements.vue";



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
        path: '/arrangements', 
        name: 'Arrangements',
        component: Arrangements,
      }


]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router;