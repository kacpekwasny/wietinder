<script>
import { ref } from "vue";
import useValidate from "@vuelidate/core"
import { email, required } from "@vuelidate/validators"

import { postJson } from "../common/requests"

const showModal = ref(false);
const errorMessage = ref("");
// const emailField = ref("");
// const passwordField = ref("");
// Mi to nie działało xD w sensie, że kiedy robiłem POST, to wysyłał się pusty string "", mimo, że wpisałem tam mail i hasło
// więc teraz w data() ... zdefiniowałem te pola i w funkcji, która to wysyła nie ma jż emailField.value, tylko this.emailField
// Zmieniłem też nazwę email na emailField, bo importujemy `email` z vuelidate, więc była kolizja nazw.


export default {
  data() {
    return {
      showModal: false,
      v$: useValidate(),
      emailField: "",
      passwordField: "",
    }
  },
  validations() {
    return {
      emailField: { email, required },
      passwordField: { required }
    }
  },
  methods: {
    navigateToRegister() {
      this.$router.push({ path: "/register" });
    },
    submitForm() {
      this.v$.$validate()
      if (!this.v$.$error) {
        postJson("/login",
          { email: this.emailField, password: this.passwordField }
        ).then(response => {
          if (response.status == 200) {
            this.$router.push({ path: "/account" });
          }
          if (response.status == 401) {
            this.showModal = true;
            return this.errorMessage = 'Błędne hasło'
          } else if (response.status == 404) {
            this.showModal = true;
            return this.errorMessage = 'Błędny email'
          }
        })        
      } else {
        this.showModal = true;
        return this.errorMessage = 'Wprowadzony tekst nie jest mejlem!'
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
    <div v-if="showModal" class="overlay">
      <p v-if="errorMessage">{{ errorMessage }}</p>><br>
      <button class="close" @click="showModal = false">Zamknij</button>
    </div>
    <div>
      <p>Masz już konto? Zaloguj się!</p>
      <p>E-mail:</p>
      <input for="email" v-model="emailField" type="email">
      <p>Hasło:</p>
      <input v-model="passwordField" type="password"><br>
      <button class="login" @click="submitForm">Zaloguj</button>
      <p>Nie masz konta? Kliknij <button class="registerButton" @click="navigateToRegister">tutaj!</button></p>
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

.overlay {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 700px;
  height: 500px;
  background-color: rgba(0, 0, 0, 0.77);
  z-index: 10;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.close {
  border: none;
  padding: 10px;
  width: 100px;
  height: 50px;
  cursor: pointer;
  font-size: 20px;
}

h1 {
  color: rgb(109, 134, 166);
  display: flex;
  justify-content: center;
  font-size: 7em;
}

.registerButton {
  border: none;
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
  color: rgb(191, 133, 120);
  background-color: rgb(193, 206, 217);
}
</style>
