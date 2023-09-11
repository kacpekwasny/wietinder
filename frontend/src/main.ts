/**
 * main.ts
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Plugins
import { registerPlugins } from '@/plugins'
import { createPinia } from 'pinia' // Kacper - pinia store
import VueSocketIO from 'vue-socket.io' 

const pinia = createPinia()
const app = createApp(App)
const socketOptions = {
    debug: true,
    connection: 'http://localhost:5000', 
  }

registerPlugins(app)

app.use(new VueSocketIO(socketOptions))
app.use(pinia)
app.mount('#app')
