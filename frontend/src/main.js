import { createApp } from 'vue'
import { mask } from 'vue-the-mask'
import './style.css'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'

createApp(App)
    .directive('mask', mask)
    .use(router)
    .mount('#app')
