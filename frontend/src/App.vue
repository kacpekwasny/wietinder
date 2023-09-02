<script lang="ts">
import Header from "./components/Header.vue";
import Drawer from "./components/Drawer.vue";
import { getJson } from "./common/requests";
import router from "./router";


export default {
  name: "App",
  components: {
    Header,
    Drawer,
  },
  data() {
    return {
      showSidePanel: true,
    };
  },
  watch: {
    $route: function (to, from) {
      this.isUserLoggedIn();
    },
  },
  methods: {
    isUserLoggedIn() {
      getJson("/is-user-logged-in")
        .then((resp) => {
          return resp.json();
        })
        .then((json) => {
          if (json.info === "user_not_logged_in") {
            if (this.$route.name != "register"){
              return router.push("/login");
            }
          }
        })
        .catch((error) => {
          console.error("An error occurred:", error);
        });
    },
    toggleSidePanel() {
      this.showSidePanel = !this.showSidePanel;
    },
  },
};
</script>

<template>
  <v-app>
    <v-app-bar app density="compact">
      <v-app-bar-nav-icon @click="toggleSidePanel"></v-app-bar-nav-icon>
      <Header />
    </v-app-bar>
    <Drawer />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

