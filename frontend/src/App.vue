<script lang="ts">
import Header from "./components/Header.vue";
import Drawer from "./components/Drawer.vue";
import router from "./router";
import { useUserAccountStore } from "./stores/AccountDataStore";
import { usePanelStore } from "./stores/SidePanelStore";
import { mapState } from "pinia";
import { useSocketStore } from "./socket/socket";
import { useChatsStore } from "./stores/ChatsStore";

export default {
  name: "App",
  components: {
    Header,
    Drawer,
  },
  
  data() {
    return {
      userAccountStore: useUserAccountStore(),
      chatsStore:       useChatsStore(),
      socketStore:      useSocketStore(),
    };
  },

  async mounted() {
    await this.socketStore.refreshJWT()
    this.socketStore.setupEventListeners()
    this.socketStore.keepConnectionToMyRoom()
  },

  watch: {
    $route: async function (to, from) {
      
      await this.userAccountStore.refreshUserData(true);
       
      if (!this.userAccountStore.loggedIn) {
        if (to.name === "register") {
          return; 
        } else {
          return router.push("/login");
        }
      }

      if (this.userAccountStore.accountData.images.length == 0 && this.userAccountStore.loggedIn) {
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
