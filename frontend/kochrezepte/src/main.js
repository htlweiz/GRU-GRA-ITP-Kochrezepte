import { createApp } from 'vue'
import './style.css'
import router from './router'
import App from './App.vue'
import star from 'vue-star-rating'

const app = createApp(App)
app.use(router)

app.mount('#app')