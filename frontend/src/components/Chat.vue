<script lang = "ts">
import {useChatsListPanelStore} from "@/stores/ChatsListPanelStore"
import { getBackendHostname } from "@/common/requests"
export default {
    data() {
        return {
          ChatsListPanelStore: useChatsListPanelStore()
        }
    },
    methods: {
        toggleChatsListsPanel(){
            this.ChatsListPanelStore.toggleChatsListPanel()
        },
        remoteURL(imageName: string) {
            return `${getBackendHostname()}/uploads/${imageName}`;
        },
    },
}

</script>

<template>
   <v-card class="chat-card">
    <v-card-title class="pa-2 d-flex justify-between align-center">
      <v-btn @click="toggleChatsListsPanel" icon class="ml-3 mr-5">
        <v-icon>mdi-comment-outline</v-icon>
      </v-btn>
      <div class="text-right">
        Dupa 
      </div>
    </v-card-title>
  </v-card>
</template>