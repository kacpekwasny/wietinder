<script>
import Header from "../components/Header.vue"
export default {
  components: {
    Header
  },
  data() {
    return {
      file: null,
      description: ''
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

<template>
  <v-layout> 
    <v-app-bar><Header /></v-app-bar>
    <v-main>
        <v-form class="px-3">
          <v-text-field label="Opis" v-model="description"></v-text-field>
        </v-form>
      <input type="file" ref="fileInput" @change="handleFileUpload">
      <button @click="submitForm">Upload</button>
    </v-main>
  </v-layout>
</template>
  
