<script >

import useValidate from "@vuelidate/core"
import { email, required } from "@vuelidate/validators"
import axios from 'axios'
import { postJson } from "../common/requests"

export default {
  data() {
    return {
      v$: useValidate(),
      nameField: '',
      lastnameField: '',
      emailField: '',
      numberField: '',
      passwordField: '',
      confirmPasswordField: '',
      descriptionField: '',
      selectedFile: ['https://kis.agh.edu.pl/wp-content/uploads/2019/09/LOGO2.png']
      //tu trzeba jakos zrobic zeby sie zdjecia zapisywaly i wysietlay potem
    }
  },
  validations() {
    return {
      emailField: {
        email,
        required
      },
      passwordField: {
        required,
      },
      confirmPasswordField: {
        required,

        },
      nameField: {
        required, 
      }
    }
  },
    methods: {
      onFileSelected(event) {
        this.selectedFile = event.target.files[0]
      },
      onUpload() {
        const fd = new FormData();
        fd.append('image', this.selectedFile, this.selectedFile.name)
        axios.post('link do bazy?')
          .then(response =>{
            console.log('udało się')
          })
      },
      submitForm() {
        this.v$.$validate()
        if (this.v$.emailField.$error){
          return alert("Podaj poprawny email")
        }
        if (!this.v$.$error) {
          // TODO: Należy najpierw wysłać do backendu to co użytkownik wprowadził w celu utworzenia konta.
          // Backend zwaliduje, czy nie istnieje już konto z takim mailem,
          // czy hasło jest git.
          // Potem backend odeśle odpowiedź i albo będzie git, albo coś będzie źle, i tą informacje będzie trzeba
          // użytkownikowi przedstawić.
          if (this.passwordField == this.confirmPasswordField){
            postJson("/register",
            { name: this.nameField,  
              email: this.emailField,   
              password: this.passwordField, 
            }).then(response => {
              if (response.status == 200){
                this.$router.push({ path: "/account" });
                return response.json()
              } else if (response.status == 400){
                return response.json()
              }
            }).then(data =>{
              alert(data.message)
            })
            
          } else {
            alert("Hasła nie pasują")
          }
        } else {
          alert("Wszystkie pola wymagane")
        }
      }
    }
  }

</script>


<template>
    <header>
      <h1>WIETINDER</h1>
    </header>
    <body>
      <div id="app" @submit="Login" >
        <p>Imię:</p>
        <input v-model="nameField" type="text" onkeydown="return /[a-z]/i.test(event.key)">
        <p>E-mail:</p>
        <input for="email" v-model="emailField" type="email">
        <p>Hasło:</p>
        <input v-model="passwordField" type="password">
        <p>Potwierdź hasło:</p>
        <input v-model="confirmPasswordField" type="password"><br>
        <button class="register" @click="submitForm">Zarejestruj</button>
        
      
        <!-- <p>Dodaj zdjęcia</p><br>
        <input type="file" @change="onFileSelected"/> --> -->
      <!-- <button @click="onUpload">Dodaj</button> -->

        <div class="row">
          <img v-for="img in selectedFile" v-bind:src="img"/>
        </div>
      </div>
    </body>
</template>

<style>
body {
  display: block;
  margin-left: auto;
  margin-right: auto;
  align-items: center;
  width: 100%;
  background-color: rgb(193, 206, 217);
  text-align: center;
}


input {
  width: 300px;
  height: 40px;
}

p {
  font-size: larger;
  color: rgb(191, 133, 120);
}

.description {
  width: 300px;
  height: 100px;
}

h1 {
  color: rgb(109, 134, 166);
  display: flex;
  justify-content: center;
  font-size: 7em;
}
</style>
