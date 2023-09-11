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
import {state} from './socket/socket'

const pinia = createPinia()
const app = createApp(App)

console.log(state)

registerPlugins(app)

app.use(pinia)
app.mount('#app')
