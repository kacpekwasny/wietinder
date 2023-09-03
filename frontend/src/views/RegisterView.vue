<script lang="ts">
import useValidate from "@vuelidate/core";
import { email, required, minLength, helpers } from "@vuelidate/validators";
import { postJson } from "../common/requests";

const IS_PROD =
  String(import.meta.env.VITE_IS_PRODUCTION).toLowerCase() === "true";

console.info(`IS_PROD = ${IS_PROD}`)

// novalidate.value = passwordValidationOff; //ogolnie to novalidate jest wpisane w html przy registerForm.passwordField i powinno usuwac te ograniczenia

export default {
  data() {
    return {
      showModal: false,
      v$: useValidate(),
      registerForm: {
        nameField: "",
        emailField: "",
        passwordField: "",
        confirmPasswordField: "",
        sexField: "",

      },
      nameServerErrors: [],
      emailServerErrors: [],
      passwordServerErrors: [],
      confirmPasswordServerErrors: [],

    };
  },
  validations() {
    return {
      registerForm: {
        nameField: {
          required,
        },
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
          sameAsPassword: helpers.withMessage("Passwords need to match", (v: string) => v === this.registerForm.passwordField)
        },

      }
    };
  },
  methods: {
    submitForm() {
      this.v$.$validate();

      if (IS_PROD) {
        this.checkPasswordChar();
        if (this.v$.$error) {
          return;
        }
      }

      postJson("/register", {
        name: this.registerForm.nameField,
        email: this.registerForm.emailField,
        password: this.registerForm.passwordField,
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
      if (!/[A-Z]/.test(this.registerForm.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zawierać przynajmniej jedną dużą litere"
        );
        return;
      }

      if (!/[a-z]/.test(this.registerForm.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zawierać przynajmniej jedną małą litere."
        );
        return;
      }

      if (!/[0-9]/.test(this.registerForm.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zaweirać przynajmniej jedną cyfre"
        );
        return;
      }

      if (!/[#?!@$%^&*-]/.test(this.registerForm.passwordField)) {
        this.passwordServerErrors.push(
          "Hasło musi zaweirać przynajmniej jeden znak specjalny (#?!@$%^&*-)."
        );
        return;
      }
      if (this.registerForm.passwordField != this.registerForm.confirmPasswordField) {
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
          v-model="registerForm.nameField"
          label="First Name"
          :error-messages="
            v$.registerForm.nameField.$errors.map((e) => e.$message).concat(nameServerErrors)
          "
          @input="
            () => {
              v$.registerForm.nameField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.registerForm.nameField.$touch"
        >
        </v-text-field>
        <v-text-field
          class="input-field-register"
          density="compact"
          v-model="registerForm.emailField"
          label="Email"
          :error-messages="
            v$.registerForm.emailField.$errors
              .map((e) => e.$message)
              .concat(emailServerErrors)
          "
          @input="
            () => {
              v$.registerForm.emailField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.registerForm.emailField.$touch"
        >
        </v-text-field>
        <v-text-field
          class="input-field-register"
          density="compact"
          v-model="registerForm.passwordField"
          label="Hasło"
          type="password"
          :error-messages="
            v$.registerForm.passwordField.$errors
              .map((e) => e.$message)
              .concat(passwordServerErrors)
          "
          @input="
            () => {
              v$.registerForm.passwordField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.registerForm.passwordField.$touch"
        >
        </v-text-field>
        <v-text-field
          class="input-field-register"
          density="compact"
          v-model="registerForm.confirmPasswordField"
          label="Powtórz hasło"
          type="password"
          :error-messages="
            v$.registerForm.confirmPasswordField.$errors
              .map((e) => e.$message)
              .concat(confirmPasswordServerErrors)
          "
          @input="
            () => {
              v$.registerForm.confirmPasswordField.$touch();
              newFieldInputs();
            }
          "
          @blur="v$.registerForm.confirmPasswordField.$touch"
        >
        </v-text-field>
        <v-row class="ma-1" justify="end" style="max-width: 100%">
          <v-btn @click="submitForm" color="blue" :disabled="v$.$invalid">Zarejestruj</v-btn>
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
