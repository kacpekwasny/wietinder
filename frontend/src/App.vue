<script lang="ts">

import Header from "./components/Header.vue"

export default {
  name: 'App',
  components: {
    Header
  },
  data: () => ({
    //
  }),
}
</script>

<template>
  
  <v-app>
     <v-app-bar>
       <Header />
       </v-app-bar>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
