import './index.css'

import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import './index.css'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

// import { Button, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'

// import * as frappeUI from 'frappe-ui'
// // console.log(frappeUI)

let app = createApp(App)

// setConfig('resourceFetcher', frappeRequest)

app.use(router)
// app.use(resourcesPlugin)
// app.use(createListResource)

app.use(Toast, {
  // Optional settings
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
})

// app.component('Button', Button)
app.mount('#app')
