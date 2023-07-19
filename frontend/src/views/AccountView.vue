<script>
import Header from "../components/Header.vue"
export default {
  components: {
    Header
  },
  data() {
    return {
      file: null,
      imageView: null,
      description: '',
      targetSex: [], 
    };
  },
  methods: {
    handleFileUpload(event) {
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
  <v-layout>
    <v-app-bar>
      <Header />
    </v-app-bar>
    <v-main>
      <v-checkbox label="Checkbox"></v-checkbox>
      <v-form class="px-3">
        <v-text-field label="Opis" v-model="description"></v-text-field>
        <v-file-input multiple accept="image/png, image/jpeg" label="Dodaj zdjęcia" v-model="file"
          @change="handleFileUpload"></v-file-input>
        <button @click="submitForm">Upload</button>

        <v-item-group multiple>
          <v-container>
            <v-row>
              <v-col>
                <v-checkbox v-model="targetSex" label="Mężczyzna" value="male"></v-checkbox>
              </v-col>
              <v-col>
                <v-checkbox v-model="targetSex" label="Kobieta" value="female"></v-checkbox>
              </v-col>
            </v-row>
          </v-container>
        </v-item-group>
      </v-form>
    </v-main>
  </v-layout>
</template>
  
