import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import { OhVueIcon, addIcons } from "oh-vue-icons";
import {IoCloseCircle, IoWifi, BiCheckCircle, MdError, 
    MdQuestionanswer, BiCheckCircleFill, MdExpandmoreRound, MdSearch, MdNetworkcheck} from "oh-vue-icons/icons";

addIcons(IoCloseCircle, IoWifi, BiCheckCircle, MdError,
    MdQuestionanswer, BiCheckCircleFill, MdExpandmoreRound, MdSearch, MdNetworkcheck);

const app = createApp(App)
app.component("v-icon", OhVueIcon);

app.use(createPinia())
app.use(router)

app.mount('#app')
