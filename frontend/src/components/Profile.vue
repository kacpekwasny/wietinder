<script lang="ts">
import { getJson } from "@/common/requests";

export default {
  props: ["profile_id"],

  data() {
    return {
      prof: {
        name: [],
        images: [],
        bio: "",
        sex: "",
        fields_of_study: [],
        target_sex: [],
        target_activity: [],
      },
    };
  },

  async created() {
    let r = await getJson(`/profile/${this.profile_id}`);
    if (r.status != 200) {
        this.prof.name = "404"
        this.prof.bio = "No such user was found."
    }
    this.prof = await r.json();
  },
  computed: {
    details() {
        return [
            ["Płeć", "mężczyzna" ? this.sex === "male" : "kobieta"],
            ["Cel", this.target_activity],
        ]
    }
  }
};
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    
    <v-text-h4>{{ prof.name }}</v-text-h4>
    <text-caption>{{ prof.bio }}</text-caption>
    <v-expansion-panels>
        <v-expansion-panel>
            <v-table>
                <tbody>
                    <tr
                        v-for="(key_val) in [
                          ['Płeć', prof.sex],
                          ['Czynność', prof.target_activity],
                          ['Płeć pary', prof.target_sex],
                          ['Kierunki', prof.fields_of_study],
                        ]"
                    >
                      <td>{{ key_val[0] }}</td>
                      <td>{{ key_val[1] }}</td>
                    </tr>
                </tbody>
            </v-table>
        </v-expansion-panel>
    </v-expansion-panels>

    <v-col cols="6" sm="4" class="pa-2">
      <v-card density="compact">
        <v-img src="/" max-height="150px"></v-img>
      </v-card>
    </v-col>
    <v-row dense>
      <v-col col="6">
        <v-card class="align-end" height="100%">
          <v-card-title class="text-left"> Moja płeć: </v-card-title>
          <v-card-action>
            <v-radio-group v-model="mySex" column>
              <v-radio
                label="Kobieta"
                color="blue"
                value="female"
                density="default"
              ></v-radio>
              <v-radio
                label="Mężczyzna"
                color="blue"
                value="male"
                density="default"
              ></v-radio>
            </v-radio-group>
          </v-card-action>
        </v-card>
      </v-col>
      <v-col col="6">
        <v-card class="align-end" height="100%">
          <v-card-title class="text-left"> Pożądana płeć pary: </v-card-title>
          <v-card-action>
            <v-checkbox
              v-model="prof.target_sex"
              label="Kobieta"
              value="female"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
            <v-checkbox
              v-model="prof.target_sex"
              label="Mężczyzna"
              value="male"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
          </v-card-action>
        </v-card>
      </v-col>
      <v-col col="6">
        <v-card class="align-end" height="100%">
          <v-card-title class="text-left"> Czynność: </v-card-title>
          <v-card-action>
            <v-checkbox
              v-model="prof.target_activity"
              label="Na piwo"
              value="beer"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
            <v-checkbox
              v-model="prof.target_activity"
              label="Na życie"
              value="life"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
            <v-checkbox
              v-model="prof.target_activity"
              label="Do projektu"
              value="project"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
          </v-card-action>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
