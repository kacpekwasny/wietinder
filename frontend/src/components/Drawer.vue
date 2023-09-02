<script lang="ts">
export default { 
    data() {
      return {
        showSidePanel: true,
      };
    },
    
    methods:{
      toggleSidePanel() {
        this.showSidePanel = !this.showSidePanel;
      },
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

