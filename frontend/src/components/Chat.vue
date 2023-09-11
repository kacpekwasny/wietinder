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
    clickOutsideEmojiPicker() {
      if (this.showEmoji) {
        this.showEmoji = false
      }
    }
  },

  components: {
    EmojiPicker,
  },

  computed: {},
};
</script>

<template>
  <div id="section" v-if="chatsStore.activeChat != null" class="chat">
    <v-card-title
      id="header"
      class="contact bar ml-6 pa-2 d-flex justify-between align-center"
    >
      <v-card class="" @click="navigateToProfile" style="cursor: pointer">
        <v-avatar>
          <v-img
            :src="remoteURL(chatsStore.activeChat.profile.images[0])"
          ></v-img>
        </v-avatar>
        {{ chatsStore.activeChat.profile.name }}
      </v-card>
    </v-card-title>
    <v-divider></v-divider>
    <v-list class="d-flex flex-column messages" style="flex-direction: column-reverse;">
      <v-list-item v-for="msg in chatsStore.activeChat.messages">
        <v-card
          class="ma-3 pa-2 elevation-4 rounded-lg"
          :class="{
            'float-right': msg.author == accountStore.accountData.public_id,
          }"
          style="max-width: 80%; position: relative; overflow: visible"
        >
          <p
            class="text-subtitle-2"
            style="top: -0.8em; position: absolute; z-index: 9999 !important"
          >
            {{
              msg.author == accountStore.accountData.public_id
                ? "Ty"
                : chatsStore.activeChat.profile.name
            }}:
          </p>
          <p class="text-caption">{{ msg.message }}</p>
        </v-card>
      </v-list-item>
    </v-list>
    <!-- Input area -->
    <v-card
      class="d-flex align-center elevation-4 ma-2 pa-0"
      style="
        flex-basis: 5rem;
        flex-shrink: 0;
        overflow: visible;
        position: relative;
      "
    >
      <EmojiPicker
        v-if="showEmoji"
        @emoji_click="handleEmojiClick"
        v-click-outside="clickOutsideEmojiPicker"
        style="position: absolute; bottom: 100%; left: 0"
      ></EmojiPicker>
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
  </div>
</template>

<style lang="scss">
.chat {
  position: relative;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  height: 100%;
  z-index: 2;

  .contact.bar {
    flex-basis: 3rem;
    flex-shrink: 0;
    margin: 1rem;
    box-sizing: border-box;
  }

  .messages {
    flex-grow: 2;
    overflow-y: auto;
    /* Hide scrollbar for Chrome, Safari and Opera */
    &::-webkit-scrollbar {
      display: none;
    }
    scrollbar-width: none; /* Firefox */
  }
}
</style>
