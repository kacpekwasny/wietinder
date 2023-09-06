<script lang="ts">
import { useChatsListPanelStore } from "@/stores/ChatsListPanelStore";
import { useChatsStore } from "@/stores/ChatsStore";
import { getBackendHostname } from "@/common/requests";

export default {
  data() {
    return {
      chatsStore: useChatsStore(),
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
  <v-card class="chat-card" v-if="chatsStore.activeChat != null">
    <v-card-title class="pa-2 d-flex justify-between align-center">
      <v-btn @click="toggleChatsListsPanel" icon class="ml-3 mr-5">
        <v-icon>mdi-comment-outline</v-icon>
      </v-btn>
      <div class="text-right">
        {{ chatsStore.activeChat.profile.name }}
      </div>
    </v-card-title>
    <v-card-content>
      <v-list>
        <v-list-item v-for="msg in chatsStore.activeChat.messages">
          <v-card class="ma-3 pa-2 elevation-3">
            <p>{{ msg.author }}</p>
            <p>{{ msg.message }}</p>
          </v-card>
        </v-list-item>
      </v-list>
    </v-card-content>
  </v-card>
</template>
