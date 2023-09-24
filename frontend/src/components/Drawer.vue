<script lang="ts">
import { usePanelStore } from "../stores/SidePanelStore";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import { mapState } from "pinia";
import { getBackendHostname, getJson, postJson } from "../common/requests";
import router from "../router";
import { useChatsStore } from "@/stores/ChatsStore";
import ChatsList from "@/components/ChatsList.vue";
import Chat from "@/components/Chat.vue";

export default {
  data() {
    return {
      panelStore: usePanelStore(),
      userAccountStore: useUserAccountStore(),
      chatsStore: useChatsStore(),
    };
  },
  methods: {
    toggleSidePanel() {
      this.panelStore.toggleSidePanel();
    },
    remoteURL(imageName: string) {
      return `${getBackendHostname()}/api/uploads/${imageName}`;
    },
    async logout() {
      await getJson("/api/logout");
      useUserAccountStore().setLoggedOut();
      router.push("/login");
    },

    navigateToSwipe() {
      this.$router.push({ path: "/swipe" });
    },
    navigateToLikes() {
      this.$router.push({ path: "/likes" });
    },
  
    navigateToAccountConfig() {
      this.$router.push({ path: "/account" });
    },
  },
  computed: {
    showSidePanel: {
      get() {
        if (this.userAccountStore.loggedIn) {
          return this.panelStore.showSidePanel;
        }
        return false;
      },
      set(newValue: boolean) {
        usePanelStore().$patch({ showSidePanel: newValue });
      },
    },
    ...mapState(useUserAccountStore, ["accountData"]),
  },
  components: { ChatsList, Chat }
};
</script>

<template>
  <v-navigation-drawer
    v-model="showSidePanel"
    temporary
    :permanent="$vuetify.display.width > 1100"
    class="drawer h-100 elevation-10"
  >
    <div class="d-flex flex-column h-100 justify-space-between pb-12">
      <v-list class="">
        <v-list-item
          @click="navigateToAccountConfig"
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

        <v-list-item class="pa-0 ">
          <v-expansion-panels class="">
            <v-expansion-panel class="" flat>
              <v-expansion-panel-title class="pa-4 pt-2 pb-2" style="margin-left: 2px;">
                <div class="v-list-item__prepend">
                  <v-icon density="default">
                    mdi-chat
                  </v-icon>
                </div>
                <p>Chaty</p>
              </v-expansion-panel-title>
              <v-expansion-panel-text class="drawer-chatlist-expansion-text">
                <ChatsList></ChatsList>
              </v-expansion-panel-text>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-list-item>
      </v-list>

      <v-list>
        <v-list-item
          prepend-icon="mdi-logout"
          class="elevation-3 ma-2 pa-2 rounded"
          title="Wyloguj"
          @click="logout"
          style="background-color: yellow"
        ></v-list-item>
      </v-list>
    </div>
  </v-navigation-drawer>
</template>

<style>
.drawer-chatlist-expansion-text .v-expansion-panel-text__wrapper {
  padding: 0;
}
</style>