<script lang="ts">
import { useUserAccountStore } from '@/stores/AccountDataStore';
import { mapState, storeToRefs } from 'pinia';

export default {
  data() {
    return {}
  },

  methods: {

  },

  computed: {
    ...mapState(useUserAccountStore, ['loggedIn', 'accountData'])
  },

  async created() {
    const store = useUserAccountStore()
    console.log('Header before refresh', this.accountData, `loggedIn ${this.loggedIn}`)
    await store.refreshUserData()
    console.log('Header after refresh', this.accountData, `loggedIn ${this.loggedIn}`)
  },
};
</script>

<template>
  <v-sheet class="d-flex justify-space-between align-center " width="100%">
    <div class="text-h4 ml-3">WIETINDER</div>
    <v-card v-if="loggedIn" density="compact" class="mr-4">
      <v-card-title class="text-center pa-1 text-caption">
        <v-icon>mdi-account</v-icon>
        {{ accountData.name }}
      </v-card-title>
    </v-card>

  </v-sheet>
</template>
