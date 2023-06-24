import { createRouter, createWebHistory } from "vue-router";
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import AccountView from '../views/AccountView.vue'

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
        }
    ]
})

export default router