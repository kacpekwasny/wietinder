<script lang=ts>
import { getJson } from "../common/requests";
import { useProfilesStore } from "@/stores/ProfilesStore";


export default {
    data() {
        return {
            matchesID: [] as string[],
            profilesStore: useProfilesStore(),

            profileData: {
              name: "" as string,
              images: [] as string[],
              bio: "" as string,
              sex: "" as string,
              fields_of_study: [] as string[],
              target_sex: [] as string[],
              target_activity: [] as string[],
          },
        }
    },
    methods: {
        async loadData(){
            let resp = await getJson("/get_matches")
            let json = await resp.json()
            this.matchesID = json
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
    },
    created(){
        this.loadData();
    }
}
</script>

<template>
    
</template>