import { createApp } from 'vue'
import './style.css'
import router from './router'
import App from './App.vue'
import star from 'vue-star-rating'
import ToastPlugin from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-bootstrap.css'

const app = createApp(App)
app.use(ToastPlugin)
app.use(router)

app.mount('#app')