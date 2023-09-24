<script lang="ts">
import Profile from "../components/Profile.vue";
import { useProfilesStore } from "@/stores/ProfilesStore";
import { getJson, postJson } from "../common/requests";
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
      if (this.noPossibleMatches) {
        return;
      }
      const p = await this.profilesStore.profile(this.other_user_public_id);
      if (p === undefined) {
        this.profileData.name = "404, profile not found";
        this.profileData.bio = "profile with this ID was not found";
        return;
      }
      this.profileData = p;
    },

    async getPossibleMatches() {
      if (this.possibleMatches.length == 0) {
        let response = await getJson("/api/matches-undecided");
        let json = await response.json();
        this.possibleMatches = json;
      }
    },

    getRandomPossibleMatchID() {
      this.other_user_public_id =
        this.possibleMatches[
          Math.floor(Math.random() * this.possibleMatches.length)
        ];
    },

  },

  components: {
    Profile,
  },

  async created() {
    this.loadData();
  },
};
</script>

<template>
  <v-card class="text-cetner pa-4" v-if="possibleMatches.length === 0">
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
    <Profile :profile-data="profileData" :likeable="true"></Profile>
  </v-card>
</template>
