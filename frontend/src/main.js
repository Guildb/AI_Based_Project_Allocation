// src/main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/css/tailwind.output.css"; // Import Tailwind CSS

createApp(App).use(router).mount("#app");
