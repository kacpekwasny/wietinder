import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

import { loadFonts } from './plugins/webfontloader'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})

createApp(App).use(vuetify).mount('#app')



loadFonts()

createApp(App)
  .use(router)
  .use(vuetify)
  .mount('#app')
