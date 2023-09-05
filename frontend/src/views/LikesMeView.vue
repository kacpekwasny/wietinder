<script lang="ts">
import {getJson} from "../common/requests";
import { useProfilesStore } from "@/stores/ProfilesStore";

export default {
    data() {
        return {
          profilesStore: useProfilesStore(),
          usersWhoLikesMe: [],
          profileData: {
              name: "" as string,
              images: [] as string[],
              bio: "" as string,
              sex: "" as string,
              fields_of_study: [] as string[],
              target_sex: [] as string[],
              target_activity: [] as string[],
          },
          profilesData: [],
        }
    },
    methods: {
        async loadData(){
            this.profilesData = [];
            let response = await getJson("/who-likes-me")
            let json =  await response.json();
            this.usersWhoLikesMe = json

            for(let user of this.usersWhoLikesMe){
              await this.getUserData(user);
              this.profilesData.push(this.profileData)
            }  
        },
        async getUserData(userID: string){
          const p = await this.profilesStore.profile(userID);
            if (p === undefined) {
                this.profileData.name = "404, profile not found";
                this.profileData.bio = "profile with this ID was not found";
                return;
            }
            this.profileData = p;
        },
        navigateToAccount(userID: string){
          this.$router.push({ path: "/profile/" + userID})
        },
    },

    created(){
        this.loadData();
    }
}


</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-card class="pa-2 mt-2 mb-2 elevation-3">

      <div class="text-h5 mb-5 mt-3 text-center">Zobacz kto cię polubił!</div>
      <v-row class="pa-2">
        <v-col
            v-for="(profile, index) in profilesData"
              cols="6"
              sm="4"
              class="pa-1"
            >
            <v-card
            @click = "navigateToAccount(profile.public_id)">
            <v-img :src="`http://localhost:5000/uploads/${profile.images[0]}`" max-height="150px"> 
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