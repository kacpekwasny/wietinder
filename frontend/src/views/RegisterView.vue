<script >
import { ref } from "vue";
import useValidate from "@vuelidate/core"
import { email, required, minLength } from "@vuelidate/validators"
import axios from 'axios'
import { postJson } from "../common/requests"

const showModal = ref(false);
const errorMessage = ref("");
const VALIDATION_OFF = String(import.meta.env.VITE_IS_PRODUCTION).toLowerCase() === "false"

// novalidate.value = passwordValidationOff; //ogolnie to novalidate jest wpisane w html przy passwordField i powinno usuwac te ograniczenia

export default {
  data() {
    return {
      showModal: false,
      v$: useValidate(),
      nameField: '',
      lastnameField: '',
      emailField: '',
      numberField: '',
      passwordField: '',
      confirmPasswordField: '',
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

        minLength: minLength(9),
        containsUppercase(value) {
          return /[A-Z]/.test(value)
        },
        containsLowercase(value) {
          return /[a-z]/.test(value)
        },
        containsNumber(value) {
          return /[0-9]/.test(value)
        },
        containsSpecial(value) {
          return /[#?!@$%^&*-]/.test(value)
        },
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
        .then(response => {
          console.log('udało się')
        })
    },
    submitForm() {
      this.v$.$validate()
      // This is PROD (not DEV), and we will be validating fields
      // To jest PROD (nie DEV), więc będziemy sprawdzać poprawność pul, które wypełnił użytkownik
      if (VALIDATION_OFF) {
        // sprawdzamy czy na email jest blad
        if (this.v$.emailField.$error) {
          this.showModal = true;
          return this.errorMessage = 'Błędny email'
        }

        // sprawdzamy czy na hasle jest blad
        if (this.v$.passwordField.invalid) {
          this.showModal = true;
          return this.errorMessage = 'Sprawdz swoje hasło';
        }
        
        if (this.passwordField != this.confirmPasswordField) {
          this.showModal = true;
          this.errorMessage = "Hasła nie pasują"
        } 

        if (this.v$.$error) {
          this.showModal = true;
          this.errorMessage = "Nastąpił jakiś błąd"
          return;
        }

        // TODO: czy sprawdzilismy wszystkie mozliwosci błędu???
      }
      
      // Bylo kilka ifow, ktore by zrobil return, gdyby cos bylo zle.
      // wszystko jest git, wiec wysylamy requesta.
      postJson("/register",
        {
          name: this.nameField,
          email: this.emailField,
          password: this.passwordField,
        }).then(response => {
          if (response.status == 200) {
            this.$router.push({ path: "/account" });
            return response.json()
          } else if (response.status == 400) {
            return response.json()
          }
        }).then(data => {
          alert(data.message) // nie wiem co to robi, co tu dac modal? - nata
        })
    }
  }
}
</script>


<template>
  <header>
    <h1>WIETINDER</h1>
  </header>

  <body>
    <div>
      <div v-if="showModal" class="overlay">
        <p v-if="errorMessage">{{ errorMessage }}</p>><br>
        <button class="close" @click="showModal = false">Zamknij</button>
      </div>
    </div>
    <div id="app" @submit="Login">
      <p>Imię:</p>
      <input v-model="nameField" type="text" onkeydown="return /[a-z]/i.test(event.key)">
      <p>E-mail:</p>
      <input for="email" v-model="emailField" type="email">
      <p>Hasło:</p>
      <input v-model="passwordField" type="password"><br>
      <span v-if="v$.passwordField && !v$.passwordField.valid">
        Password contains atleast One Uppercase, One Lowercase, One Number
        and One Special Chacter and must contatain of minimum 9 characters!
      </span>
      <p>Potwierdź hasło:</p>
      <input v-model="confirmPasswordField" type="password"><br>
      <button class="register" @click="submitForm">Zarejestruj</button>


      <div class="row">
        <img v-for="img in selectedFile" v-bind:src="img" />
      </div>
    </div>
  </body>
</template>

<style>
</style>
