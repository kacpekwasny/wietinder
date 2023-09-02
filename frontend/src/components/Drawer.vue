<script lang="ts">

import { usePanelStore } from "../stores/SidePanelStore";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import { mapState } from "pinia";
import { getBackendHostname, postJson} from "../common/requests";
import router from "../router";

export default { 
  data() {
    return {
      panelStore: usePanelStore()
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
      let respo = await postJson("/logout", { logout: "true" });
      router.push("/login");
    },
    navigateToAccount(){
      this.$router.push({ path: "/profile/" + this.accountData.public_id})
    }
  },
  computed: {
    showSidePanel: {
      get() {
        return this.panelStore.showSidePanel
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
      class = "drawer"
    >
      <v-list>
        <v-list-item 
          @click="navigateToAccount"
          lines="two"
          :prepend-avatar="remoteURL(accountData.images[0])"
          :title="accountData.name"
          subtitle="Zalogowane"
        ></v-list-item>
        <v-divider></v-divider>
        <v-list-item 
          prepend-icon="mdi-cards" 
          title="Chybił trafił" 
        ></v-list-item>
        <v-list-item 
          prepend-icon="mdi-heart" 
          title="Polubienia" 
        ></v-list-item>
        <v-list-item 
          prepend-icon="mdi-account" 
          title="Profil" 
          :to="{ name: 'account'}"
        ></v-list-item>
        <v-list-item 
          prepend-icon="mdi-logout" 
          title="Wyloguj" 
          @click="logout"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>
</template>

