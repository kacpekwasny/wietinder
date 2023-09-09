<script lang="ts">
import AccountSettings from '@/components/AccountSettings.vue';
import Profile from '@/components/Profile.vue'
import { useProfilesStore } from "@/stores/ProfilesStore";
import { useUserAccountStore } from '@/stores/AccountDataStore';


export default {
  data() {
    return{
      showProfile: false as boolean,

      profilesStore: useProfilesStore(),
      userAccountStore: useUserAccountStore(),
      
      profileData: {
        name: "",
        images: [],
        bio: "",
        sex: "",
        fields_of_study: [],
        target_sex: [],
        target_activity: [],
      },
    }
  },

  methods: {
    changeView(){
      this.showProfile = !this.showProfile
      
    },

    async getProfileData() {
      const p = await this.profilesStore.profile(this.userAccountStore.accountData.public_id)
      if (p === undefined) {
        this.profileData.name = "404, profile not found"
        this.profileData.bio = "profile with this ID was not found"
        return
      }
      this.profileData = p
    }
  },

  created() {
    this.getProfileData();
  },

  components: {
    AccountSettings,
    Profile,
  },
};
</script>

<!-- zrobic zeby zdjecia sie wyswietlaly, check box kogo szukam, piwo/etc, nie widac boxów :(()) -->

<template>
  <v-btn
  class="v-btn--floating-action v-btn--fab v-btn--fixed ml-2 "
  color="yellow"
  @click = "changeView"
  style="position:fixed, relative; bottom: 10px; z-index: 999;"
  >
    <v-icon v-if = "showProfile">mdi-account-cog</v-icon>
    <v-icon v-else>mdi-account</v-icon>
  </v-btn>

  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <Profile :profile-data="profileData" v-if="showProfile"></Profile>
    <AccountSettings v-else></AccountSettings>
  </v-container>
</template>

