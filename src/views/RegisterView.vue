<script setup>
  import Header from "../components/Header.vue"
</script>

<template>
    <Header />
    <body>
      <form id="app" @submit="Login" >
        <p>Imię:</p>
        <input v-model="name" type="text">
        <p>Nazwisko:</p>
        <input v-model="lastname" type="text">
        <p>E-mail:</p>
        <input v-model="email" type="text">
        <p>Numer telefonu:</p>
        <input v-model="number" type="text">
        <p>Login:</p>
        <input v-model="login" type="text">
        <p>Hasło:</p>
        <input v-model="password" type="text">
        <p>Swój opis:</p>
        <input class="description" v-model="password" type="text">
      </form>
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
</style>
