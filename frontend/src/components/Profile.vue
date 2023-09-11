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
    return {};
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
  },
};
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-card class="pa-2 mb-4 elevation-6" style="position: relative">
      <v-carousel hide-delimiters :show-arrows="shouldShowArrows">
        <v-carousel-item v-for="image in profileData.images" :key="image" eager>
          <v-img :src="remoteURL(image)" height="100%" eager></v-img>
        </v-carousel-item>
      </v-carousel>
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
  </v-container>
</template>
