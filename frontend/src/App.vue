<script lang="ts">
import Header from "./components/Header.vue";
import Drawer from "./components/Drawer.vue";
import { getJson } from "./common/requests";
import router from "./router";
import { usePanelStore } from "./stores/SidePanelStore";
import { useUserAccountStore } from "./stores/AccountDataStore";
import { mapState } from "pinia";


export default {
  name: "App",
  components: {
    Header,
    Drawer,
  },
  data() {
    return {
      showSidePanel: usePanelStore().showSidePanel,
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
      usePanelStore().toggleSidePanel();
    },
  },
  computed: {
    ...mapState(useUserAccountStore, ['loggedIn'])
  },
};
</script>

<template>
  <v-app>
    <v-app-bar app density="compact">
      <v-app-bar-nav-icon v-if="loggedIn" @click="toggleSidePanel"></v-app-bar-nav-icon>
      <Header />
    </v-app-bar>
    <Drawer />
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

