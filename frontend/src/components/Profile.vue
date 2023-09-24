<script lang="ts">
import { getBackendHostname, getJson, postJson } from "@/common/requests";

export default {
  props: {
    profileData: {
      type: Object,
      default: {
        name: "",
        images: [],
        bio: "",
        sex: "",
        fields_of_study: [],
        target_sex: [],
        target_activity: [],
      },
    },
    likeable: {
      type: Boolean,
      default: false,
    },
  },

  data() {
    return {
      imageDialog: false,
      currentImageIndex: null,
      imageToShow: "",
    };
  },

  async created() {},
  computed: {
    details() {
      const isMale = this.profileData.sex === "male";

      const items = [
        {
          key: "Płeć",
          chips: [
            {
              text: isMale ? "mężczyzna" : "kobieta",
              icon: isMale ? "mdi-human-male" : "mdi-human-female",
            },
          ],
        },
        {
          key: "Cel",
          chips: this.profileData.target_activity.map((v) => ({ text: v })),
        },
        {
          key: "Płeć pary",
          chips: this.profileData.target_sex.map((v) => ({ text: v })),
        },
        {
          key: "Kierunki",
          chips: this.profileData.fields_of_study.map((v) => ({ text: v })),
        },
      ];
      return items;
    },
    shouldShowArrows() {
      return this.profileData.images.length > 1 ? true : false;
    },
  },
  methods: {
    backendHostname() {
      return getBackendHostname();
    },

    remoteURL(imageName: string) {
      return `${getBackendHostname()}/api/uploads/${imageName}`;
    },
    openImageDialog(image) {
      this.imageToShow = image;
      this.imageDialog = true;
    },

    async updateChoice(choice: string) {
      postJson("/api/update-match-choice", {
        other_user_public_id: this.profileData.public_id,
        my_choice: choice,
      });
      // this.profilesChoiceMade.push(this.other_user_public_id);
      // this.possibleMatches = this.possibleMatches.filter(
      //   (item) => item !== this.other_user_public_id
      // );
      // this.loadData();
    },
  },
};
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-card class="pa-2 mb-4 elevation-6" min-height="100px">
      <v-card-item style="position: relative">
        <v-img
          :src="remoteURL(profileData.images[0])"
          max-height="500px"
        ></v-img>
        <div class="pa-2" style="position: absolute; bottom: 0; left: 0">
          <div class="text-h4">{{ profileData.name }}</div>
          <div class="text-caption">{{ profileData.bio }}</div>
        </div>
      </v-card-item>
      <v-card-actions v-if="likeable" class="d-flex flex-row justify-center">
        <v-btn
          value="dislike"
          variant="outlined"
          class="mr-4"
          @click="updateChoice('dislike')"
        >
          <v-icon class="ma-1">mdi-close-circle</v-icon>

          <span>Odrzuć</span>
        </v-btn>

        <v-btn
          value="like"
          variant="elevated"
          color="pink"
          @click="updateChoice('like')"
        >
          <v-icon class="ma-1">mdi-heart-circle</v-icon>

          <span>Polub</span>
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-expansion-panels>
      <v-expansion-panel>
        <v-table>
          <tbody>
            <tr v-for="item in details">
              <td>{{ item.key }}</td>
              <td>
                <v-chip-group>
                  <v-chip v-for="chip in item.chips">
                    <v-icon v-if="chip.icon">{{ chip.icon }}</v-icon>
                    {{ chip.text }}
                  </v-chip>
                </v-chip-group>
              </td>
            </tr>
          </tbody>
        </v-table>
      </v-expansion-panel>
    </v-expansion-panels>
    <v-card min-height="100px" class="mb-15">
      <v-card-title>Zdjęcia</v-card-title>
      <v-row class="pa-2">
        <v-col
          v-for="(image, index) in profileData.images"
          cols="6"
          sm="4"
          class="pa-2"
        >
          <v-card @click="openImageDialog(image)" class="cursor-pointer">
            <v-img :src="remoteURL(image)" max-height="150px"></v-img>
          </v-card>
          <v-dialog v-model="imageDialog" max-width="600px" max-height="600px">
            <v-card>
              <v-img
                :src="remoteURL(imageToShow)"
                max-height="600px"
                max-width="600px"
              ></v-img>
            </v-card>
          </v-dialog>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>
