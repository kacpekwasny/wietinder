<script lang="ts">
import { useChatsListPanelStore } from "@/stores/ChatsListPanelStore";
import { useChatsStore } from "@/stores/ChatsStore";
import { getBackendHostname } from "@/common/requests";
import { useUserAccountStore } from "@/stores/AccountDataStore";

export default {
  data() {
    return {
      chatsStore: useChatsStore(),
      accountStore: useUserAccountStore(),
      ChatsListPanelStore: useChatsListPanelStore(),
    };
  },

  methods: {
    toggleChatsListsPanel() {
      this.ChatsListPanelStore.toggleChatsListPanel();
    },

    remoteURL(imageName: string) {
      return `${getBackendHostname()}/uploads/${imageName}`;
    },
  },
};
</script>

<template>
  <v-card class="chat-card" v-if="chatsStore.activeChat != null" style="height: 100%; position: relative;">
    <v-card-title class="pa-2 d-flex justify-between align-center">
      <v-btn @click="toggleChatsListsPanel" icon class="ml-3 mr-5">
        <v-icon>mdi-comment-outline</v-icon>
      </v-btn>
      <div class="text-right">
        <v-avatar>
          <v-img
            :src=remoteURL(chatsStore.activeChat.profile.images[0])
          ></v-img>
        </v-avatar>
        {{ chatsStore.activeChat.profile.name }}
     </div>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-content class="chat-content" >
      <v-list>
        <v-list-item v-for="msg in chatsStore.activeChat.messages">
          <v-card class="ma-3 pa-2 elevation-3 float-right" style ="max-width: 80%;"
          v-if=" msg.author ==  accountStore.accountData.public_id">
            <p>Ty:</p>
            <p>{{ msg.message }}</p>
          </v-card>
          <v-card v-else class="ma-3 pa-2 elevation-3 " style ="max-width: 80%;"
          >
            <p>{{ chatsStore.activeChat.profile.name }}:</p>
            <p>{{ msg.message }}</p>
          </v-card>
        </v-list-item>
      </v-list>
      
    </v-card-content>
    <v-card class="textarea-card d-flex" >
      
        
        <v-textarea
          prepend-inner-icon="mdi-chat"
          class="mx-6 resize mt-4 "
          label="Napisz wiadomość"
          rows="1"
          max-rows="4"
          style="width: 100%;"
          auto-grow
        ></v-textarea>
      <v-btn icon class="ml-3 mr-5" color="yellow" float-right>
        <v-icon>mdi-send</v-icon>
      </v-btn>

    </v-card>
  </v-card>
</template>

<style>

.textarea-card {
  position: absolute;
  width: 100%;
  bottom: 0;
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.1); 
  align-items: center;
  z-index: 999;
}
</style>