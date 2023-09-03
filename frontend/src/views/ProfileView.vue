<script lang="ts">
import { useProfilesStore } from "@/stores/ProfilesStore";
import { getJson } from "../common/requests";
import Profile from "../components/Profile.vue";


export default {
  data() {
    return {
      profilesStore: useProfilesStore(),
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
  <Profile :profile-data="profileData"></Profile>
</template>
