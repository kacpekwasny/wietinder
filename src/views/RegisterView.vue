<script >
  import { useRouter } from "vue-router";
  import useValidate from "@vuelidate/core"
  import { email, required } from "@vuelidate/validators"

  export default {
    data() {
      return {
        v$: useValidate(),
        email: '',
      }
    },
    validations() {
      return {
        email: {email, required},
      }
    },
    methods: {
      submitForm() {
        this.v$.$validate() 
        if (!this.v$.$error) {
          this.$router.push({ path: "/account" });
        } else {
          alert("Brakuje mejla")
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
      <form id="app" @submit="Login" >
        <p>Imię:</p>
        <input v-model="name" type="text">
        <p>Nazwisko:</p>
        <input v-model="lastname" type="text">
        <p>E-mail:</p>
        <input for="email" v-model="email" type="email">
        <p>Numer telefonu:</p>
        <input v-model="number" type="text">
        <p>Login:</p>
        <input v-model="login" type="text">
        <p>Hasło:</p>
        <input v-model="password" type="text">
        <p>Swój opis:</p>
        <input class="description" v-model="password" type="text"><br>
        <button type="submit" @click="submitForm">Zarejestruj</button>
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

  h1 {
    color: rgb(109, 134, 166);
    display: flex;
    justify-content: center;
    font-size: 7em;
  }
</style>
