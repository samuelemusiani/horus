import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { OhVueIcon, addIcons } from "oh-vue-icons";
import {
    IoWifi,
    BiCheckCircle,
    MdError,
    BiCheckCircleFill,
    MdExpandmoreRound,
    MdSearch,
    MdCable
} from "oh-vue-icons/icons";

addIcons(IoWifi, BiCheckCircle, MdError, BiCheckCircleFill, MdExpandmoreRound, MdSearch, MdCable);

const app = createApp(App)
app.component("v-icon", OhVueIcon);

app.use(createPinia())
app.use(router)

app.mount('#app')
