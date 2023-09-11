<script lang=ts>
import { getJson } from "../common/requests";
import { useProfilesStore } from "@/stores/ProfilesStore";
import Chat from "@/components/Chat.vue";
import { useChatsStore } from "@/stores/ChatsStore";


export default {
    data() {
        return {
            profilesStore: useProfilesStore(),
            chatStore: useChatsStore(),
        };
    },
    methods: {
    },
    async created() {
        await this.chatStore.fetchChats()
        this.chatStore.makeActive(this.chatStore.toList()[0].profile.public_id)
    },
    components: { Chat }
}
</script>

<template>
  <v-container fluid class="d-flex flex-column pa-0" style="max-width: 800px; height: 100%;">
      <Chat></Chat>
  </v-container>
</template>