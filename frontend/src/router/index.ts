import { createRouter, createWebHistory } from "vue-router";
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AccountView from '../views/AccountView.vue'
import ProfileView from "@/views/ProfileView.vue";
import SwipeView from "@/views/SwipeView.vue";
import LikesMeView from  "@/views/LikesMeView.vue";
import ChatsView from "@/views/ChatsView.vue";

const router = createRouter ({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "login",
            component: LoginView
        },
        {
            path: "/home",
            redirect: "/"
        },
        {
            path: "/login",
            redirect: "/"
        },
        {
            path: "/register",
            name: "register",
            component: RegisterView
        },
        {
            path: "/account",
            name: "account",
            component: AccountView
        },
        {
            path: "/profile/:profile_id",
            name: "profile",
            component: ProfileView
        },
        {
            path: "/swipe",
            name: "swipe",
            component: SwipeView
        },
        {
            path: "/likes",
            name: "likes",
            component: LikesMeView
        },
        {
            path: "/chats",
            name: "chats",
            component: ChatsView
        },
        {
            path: "/:pathMatch(.*)*",
            redirect: '/'
        },
    ],
})

export default router
// // Composables
// import { createRouter, createWebHistory } from 'vue-router'

// const routes = [
//   {
//     path: '/',
//     component: () => import('@/layouts/default/Default.vue'),
//     children: [
//       {
//         path: '',
//         name: 'Home',
//         // route level code-splitting
//         // this generates a separate chunk (about.[hash].js) for this route
//         // which is lazy-loaded when the route is visited.
//         component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
//       },
//     ],
//   },
// ]

// const router = createRouter({
//   history: createWebHistory(process.env.BASE_URL),
//   routes,
// })

// export default router
