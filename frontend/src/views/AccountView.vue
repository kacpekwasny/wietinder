<script lang="ts">
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
    }
  },

  components: {
    draggable,
  },
};
</script>

<!-- zrobic zeby zdjecia sie wyswietlaly, check box kogo szukam, piwo/etc, nie widac boxów :(()) -->

<template>
  <v-container class="d-flex flex-column">
    <v-textarea label="Opis profilu" v-model="description"></v-textarea>
    <v-file-input
      chips
      multiple
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
        <v-col cols="6" sm="4" md="3" lg="2">
          <v-card class="ma-4">
            <v-img :src="makeURL(preview)" height="125"></v-img>
            <v-card-text class="text-caption">
              {{ preview.name }}
            </v-card-text>
          </v-card>
        </v-col>
      </template>
    </draggable>

    <v-container fluid>
      <v-row dense>
        <v-col>
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
        <v-col>
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
    </v-container>

    <v-btn @click="submitForm">Zapisz zmiany!</v-btn>
  </v-container>
</template>
