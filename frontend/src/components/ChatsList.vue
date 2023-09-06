<script lang="ts">
import {useChatsStore} from "@/stores/ChatsStore"
import { Chat } from '@/stores/ChatsStore'
import { getBackendHostname } from "@/common/requests"
import { useChatsListPanelStore } from "@/stores/ChatsListPanelStore"

export default {
    data() {
        return {
            //profilesStore: useProfilesStore(),
            chatStore: useChatsStore(),
            chatListPanelStore: useChatsListPanelStore(),
            chats: [] as Chat[],

            profileData: {
              name: "" as string,
              images: [] as string[],
              bio: "" as string,
              sex: "" as string,
              fields_of_study: [] as string[],
              target_sex: [] as string[],
              target_activity: [] as string[],
          },
        }
    },
    methods: {
        async loadChats(){
            await this.chatStore.loadChats()
            this.chats = this.chatStore.toList()

            console.log(this.chats.profile)
        },
        remoteURL(imageName: string) {
             return `${getBackendHostname()}/uploads/${imageName}`;
        },
        navigateToChat(){

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

    created() {
        this.loadChats();
    }
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
     
        <!-- <v-list class="chats list">
          <v-list-item 
            v-for="account in accounts"
            :key="account.id"
            @click="navigateToChat(account.public_id)"
            lines="two"
            :prepend-avatar="remoteURL(accountData.images[0])"
            :title="accountData.name"
            subtitle="Last message"
          ></v-list-item>
        </v-list> -->

    </v-navigation-drawer>
</template>