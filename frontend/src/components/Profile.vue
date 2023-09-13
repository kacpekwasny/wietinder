<script lang="ts">
import { getBackendHostname, getJson } from "@/common/requests";

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
      return `${getBackendHostname()}/uploads/${imageName}`;
    },
    openImageDialog(image) {
      this.imageToShow = image;
      this.imageDialog = true;
    }
  }
};
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-card class="pa-2 mb-4 elevation-6" style="position: relative" min-height="100px">
      
      <v-img :src="remoteURL(profileData.images[0])" max-height="500px" eager></v-img>
      <div class="pa-2" style="position: absolute; bottom: 0; left: 0">
        <div class="text-h4">{{ profileData.name }}</div>
        <div class="text-caption">{{ profileData.bio }}</div>
      </div>
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
    <v-card min-height="100px">
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
            <v-img :src="remoteURL(imageToShow)" max-height="600px" max-width="600px"></v-img>
          </v-card>
        </v-dialog>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>
