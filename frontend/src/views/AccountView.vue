<script lang="ts">
import { file } from "@babel/types";
import draggable from "vuedraggable";

export default {
  data() {
    return {
      selectedImages: [],
      imageView: null,
      description: "",
      targetSex: [],
      mySex: "",
      overlay: false,
      rules: [
        (files: File[]) => {
          if (files.length > 9) {
            return "Można dodać maksymalnie 9 zdjęć."
          }
          let MB = 1_024_000;
          for (let f of files) {
            if (f.size > 2 * MB) {
              return `Images should be smaller than 2MB. ${f.name} has size: ${(f.size/MB).toFixed(2)} MB.`;
            }
          }
        }
        
      ]
    };
  },

  methods: {
    addImagesChanged(_: Event) {
      console.log(this.selectedImages);
      this.imagePreviews = this.selectedImages.map((img) => {
        return { img: img, url: URL.createObjectURL(img) };
      });
    },
    submitForm() {
      const formData = new FormData();
      formData.append("image", this.selectedImages);

      fetch("http://localhost:5000/account-data", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          // Handle the response from the Flask backend
        });
    },
    makeURL(file: File) {
      return URL.createObjectURL(file);
    },
  },

  components: {
    draggable,
  },
};
</script>

<!-- zrobic zeby zdjecia sie wyswietlaly, check box kogo szukam, piwo/etc, nie widac boxów :(()) -->

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px;">
      <v-textarea label="Opis profilu" v-model="description"></v-textarea>
      <v-file-input
        chips
        multiple
        :rules="rules"
        prepend-icon="mdi-camera"
        accept="image/*"
        label="Dodaj zdjęcia"
        v-model="selectedImages"
        @change="addImagesChanged"
      ></v-file-input>

      <draggable
        v-model="selectedImages"
        item-key="url"
        group="people"
        style="align-items: center; display: flex; flex-wrap: wrap"
      >
        <!-- Had to mannulay add these style elements copied from https://github.com/vuetifyjs/vuetify/blob/master/packages/vuetify/src/components/VGrid/VGrid.sass
    for the column layout to start working, because when v-row was the parent of draggable,
    draggable became a column of width 2/12 I think, and as such its children became even thinnger :/ -->
        <template #item="{ element: preview }">
          <v-col cols="6" sm="4" class="pa-2">
            <v-card density="compact">
              <v-img :src="makeURL(preview)" max-height="150px"></v-img>
              <div class="text-caption ma-1">
                {{ preview.name }}
              </div>
            </v-card>
          </v-col>
        </template>
      </draggable>
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
                v-model="targetSex"
                label="Kobieta"
                value="female"
                hideDetails
                density="compact"
                class="ml-2"
              ></v-checkbox>
              <v-checkbox
                v-model="targetSex"
                label="Mężczyzna"
                value="male"
                hideDetails
                density="compact"
                class="ml-2"
              ></v-checkbox>
            </v-card-action>
          </v-card>
        </v-col>
      </v-row>
      <v-btn class="mt-2 mb-2" @click="submitForm">Zapisz zmiany!</v-btn>
    </v-container>

</template>
