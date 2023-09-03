<script lang="ts">
import { defineComponent } from "vue";
import { useVuelidate } from "@vuelidate/core";
import { email, required } from "@vuelidate/validators";

import { postJson } from "../common/requests";
import { useUserAccountStore } from "@/stores/AccountDataStore";

export default defineComponent({
  setup() {
    return {
      v$: useVuelidate(),
    };
  },
  data() {
    return {
      showModal: false,
      emailField: "",
      passwordField: "",
      emailServerErrors: [],
      passwordServerErrors: [],
    };
  },
  validations() {
    return {
      emailField: { email, required },
      passwordField: { required },
    };
  },
  methods: {
    navigateToRegister() {
      this.$router.push({ path: "/register" });
    },
    async submitForm() {
      this.v$.$validate();
      if (this.v$.$error) {
        return;
      }
      const resp = await postJson("/login", {
        email: this.emailField,
        password: this.passwordField,
      });

      if (resp.status == 200) {
        useUserAccountStore().refreshUserData(true)
        this.$router.push({ path: "/account" });
      }
      if (resp.status == 401) {
        this.passwordServerErrors = ["Błędne hasło!"];
        return;
      } else if (resp.status == 404) {
        this.emailServerErrors = ["Email nie istnieje!"];
        return;
      }
    },

    newFieldInputs() {
      this.emailServerErrors = [];
      this.passwordServerErrors = [];
    },
  },
});
</script>

<template>
  <v-container fluid class="d-flex flex-column" style="width: fit-content">
    <v-card class="pa-4">
      <v-card-text class="text-h3 mb-8 text-center"> Logowanie </v-card-text>
      <v-form v-on:keydown.enter="submitForm">
        <v-text-field
          class="input-field"
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
          class="input-field"
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
        <v-row class="ma-1" justify="end" style="max-width: 100%">
          <v-btn @click="submitForm" color="blue" :disabled="v$.$invalid">Zaloguj</v-btn>
        </v-row>
      </v-form>
      <v-card-text class="text-caption pt-4 pb-0 text-center">
        Nie masz konta? Kliknij
        <button
          class="registerButton"
          density="compact"
          @click="navigateToRegister"
        >
          tutaj!
        </button>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style>
.input-field {
  width: 15em;
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
