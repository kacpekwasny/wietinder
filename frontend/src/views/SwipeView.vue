<script lang="ts">
import Profile from "../components/Profile.vue"
import { useProfilesStore } from "@/stores/ProfilesStore";
import { getJson, postJson} from "../common/requests";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import { createDecipheriv } from "crypto";

export default {
    data() {
        return {
            possibleMatches: [],
            profilesStore: useProfilesStore(),
            accountStore: useUserAccountStore(),
            user2_public_id: "",
            profilesChoiceMade: [],

            profileData: {
                name: "",
                images: [],
                bio: "",
                sex: "",
                fields_of_study: [],
                target_sex: [],
                target_activity: [],
            },
        };
    },

    methods: {
        async loadData() {
            await this.getPossibleMatches();
            this.getRandomPossibleMatchID();
            const p = await this.profilesStore.profile(this.user2_public_id);
            if (p === undefined) {
                this.profileData.name = "404, profile not found";
                this.profileData.bio = "profile with this ID was not found";
                return;
            }
            this.profileData = p;
        },
        async getPossibleMatches(){
            if (this.possibleMatches.length == 0){
                let response = await getJson("/matches-undecided")
                let json = await response.json();
                this.possibleMatches = json
            }
        },
        getRandomPossibleMatchID(){
            this.user2_public_id = this.possibleMatches[Math.floor(Math.random()*this.possibleMatches.length)]
        },
        async updateChoice(choice: String){
            let response = await postJson("/update-match-choice", {
                user2_public_id: this.user2_public_id,
                choice: choice
            })
            this.profilesChoiceMade.push(this.user2_public_id) 
            this.possibleMatches = this.possibleMatches.filter(item => item !== this.user2_public_id);
            this.loadData();
        },

    },

    components: {
        Profile,
    },

    async created() {
        this.loadData();
    }
       
}
</script>

<template>
    <Profile :profile-data="profileData"></Profile>
    <v-bottom-navigation 
        style="height: 60px;"
        :elevation="15"
        grow>
        <v-btn 
        value="dislike" 
        class="mr-4"
        @click = "updateChoice('dislike')"
        >
        <v-icon>mdi-close-circle</v-icon>

        <span>Odrzuć</span>
        </v-btn>

        <v-btn 
        value="like" 
        class="mr-4"
        @click = "updateChoice('like')"
        >
        <v-icon>mdi-heart-circle</v-icon>

        <span>Polub</span>
        </v-btn>
    </v-bottom-navigation>
</template>
  