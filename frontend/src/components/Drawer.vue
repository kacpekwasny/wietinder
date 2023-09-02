<script lang="ts">

import { usePanelStore } from "../stores/SidePanelStore";

export default { 
  data() {
    return {panelStore: usePanelStore()}
  },
  methods: {
    toggleSidePanel() {
      this.panelStore.toggleSidePanel();
    },
  },
  computed: {
    showSidePanel: {
      get() {
        return this.panelStore.showSidePanel
      },
      set(newValue: boolean) {
        usePanelStore().$patch({showSidePanel: newValue})
      }
    }
  },
};
</script>

<template>
    <v-navigation-drawer
      v-model="showSidePanel"
      temporary
      :permanent="$vuetify.display.width > 1100"
      class = "drawer"
    >
      <v-list>
        <v-list-item :to="{ name: 'login'}">
          <v-list-item-icon>
            <v-icon>mdi-home</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <!-- Add more menu items as needed -->
      </v-list>
    </v-navigation-drawer>
</template>

