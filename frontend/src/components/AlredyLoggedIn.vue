<script lang="ts">
import { useUserAccountStore } from '@/stores/AccountDataStore';
import { getBackendHostname } from '@/common/requests';
import router from '@/router';
import { getJson } from '@/common/requests';
    export default {
        data(){
            return {
            userAccountStore: useUserAccountStore()
            }
        },

        methods: {
            remoteURL(imageName: string) {
                return `${getBackendHostname()}/uploads/${imageName}`;
            },
            async logout() {
                await getJson("/logout");
                useUserAccountStore().setLoggedOut();
                router.push("/login");
            },
        }
    }
</script>

<template>
<v-container fluid class="d-flex flex-column" style="width: fit-content">
  <v-card class="d-flex justify-center align-center flex-column" style="width: fit-content">
    <v-card-title class="text-h6">Aktualnie jesteś zalogowany jako:</v-card-title>
    <v-card-text>
      <v-avatar size="100">
        <v-img :src="remoteURL(this.userAccountStore.accountData.images[0])"/>
      </v-avatar>
      <div class="text-h5 text-cetner ml-4">{{ this.userAccountStore.accountData.name }}</div>
    </v-card-text>
    <div class="text-h6 text-cetner ml-0">Czy chcesz się wylogować?</div>
    
    <v-card class="d-flex justify-center align-center my-3">
        <v-btn @click="logout" color="yellow"><v-icon class="mr-3">mdi-logout</v-icon>Wyloguj</v-btn>
    </v-card>
  </v-card>
</v-container>
</template>