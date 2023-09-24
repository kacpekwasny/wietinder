<script lang="ts">
import { useProfilesStore, Profile as ProfileInterface } from "@/stores/ProfilesStore";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import { getJson } from "../common/requests";
import Profile from "../components/Profile.vue";

export default {
  data() {
    return {
      profilesStore: useProfilesStore(),
      accountDataStore: useUserAccountStore(),
      profileData: {
        name: "",
        public_id: "",
        images: [] as string[],
        bio: "",
        sex: "",
        fields_of_study: [] as string[],
        target_sex: [] as string[],
        target_activity: [] as string[],
      } as ProfileInterface,
    };
  },

  methods: {

  },

  components: {
    Profile,
  },

  async created() {
    const p = await this.profilesStore.profile(this.$route.params.profile_id)
    if (p === undefined) {
      this.profileData.name = "404, profile not found"
      this.profileData.bio = "profile with this ID was not found"
      return
    }
    this.profileData = p
  },
};
</script>

<template>
  <Profile :profile-data="profileData" :likeable="profileData.public_id !== accountDataStore.accountData.public_id"></Profile>
</template>
