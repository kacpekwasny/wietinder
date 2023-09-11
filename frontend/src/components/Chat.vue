<script lang="ts">
import { useChatsListPanelStore } from "@/stores/ChatsListPanelStore";
import { useChatsStore } from "@/stores/ChatsStore";
import { getBackendHostname, postJson } from "@/common/requests";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import EmojiPicker from "@/components/EmojiPicker/EmojiPicker.vue"
import { onMounted } from "vue";
import {state, socket} from '../socket/socket'


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
        this.showEmoji = false;
      }
    },
  },
  mounted() {
    socket.emit('send_message', { content: 'Hello from Vue component!' })
    console.log('emited send messsage')

  },
  setup() {
    onMounted(() => {
    })
  },

  components: {
    EmojiPicker,
  },

  computed: {},
};
</script>

<template>
  <div id="section" v-if="chatsStore.activeChat != null" class="chat">
    <v-card-title id="header">
      <div
        class="contact bar ml-6 ma-1 pa-1 d-flex justify-between align-center elevation-5 rounded-sm"
        @click="navigateToProfile"
        style="cursor: pointer; width: fit-content"
      >
        <v-avatar class="mr-2">
          <v-img
            :src="remoteURL(chatsStore.activeChat.profile.images[0])"
          ></v-img>
        </v-avatar>
        {{ chatsStore.activeChat.profile.name }}
      </div>
    </v-card-title>
    <v-divider></v-divider>
    <v-list class="d-flex scroll-nobar" style="flex-direction: column-reverse">
      <v-list-item
        v-for="msg in chatsStore.activeChat.messages"
        style="overflow-anchor: none"
      >
        <v-card
          class="ma-3 pa-2 elevation-4 rounded-lg"
          :class="{
            'float-right': msg.author == accountStore.accountData.public_id,
          }"
          style="max-width: 80%; position: relative; overflow: visible"
        >
          <p
            class="text-subtitle-2"
            style="
              top: -0.8em;
              left: 0.1rem;
              position: absolute;
            "
          >
            {{
              msg.author == accountStore.accountData.public_id
                ? "Ty"
                : chatsStore.activeChat.profile.name
            }}:
          </p>
          <p class="text-caption">{{ msg.message }}</p>
        </v-card>
        <div style="overflow-anchor: auto; height: 1px"></div>
      </v-list-item>
    </v-list>
    <!-- Input area -->
    <v-card
      class="d-flex align-center elevation-4 ma-2 pa-0"
      style="
        flex-basis: 4.3rem;
        flex-shrink: 0;
        overflow: visible;
        position: relative;
      "
    >
      <EmojiPicker
        v-if="showEmoji"
        @emoji_click="handleEmojiClick"
        v-click-outside="clickOutsideEmojiPicker"
        style="position: absolute; bottom: 100%; right: 0"
      ></EmojiPicker>
      <v-textarea
        prepend-inner-icon="mdi-chat"
        class="ma-2"
        label="Napisz wiadomość"
        rows="1"
        max-rows="8"
        style="width: 40rem"
        auto-grow
        v-model="content"
        hide-details
      ></v-textarea>
      <div class="d-sm-flex flex-row">
        <v-btn
          icon
          class="ma-1 float-right"
          color="yellow"
          float-right
          @click="sendMessage()"
        >
          <v-icon>mdi-send</v-icon>
        </v-btn>
        <v-btn icon class="ma-1 float-right" color="yellow" @click="toggleEmojiPicker">
          <v-icon>mdi-emoticon-happy</v-icon>
        </v-btn>

      </div>
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

  .scroll-nobar {
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
