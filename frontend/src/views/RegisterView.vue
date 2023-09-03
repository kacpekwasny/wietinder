<script lang="ts">
import { ref } from "vue";
import useValidate from "@vuelidate/core";
import { email, required, minLength, sameAs } from "@vuelidate/validators";
import axios from "axios";
import { postJson } from "../common/requests";

const showModal = ref(false);
const errorMessage = ref("");
const VALIDATION_OFF =
  String(import.meta.env.VITE_IS_PRODUCTION).toLowerCase() === "false";

// novalidate.value = passwordValidationOff; //ogolnie to novalidate jest wpisane w html przy passwordField i powinno usuwac te ograniczenia

export default {
  data() {
    return {
      showModal: false,
      v$: useValidate(),

      nameField: "",
      lastnameField: "",
      emailField: "",
      passwordField: "",
      confirmPasswordField: "",
      nameServerErrors: [],
      emailServerErrors: [],
      passwordServerErrors: [],
      confirmPasswordServerErrors: [],

    };
  },
  validations() {
    return {
      emailField: {
        email,
        required,
      },
      passwordField: {
        required,

        minLength: minLength(8),
      },
      confirmPasswordField: {
        required,
        // sameAsPassword: sameAs(sameAs(function() {
        //     return this.passwordField;
        //   }))   //nie wiem czemu nie chce to działać
      },
      nameField: {
        required,
      },
    };
  },
  methods: {
    submitForm() {
      this.v$.$validate();

      // This is PROD (not DEV), and we will be validating fields
      // To jest PROD (nie DEV), więc będziemy sprawdzać poprawność pul, które wypełnił użytkownik
      if (VALIDATION_OFF) {
        this.checkPasswordChar();
        if (this.v$.$error) {
          return;
        }
      }

      postJson("/register", {
        name: this.nameField,
        email: this.emailField,
        password: this.passwordField,
      }).then((response) => {
        if (response.status == 200) {
          this.$router.push({ path: "/account" });
          return;
        } else if (response.status == 409) {
          this.emailServerErrors = ["Ten email już jest zarejestrowany"];
          return;
        } else if (response.status == 422) {
          this.passwordServerErrors = ["Hasło musi mieć conajmniej 8 znaków"];
          return;
        } else if (response.status == 400) {
          if (response.data == "email_bad") {
            this.emailServerErrors = ["Podano błędy adres email"];
            return;
          } else if (response.data == "name_len_bad") {
            this.nameServerErrors = ["Wpisz poprawne imię!"];
            return;
          } else if (response.data == "name_alpha_bad") {
            this.nameServerErrors = ["Imie musi zawierać tylko litery!"];
            return;
          }
        }
      });
    },
    checkPasswordChar() {
      if (!/[A-Z]/.test(this.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zawierać przynajmniej jedną dużą litere"
        );
        return;
      }

      if (!/[a-z]/.test(this.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zawierać przynajmniej jedną małą litere."
        );
        return;
      }

      if (!/[0-9]/.test(this.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zaweirać przynajmniej jedną cyfre"
        );
        return;
      }

      if (!/[#?!@$%^&*-]/.test(this.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zaweirać przynajmniej jeden znak specjalny (#?!@$%^&*-)."
        );
        return;
      }
      if (this.passwordField != this.confirmPasswordField) {
        this.confirmPasswordServerErrors.push("Hasła są rózne");
        return;
      }
    },
    
    newFieldInputs() {
      this.emailServerErrors = [];
      this.passwordServerErrors = [];
      this.nameServerErrors = [];
      this.confirmPasswordServerErrors = [];
    },

    navigateToLogin() {
      this.$router.push({ path: "/login" });
    },
  },
};
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="width: fit-content">
    <v-card class="pa-4">
      <v-card-text class="text-h3 mb-8 text-center"> Rejestracja </v-card-text>
      <v-form v-on:keydown.enter="submitForm">
        <v-text-field
          class="input-field-register"
          density="compact"
          v-model="nameField"
          label="First Name"
          :error-messages="
            v$.nameField.$errors.map((e) => e.$message).concat(nameServerErrors)
          "
          @input="
            () => {
              v$.nameField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.nameField.$touch"
        >
        </v-text-field>
        <v-text-field
          class="input-field-register"
          density="compact"
          v-model="emailField"
          label="Email"
          :error-messages="
            v$.emailField.$errors
              .map((e) => e.$message)
              .concat(emailServerErrors)
          "
          @input="
            () => {
              v$.emailField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.emailField.$touch"
        >
        </v-text-field>
        <v-text-field
          class="input-field-register"
          density="compact"
          v-model="passwordField"
          label="Hasło"
          type="password"
          :error-messages="
            v$.passwordField.$errors
              .map((e) => e.$message)
              .concat(passwordServerErrors)
          "
          @input="
            () => {
              v$.passwordField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.passwordField.$touch"
        >
        </v-text-field>
        <v-text-field
          class="input-field-register"
          density="compact"
          v-model="confirmPasswordField"
          label="Hasło"
          type="password"
          :error-messages="
            v$.confirmPasswordField.$errors
              .map((e) => e.$message)
              .concat(confirmPasswordServerErrors)
          "
          @input="
            () => {
              v$.confirmPasswordField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.confirmPasswordField.$touch"
        >
        </v-text-field>
        <v-row class="ma-1" justify="end" style="max-width: 100%">
          <v-btn @click="submitForm" color="blue">Zarejestruj</v-btn>
        </v-row>
      </v-form>
      <v-card-text class="text-caption pt-4 pb-0 text-center">
        Masz już konto? Kliknij
        <button
          class="registerButton"
          density="compact"
          @click="navigateToLogin"
        >
          tutaj
        </button>
        aby sie zalogować!
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style>
.input-field-register {
  width: 20em;
}
</style>
