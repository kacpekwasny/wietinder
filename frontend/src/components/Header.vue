<script lang="ts">
import { useUserAccountStore } from '@/stores/AccountDataStore';
import { mapState, storeToRefs } from 'pinia';

export default {
  data() {
    const accountRefs = storeToRefs(useUserAccountStore())
    return {
      loggedInR: accountRefs.loggedIn,
      accountDataR: accountRefs.accountData,
    };
  },

  methods: {

  },

  computed: {
    ...mapState(useUserAccountStore, ['loggedIn', 'accountData'])
  },

  watch: {
    loggedInF() {
      console.log('this.loggedInR', this.loggedInR)
    }
  },

  created() {
    const store = useUserAccountStore()
    store.refreshUserData()
    console.log('AccountData', store.accountData)
  },
};
</script>

<template>
  <v-sheet class="d-flex justify-space-between align-center " width="100%">
    <div class="text-h4">WIETINDER</div>
    <v-card v-if="loggedInR" density="compact" class="mr-4">
      <v-card-title class="text-center pa-1 text-caption">
        <v-icon>mdi-account</v-icon>
        {{ accountDataR.name }}
      </v-card-title>

    </v-card>

  </v-sheet>
</template>
