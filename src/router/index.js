import {createRouter, createWebHistory} from "vue-router";
import Data from "@/components/Data.vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Data,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;