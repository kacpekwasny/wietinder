<script lang="ts">
import Profile from "../components/Profile.vue"
import { useProfilesStore } from "@/stores/ProfilesStore";
import { getJson, postJson} from "../common/requests";
import { useUserAccountStore } from "@/stores/AccountDataStore";

export default {
    data() {
        return {
            possibleMatches: [],
            profilesStore: useProfilesStore(),
            accountStore: useUserAccountStore(),
            other_user_public_id: "",
            profilesChoiceMade: [] as string[],
            noPossibleMatches: false as boolean,

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
            const p = await this.profilesStore.profile(this.other_user_public_id);
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
                if (this.possibleMatches.length==0){
                    this.noPossibleMatches = true
                } else {
                    this.noPossibleMatches = false
                }
            }
        },

        getRandomPossibleMatchID(){
            this.other_user_public_id = this.possibleMatches[Math.floor(Math.random()*this.possibleMatches.length)]
        },

        async updateChoice(choice: string) {
            postJson("/update-match-choice", {
                other_user_public_id: this.other_user_public_id,
                my_choice: choice
            })
            this.profilesChoiceMade.push(this.other_user_public_id) 
            this.possibleMatches = this.possibleMatches.filter(item => item !== this.other_user_public_id);
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
    <v-card-text class="text-h4 mt-3 text-center"> Swipe </v-card-text>
    <v-card class="text-cetner" v-if="noPossibleMatches">
        <v-alert
        icon="mdi-information"
        dense
        outlined
        class="d-flex align-center justify-center"
       
        >
        Nie mamy więcej propozycji dla ciebie. Wróć po więcej później.
        </v-alert>
    </v-card>
    <v-card v-else>
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
    </v-card>
</template>
  