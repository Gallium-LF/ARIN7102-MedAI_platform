import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomePage from "@/pages/HomePage.vue";
import UserLoginPage from "@/pages/user/UserLoginPage.vue";
import HomeView from "@/views/HomeView.vue";
import AboutView from "@/views/AboutView.vue";
import DashboardView from "@/views/DashboardView.vue";
import Dash2View from "@/views/Dash2View.vue";
import Dash3View from "@/views/Dash3View.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    name: "about",
    component: AboutView,
  },
  {
    path: "/aiagent",
    name: "aiagent",
    component: HomeView,
  },
  { path: "/dashboard", name: "dashboard", component: DashboardView },
  { path: "/dashboard2", name: "dashboard2", component: Dash2View },
  { path: "/dashboard3", name: "dashboard3", component: Dash3View },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
