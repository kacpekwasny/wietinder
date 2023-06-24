<script setup>
  import {ref} from "vue";
  import Header from "../components/Header.vue";
  import {useRouter} from "vue-router";

  const router = useRouter();
  const showModal = ref(false);
  const errorMessage = ref("");
  const email = ref("");

  const navigateToRegister = () => {
    router.push(`/register`)
  }

  const log = () => {
    // // if(email != in data) {
    //   return errorMessage.value = "Nie istnieje konto zarejestrowane na ten e-mail!"
    // }
    if(email.value.includes(!("@"))){
      console.log("dupa")
      showModal.value = true;
      return errorMessage.value = "Nie istnieje konto zarejestrowane na ten e-mail!"
    }
    
    router.push(`/account`)
  }
</script>

<template>
    <Header />
    <body>
      <div v-if="showModal" class="overlay">
        <p v-if="errorMessage">{{ errorMessage }}</p>>
        <button class="close" @click="showModal = false">Zamknij</button>
      </div>
      <div>
        <p>Masz już konto? Zaloguj się!</p>
          <p>E-mail:</p>
          <input v-model="email" type="text">
          <p>Hasło:</p>
          <input v-model="password" type="text"><br>
          <button class="login" @click="log">Zaloguj</button>
          <p>Nie masz konta? Kliknij <button @click="navigateToRegister">tutaj!</button></p>
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
    width: 300px;
    height: 300px;
    background-color: rgba(0, 0, 0, 0.77);
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
  }

 .close {
    border: none;
    padding: 10px;
    width: 100px;
    height: 50px;
    cursor: pointer;
    font-size: 20px;
 }
</style>
