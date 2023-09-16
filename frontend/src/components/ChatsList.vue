<script lang="ts">
import { useChatsStore, lastChatInteraction } from "@/stores/ChatsStore";
import { getBackendHostname } from "@/common/requests";
import ChatsView from "@/views/ChatsView.vue";

export default {
  data() {
    return {
      chatStore: useChatsStore(),
    };
  },

  async created() {
    await this.chatStore.fetchChats();
  },

  methods: {
    remoteURL(imageName: string) {
      return `${getBackendHostname()}/uploads/${imageName}`;
    },

    navigateToChat(publicId: string) {
      this.$router.push({path: '/chats'})
      this.chatStore.makeActive(publicId);
    },
    formatDate(unixTimeStamp: number): string {
      let d = new Date(unixTimeStamp)
      let p = (v, l) => String(v).padStart(l, '0')
      let year  = d.getFullYear()
      let month = d.getMonth() + 1
      let date  = d.getDate()
      let hour  = d.getHours()
      let min   = d.getMinutes()
      let sec   = d.getSeconds()
      return `${p(date, 2)}/${p(month, 2)}/${year} ${p(hour, 2)}:${p(min, 2)}`
    }
  },

  
};
</script>

<template>
  <v-list class="pa-0">
    <v-list-item
      v-for="chat in chatStore.toList()"
      class="pa-1 ma-2 mb-0 mt-1"
      :key="chat.profile.public_id"
      @click="navigateToChat(chat.profile.public_id)"
      lines="two"
      :prepend-avatar="remoteURL(chat.profile.images[0])"
      :title="chat.profile.name"
      :subtitle="formatDate(lastChatInteraction(chat))"
    >
  
  </v-list-item>
  </v-list>
</template>
