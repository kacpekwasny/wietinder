<script lang="ts">
import Header from "./components/Header.vue";
import Drawer from "./components/Drawer.vue";
import { getJson } from "./common/requests";
import router from "./router";
import { useUserAccountStore } from "./stores/AccountDataStore";
import { usePanelStore } from "./stores/SidePanelStore";
import { mapState } from "pinia";

export default {
  name: "App",
  components: {
    Header,
    Drawer,
  },
  data() {
    return {
      userAccountStore: useUserAccountStore(),
      dialog:false,
    };
  },

  watch: {
    $route: async function (to, from) {
      
      await this.userAccountStore.refreshUserData();
      if (!this.userAccountStore.loggedIn) {
        if (!this.$route.name.startsWith("/register")) {
          if (to.name.startsWith("/register")) {
            return router.push("/login");
          }
        }
      }

      if (this.userAccountStore.accountData.images.length == 0 && this.userAccountStore.loggedIn){
        this.dialog = true
        return router.push("/account")
      }
    },
  },
  methods: {
    toggleSidePanel() {
      usePanelStore().toggleSidePanel();
    },
  },
  computed: {
    ...mapState(useUserAccountStore, ["loggedIn", "accountData"]),
    ...mapState(usePanelStore, ["showSidePanel"]),
  },
};
</script>

<template>
  <v-app>
    <v-dialog
      v-model="dialog"
      width="auto"
    >
      <v-card>
        <v-card-text>
          Musisz dodać przynajmniej jedno zdjęcie!
        </v-card-text>
        <v-card-actions>
          <v-btn block @click="dialog = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-app-bar app density="compact">
      <v-app-bar-nav-icon
        v-if="loggedIn"
        @click="toggleSidePanel"
      ></v-app-bar-nav-icon>
      <Header />
    </v-app-bar>
    <Drawer />
    <v-main style="height: 100vh;">
      <router-view />
    </v-main>
  </v-app>
</template>
