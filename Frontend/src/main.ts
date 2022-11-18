import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'


const app = createApp(App)
import axios from 'axios'
import VueAxios from 'vue-axios'

app.use(VueAxios, axios)

app.use(router)

app.mount('#app')
