<script lang="ts">
import {useChatsStore} from "@/stores/ChatsStore"
import { Chat } from '@/stores/ChatsStore'
import { getBackendHostname } from "@/common/requests"
import { useChatsListPanelStore } from "@/stores/ChatsListPanelStore"

export default {
    data() {
        return {
            chatStore: useChatsStore(),
            chatListPanelStore: useChatsListPanelStore(),
        }
    },

    async created() {
        await this.chatStore.loadChats()
    },

    methods: {
        remoteURL(imageName: string) {
             return `${getBackendHostname()}/uploads/${imageName}`;
        },

        navigateToChat(publicId: str) {

        }
    },
    computed: {
        showChatsListPanel: {
            get() {
                return this.chatListPanelStore.showChatsListPanel
            },
            set(newValue: boolean) {
                this.chatListPanelStore.$patch({showChatsListPanel: newValue})
            }
        }
    },
}
</script>

<template>
    <v-navigation-drawer
      v-model="showChatsListPanel"
      temporary
      :permanent="$vuetify.display.width > 1100"
      class = "drawer chats list"
    >
    <div class="text-h5 mt-5 mb-5 ml-5" >Czaty</div>
     
        <v-list class="chats list">
          <v-list-item 
            v-for="chat in chatStore.toList()"
            :key="chat.profile.public_id"
            @click="navigateToChat(chat.profile.public_id)"
            lines="two"
            :prepend-avatar="remoteURL(chat.profile.images[0])"
            :title="chat.profile.name"
            subtitle="Last message"
          ></v-list-item>
        </v-list>

    </v-navigation-drawer>
</template>