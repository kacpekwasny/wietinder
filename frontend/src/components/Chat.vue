<script lang="ts">
import { useChatsListPanelStore } from "@/stores/ChatsListPanelStore";
import { useChatsStore } from "@/stores/ChatsStore";
import { getBackendHostname, postJson } from "@/common/requests";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import EmojiPicker from "@/components/EmojiPicker/EmojiPicker.vue";

export default {
  data() {
    return {
      chatsStore: useChatsStore(),
      accountStore: useUserAccountStore(),
      ChatsListPanelStore: useChatsListPanelStore(),
      showEmoji: false as boolean,
      content: "",
    };
  },

  methods: {
    toggleChatsListsPanel() {
      this.ChatsListPanelStore.toggleChatsListPanel();
    },

    remoteURL(imageName: string) {
      return `${getBackendHostname()}/uploads/${imageName}`;
    },

    async sendMessage() {
      let resp = await postJson(`/send-message`, {
        recepient_public_id: this.chatsStore.activeChat.profile.public_id,
        content: this.content,
      });
    },
    toggleEmojiPicker() {
      this.showEmoji = !this.showEmoji;
    },

    handleEmojiClick(emoji: string) {
      this.content += emoji;
    },

    navigateToProfile() {
      this.$router.push({
        path: "/profile/" + this.chatsStore.activeChat.profile.public_id,
      });
    },
  },

  components: {
    EmojiPicker,
  },
};
</script>

<template>
  <v-card
    class="chat-card"
    v-if="chatsStore.activeChat != null"
    style="height: 100%; position: relative"
  >
    <v-card-title class="ml-6 pa-2 d-flex justify-between align-center">
      <v-card
        class="pa-1 pl-2 pr-2 v-btn--elevated pointer"
        @click="navigateToProfile"
      >
        <v-avatar>
          <v-img
            :src="remoteURL(chatsStore.activeChat.profile.images[0])"
          ></v-img>
        </v-avatar>
        {{ chatsStore.activeChat.profile.name }}
      </v-card>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-content class="chat-content">
      <v-list style="display: flex; flex-direction: column-reverse">
        <v-list-item v-for="msg in chatsStore.activeChat.messages">
          <v-card
            class="message-card ma-3 pa-2 elevation-3 float-right"
            style="max-width: 80%"
            v-if="msg.author == accountStore.accountData.public_id"
          >
            <p>Ty:</p>
            <p>{{ msg.message }}</p>
          </v-card>
          <v-card
            v-else
            class="message-card ma-3 pa-2 elevation-3"
            style="max-width: 80%"
          >
            <p>{{ chatsStore.activeChat.profile.name }}:</p>
            <p>{{ msg.message }}</p>
          </v-card>
        </v-list-item>
      </v-list>
      <div class="emoji-picker-card">
        <EmojiPicker
          v-if="showEmoji"
          @emoji_click="handleEmojiClick"
        ></EmojiPicker>
      </div>
    </v-card-content>
    <v-card class="textarea-card d-flex">
      <v-btn icon class="ml-5 mr-3" color="yellow" @click="toggleEmojiPicker">
        <v-icon>mdi-emoticon-happy</v-icon>
      </v-btn>

      <v-textarea
        prepend-inner-icon="mdi-chat"
        class="mx-2 resize mt-4"
        label="Napisz wiadomość"
        rows="1"
        max-rows="4"
        style="width: 100%"
        auto-grow
        v-model="content"
      ></v-textarea>
      <v-btn
        icon
        class="ml-3 mr-5"
        color="yellow"
        float-right
        @click="sendMessage()"
      >
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
.emoji-picker-card {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: white; /* You can adjust the background color as needed */
  z-index: 100;
  max-width: 40%;
}
.message-card {
  background-color: #e0e0e0; /* Background color of the chat bubble */
  padding: 10px;
  margin: 10px; /* Add spacing between chat messages */
  border-radius: 10px; /* Rounded corners for the chat bubble */
  box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Optional: Add a shadow for depth */
  word-wrap: break-word; /* Wrap long words to the next line */
}

.pointer {
  cursor: pointer;
}
</style>
