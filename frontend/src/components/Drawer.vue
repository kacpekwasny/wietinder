<script lang="ts">

import { usePanelStore } from "../stores/SidePanelStore";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import { mapState } from "pinia";
import { getBackendHostname, getJson, postJson} from "../common/requests";
import router from "../router";
import { useChatsListPanelStore } from "@/stores/ChatsListPanelStore";

export default { 
  data() {
    return {
      panelStore: usePanelStore(),
      userAccountStore: useUserAccountStore(),
    }
  },
  methods: {
    toggleSidePanel() {
      this.panelStore.toggleSidePanel();
    },
    remoteURL(imageName: string) {
      return `${getBackendHostname()}/uploads/${imageName}`;
    },
    async logout() {
      await getJson("/logout");
      useUserAccountStore().setLoggedOut()
      router.push("/login");
    },
    navigateToAccount(){
      this.$router.push({ path: "/profile/" + this.accountData.public_id})
    },
    navigateToSwipe(){
      this.$router.push({ path: "/swipe"})
    },
    navigateToLikes(){
      this.$router.push({ path: "/likes"})
    },
    navigateToChats(){
      useChatsListPanelStore().openChatsListPanel()
      this.$router.push({ path: "/chats"})
    },
  },
  computed: {
    showSidePanel: {
      get() {
        if (this.userAccountStore.loggedIn) {
          return this.panelStore.showSidePanel
        }
        return false;
      },
      set(newValue: boolean) {
        usePanelStore().$patch({showSidePanel: newValue})
      }
    },
    ...mapState(useUserAccountStore, ['accountData'])
  },
};
</script>

<template>
    <v-navigation-drawer
      v-model="showSidePanel"
      temporary
      :permanent="$vuetify.display.width > 1100"
      
      class = "drawer h-100 elevation-10"
    >
      <div
        class="d-flex flex-column h-100 justify-space-between pb-12"
      >
        <v-list class="">
          <v-list-item 
            @click="navigateToAccount"
            lines="two"
            :prepend-avatar="remoteURL(accountData.images[0])"
            :title="accountData.name"
            subtitle="Zalogowane"
          ></v-list-item>
          <v-divider></v-divider>
          <v-list-item 
            @click="navigateToSwipe"
            prepend-icon="mdi-cards" 
            title="Chybił trafił" 
          ></v-list-item>
          <v-list-item 
            @click="navigateToLikes"
            prepend-icon="mdi-heart" 
            title="Polubienia" 
          ></v-list-item>
          <v-list-item 
            @click="navigateToChats"
            prepend-icon="mdi-chat" 
            title="Chat" 
          ></v-list-item>
          <v-list-item 
            prepend-icon="mdi-account" 
            title="Profil" 
            :to="{ name: 'account'}"
          ></v-list-item>
        </v-list>
  
        <v-list>
          <v-list-item 
            prepend-icon="mdi-logout"
            class="elevation-3 ma-2 pa-2 rounded"
            title="Wyloguj"
            @click="logout"
            style="background-color: yellow;"
          ></v-list-item>
        </v-list>
      </div>
    </v-navigation-drawer>
</template>

