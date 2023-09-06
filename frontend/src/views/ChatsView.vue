<script lang=ts>
import { getJson } from "../common/requests";
import { useProfilesStore } from "@/stores/ProfilesStore";
import ChatsList from "@/components/ChatsList.vue";
import Chat from "@/components/Chat.vue";


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
        };
    },
    methods: {
        async loadData() {
            let resp = await getJson("/my-matches");
            let json = await resp.json();
            this.matchesID = json;
        },
        async getUserData(userID: string) {
            const p = await this.profilesStore.profile(userID);
            if (p === undefined) {
                this.profileData.name = "404, profile not found";
                this.profileData.bio = "profile with this ID was not found";
                return;
            }
            this.profileData = p;
        },
    },
    components: { ChatsList, Chat }
}
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <ChatsList></ChatsList>
    <v-card class="pa-0">
      <Chat></Chat>
    </v-card>
  </v-container>
</template>