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
      console.log(items);
      return items;
    },
    backendHostname() {
      return getBackendHostname();
    },
  },
};
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-card class="pa-2 mb-4 elevation-6">
      <v-img
        :src="`http://localhost:5000/uploads/${profileData.images[0]}`"
        max-height="480px"
        class="align-end"
      >
        <div class="text-h4">{{ profileData.name }}</div>
        <div class="text-caption">{{ profileData.bio }}</div>
      </v-img>
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
