<template>
    <div>
      <input type="file" ref="fileInput" @change="handleFileUpload">
      <button @click="submitForm">Upload</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        file: null
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