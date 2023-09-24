<script lang="ts">
import {getJson} from "../common/requests";
import { Profile, useProfilesStore } from "@/stores/ProfilesStore";

export default {
    data() {
        return {
          profilesStore: useProfilesStore(),
          profilesData: [] as Profile[],
        }
    },
    methods: {
        async fetchWhoLikesMe(){
            let response = await getJson("/api/who-likes-me")
            let profilesThatLikeMe: Profile[] =  await response.json();
            this.profilesData = profilesThatLikeMe
            this.profilesStore.addProfilesToCache(profilesThatLikeMe)
        },

        navigateToAccount(userID: string){
          this.$router.push({ path: "/profile/" + userID})
        },
    },

    created() {
        this.fetchWhoLikesMe();
    }
}


</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-card class="pa-2 mt-2 mb-2 elevation-3">

      <div class="text-h5 mb-5 mt-3 text-center">Zobacz kto cię polubił!</div>
      <v-row class="pa-2">
        <v-col
            v-for="profile in profilesData"
              cols="6"
              sm="4"
              class="pa-1"
            >
            <v-card
            @click = "navigateToAccount(profile.public_id)">
            <v-img :src="`http://localhost:5000/api/uploads/${profile.images[0]}`" max-height="150px"> 
            </v-img>
            <div class="text-caption ma-1">
            {{ profile.name }}
            </div>
            </v-card>
        </v-col>
      </v-row>
      </v-card>
  </v-container>
</template>