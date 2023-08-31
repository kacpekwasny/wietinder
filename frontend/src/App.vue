<script lang="ts">
import Header from "./components/Header.vue";
import { getJson, postJson } from "./common/requests";
import router from "./router";
import { nextTick } from "process";

export default {
  name: "App",
  components: {
    Header,
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
            return router.push("/login");
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
    <v-navigation-drawer
      v-model="showSidePanel"
      temporary
      :permanent="!$vuetify.display.sm"
    >
      <v-list>
        <v-list-item link>
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- Add more menu items as needed -->
      </v-list>
    </v-navigation-drawer>
    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>
