<script >
import { ref } from "vue";
import useValidate from "@vuelidate/core"
import { email, required, minLength } from "@vuelidate/validators"
import axios from 'axios'
import { postJson } from "../common/requests"

const showModal = ref(false);
const errorMessage = ref("");
const passwordValidationOff = ref(true); 

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
      // descriptionField: '',
      // selectedFile: ['https://kis.agh.edu.pl/wp-content/uploads/2019/09/LOGO2.png']
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
        
        minLength: minLength(9),
        containsUppercase: function(value) {
          return /[A-Z]/.test(value)
        },
        containsLowercase: function(value) {
          return /[a-z]/.test(value)
        },
        containsNumber: function(value) {
          return /[0-9]/.test(value)
        },
        containsSpecial: function(value) {
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
        .then(response =>{
          console.log('udało się')
        })
    },
    submitForm() {
      this.v$.$validate()
      if (this.v$.emailField.$error){
        this.showModal = true;
        return this.errorMessage = 'Błędny email'
      }
      if (this.v$.passwordField.invalid) {
        this.showModal = true;
        return this.errorMessage = 'Sprawdz swoje hasło';
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
            alert(data.message) // nie wiem co to robi, co tu dac modal? - nata
          })
          
        } else {
          this.showModal = true;
          this.errorMessage = "Hasła nie pasują"
        }
      } else {
        this.showModal = true;
        this.errorMessage = "Wszystkie pola wymagane"
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
      <div>
        <div v-if="showModal" class="overlay">
        <p v-if="errorMessage">{{ errorMessage }}</p>><br>
        <button class="close" @click="showModal = false">Zamknij</button>
    </div>
      </div>
      <div id="app" @submit="Login" >
        <p>Imię:</p>
        <input v-model="nameField" type="text" onkeydown="return /[a-z]/i.test(event.key)">
        <p>E-mail:</p>
        <input for="email" v-model="emailField" type="email">
        <p>Hasło:</p>
        <input v-model="passwordField" type="password" novalidate><br>
        <span v-if="v$.passwordField && !v$.passwordField.valid">
          Password contains atleast One Uppercase, One Lowercase, One Number
            and One Special Chacter and must contatain of minimum 9 characters!
        </span>
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
