<script setup>
import { ref } from "vue";
import Header from "../components/Header.vue";
import { useRouter } from "vue-router";
import useValidate from "@vuelidate/core"
import { email, required } from "@vuelidate/validators"


const router = useRouter();
const showModal = ref(false);
const errorMessage = ref("");
const email = ref("");
const password = ref("");

const navigateToRegister = () => {
  router.push(`/register`)
}

const log = () => {
  if (email.value.includes(("@"))) {
    fetch(import.meta.env.VITE_API_URL+"/login",
      {
        method: "POST", headers: {
          "Content-Type": "application/json",
          // 'Content-Type': 'application/x-www-form-urlencoded',
        }, body: JSON.stringify({ email: email.value, password: password.value })
      }).then(response => {
        if (!response.ok) {
          throw new Error('Request failed');
        }
        return response.json();
      })
      .then(login => {
        if (login.status == "failure"){
          showModal.value = true;
          return errorMessage.value = "Błędny login lub hasło"
        } else{
          router.push(`/account`)
        }
      })
  } else {
    showModal.value = true;
    return errorMessage.value = "Nie istnieje konto zarejestrowane na ten e-mail!"
  }


}
</script>

<template>
  <Header />

  <body>
    <div v-if="showModal" class="overlay">
      <p v-if="errorMessage">{{ errorMessage }}</p>><br>
      <button class="close" @click="showModal = false">Zamknij</button>
    </div>
    <div>
      <p>Masz już konto? Zaloguj się!</p>
      <p>E-mail:</p>
      <input v-model="email" type="text">
      <p>Hasło:</p>
      <input v-model="password" type="text"><br>
      <button class="login" @click="log">Zaloguj</button>
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

.registerButton {
  border: none;
  font-weight: bold;
  text-decoration: underline;
  cursor: pointer;
  color: rgb(191, 133, 120);
  background-color: rgb(193, 206, 217);
}</style>
