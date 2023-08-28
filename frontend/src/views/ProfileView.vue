<script lang="ts">
import draggable from "vuedraggable";
import { getBackendHostname, getJson, postJson } from "../common/requests";
import Profile from "../components/Profile.vue";
import axios from "axios";
import { profile } from "console";

export default {
  data() {
    return {
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
    const resp = await getJson(`/profile/${this.$route.params.profile_id}`);
    this.profileData = await resp.json();
    console.log(this.profileData);
  },
};
</script>

<template>
  <Profile :profile-data="profileData"></Profile>
</template>
