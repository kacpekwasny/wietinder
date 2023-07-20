<script lang="ts">

export default {

  data() {
    return {
      file: null,
      imageView: null,
      description: '',
      targetSex: [],
      mySex: "",
      overlay: false,
    };
  },
  
  methods: {
    handleFileUpload(event: Event) {
      this.file = event.target.files[0];
    },
    submitForm() {
      const formData = new FormData();
      formData.append('image', this.file);

      fetch('http://localhost:5000/account-data', {
        method: 'POST',
        body: formData
      })
        .then(response => response.json())
        .then(data => {
          console.log(data);
          // Handle the response from the Flask backend
        })
    },

  },
};
</script>

<!-- zrobic zeby zdjecia sie wyswietlaly, check box kogo szukam, piwo/etc, nie widac boxów :(()) -->

<template>
    <v-container class="d-flex flex-column">
      <v-textarea label="Opis profilu" v-model="description"></v-textarea>
      <v-file-input multiple accept="image/png, image/jpeg" label="Dodaj zdjęcia" v-model="file"
        @change="handleFileUpload"></v-file-input>

      <v-container fluid>
        <v-row dense>
          <v-col>
            <v-card class="align-end" height="100%">
              <v-card-title class="text-left">
                Moja płeć:
              </v-card-title>
              <v-card-action>
                <v-radio-group v-model="mySex" column>
                  <v-radio label="Kobieta" color="blue" value="female" density="default"></v-radio>
                  <v-radio label="Mężczyzna" color="blue" value="male" density="default"></v-radio>
                </v-radio-group>
              </v-card-action>
            </v-card>
          </v-col>
          <v-col>
            <v-card class="align-end" height="100%">
              <v-card-title class="text-left">
                Pożądana płeć pary:
              </v-card-title>
              <v-card-action>
                <v-checkbox v-model="targetSex" label="Kobieta" value="female" hideDetails density="compact" class="ml-2"></v-checkbox>
                <v-checkbox v-model="targetSex" label="Mężczyzna" value="male" hideDetails density="compact" class="ml-2"></v-checkbox>
              </v-card-action>
            </v-card>

          </v-col>
        </v-row>
      </v-container>

      <v-btn @click="submitForm">Zapisz zmiany!</v-btn>

    </v-container>
</template>
  
