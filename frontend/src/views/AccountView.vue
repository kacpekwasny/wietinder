<script lang="ts">
import draggable from "vuedraggable";
import { getBackendHostname, getJson, postJson } from "../common/requests";
import { assertExpressionStatement } from "@babel/types";
import axios from "axios";

export default {
  data() {
    return {
      accountData: {
        images: [],
        bio: "",
        sex: "",
        fields_of_study: "",
        target_sex: [],
        target_activity: [],
      },
      imageView: null,
      selectedImages: [],
      imagePreviews: [],
      overlay: false,
      rules: [
        (files: File[]) => {
          if (files.length > 9) {
            return "Można dodać maksymalnie 9 zdjęć.";
          }
          let MB = 1_024_000;
          for (let f of files) {
            if (f.size > 2 * MB) {
              return `Images should be smaller than 2MB. ${f.name} has size: ${(
                f.size / MB
              ).toFixed(2)} MB.`;
            }
          }
        },
      ],
    };
  },

  methods: {
    addImagesChanged(_: Event) {
      console.log(this.selectedImages);
      this.imagePreviews = this.selectedImages.map((imgFile) => {
        return { file: imgFile, url: URL.createObjectURL(imgFile) };
      });
    },

    async sendAccountData() {
      this.selectedImages = [];
      let resp = await postJson("/account-data", this.accountData);
      let json = resp.json();
      if (json.ok === undefined) {
        this.accountData = json;
      }
    },

    async updateAccountData() {
      this.accountData = await (await getJson("/account-data")).json();
    },

    async uploadImages() {
      const formData = new FormData();
      for (let i = 0; i < this.selectedImages.length; i++) {
        formData.append("images", this.selectedImages[i]);
      }
      const resp = await axios
        .post(`${getBackendHostname()}/upload-images`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          withCredentials: true,
        })
      console.log(resp);
      this.selectedImages = [];
      this.updateAccountData()
    },

    async removeImageFromRemote(index: int) {
      const removedImageName = this.accountData.images[index];
      this.accountData.images.splice(index, 1);

      const resp = await postJson("/delete-image", {
        removed_image_name: removedImageName,
      });
      const data = await resp.json();
      console.log(data)
      if (!data.ok) {
        return alert("Nie powiodło się, Error :( ");
      }
    },

    removeImageFromUploadList(index: int) {
      this.selectedImages.splice(index, 1);
    },

    remoteURL(imageName: string) {
      return `${getBackendHostname()}/uploads/${imageName}`;
    },

    localURL(file: File) {
      return URL.createObjectURL(file);
    },
  },

  components: {
    draggable,
  },

  computed: {},

  async created() {
    await this.updateAccountData();
  },
};
</script>

<!-- zrobic zeby zdjecia sie wyswietlaly, check box kogo szukam, piwo/etc, nie widac boxów :(()) -->

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-textarea label="Opis profilu" v-model="accountData.bio"></v-textarea>
    <v-card class="pa-2 mt-2 mb-2">
      <div class="text-h5 ma-2">Dodaj zdjęcia</div>
      <v-file-input
        chips
        multiple
        :rules="rules"
        prepend-icon="mdi-camera"
        accept="image/*"
        label="Wybierz zdjęcia"
        v-model="selectedImages"
        @change="addImagesChanged"
      ></v-file-input>
      <v-row>
        <v-col
          v-for="(file, index) in selectedImages"
          cols="6"
          sm="4"
          class="pa-2"
        >
          <v-card density="compact">
            <v-img :src="localURL(file)" max-height="150px">
              <v-btn
                class="ma-1 float-right"
                icon
                @click="removeImageFromUploadList(index)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-img>
            <div class="text-caption ma-1">
              {{ file.name }}
            </div>
          </v-card>
        </v-col>
      </v-row>
      <v-btn
        class="float-right mt-2"
        @click="uploadImages()"
        :disabled="selectedImages.length == 0"
        >Wyślij {{selectedImages.length == 1 ? "zdjęcie" : "zdjęcia"}}</v-btn
      >
    </v-card>
    <v-card class="pa-2 mt-2 mb-2">
      <div class="text-h5">Moje zdjęcia</div>

      <!--
      TODO:
      tutaj było `selectedImages` zamiast `images`
      teraz możemy przeciągać i zmieniać kolejność zdjęć, które już są zuploadowane na serwer,
      
      Czyli używamy tego v-file-input do wybrania zdjec tak jak do tej pory, ale upload zdjec odbywa sie osobno od zapisywania ustawien profilu - trzeba dodać przycisk obok tego v-file-input.
      Po udanym upload należy wyczyścić selectedImages, żeby było wrażenie, że się powiodło i że znikneły pliki z pola v-file-input.
      Jednocześnie powinny się pokazać w draggable.
      Jak już zuploadujemy zdjęcia, to powinny się pokazać w tym draggable (powinny być od teraz w `images` a draggable je wyrenderuje.)
      Ten dotychczasowy przycisk na dole będzie służyć do zapisywania ustawien profilu i kolejności wyświetlania zdjęć. nie będzie uploadował zdjęć.
      Draggable powinno umożliwić usunięcie zdjęć jakichś z tych co już są - czyli jakiś znaczek x na zdjęciu każdym w prawym górnym rogu który by wywoływał funkcję,
      która robi requesta GET /delete-img/<filename> a na backendzie sprawdzamy, czy to jest plik tego usera, co chce usunąć.

    -->
      <draggable
        v-if="accountData.images.length > 0"
        v-model="accountData.images"
        item-key="url"
        group="people"
        style="align-items: center; display: flex; flex-wrap: wrap"
      >
        <!-- Had to mannulay add these style elements copied from https://github.com/vuetifyjs/vuetify/blob/master/packages/vuetify/src/components/VGrid/VGrid.sass
    for the column layout to start working, because when v-row was the parent of draggable,
    draggable became a column of width 2/12 I think, and as such its children became even thinnger :/ -->
        <template #item="{ element: preview, index }">
          <v-col cols="6" sm="4" class="pa-2">
            <v-card density="compact">
              <v-img :src="remoteURL(preview)" max-height="150px">
                <v-btn
                  class="ma-1 float-right"
                  icon
                  @click="removeImageFromRemote(index)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-img>
              <div class="text-caption ma-1">
                {{ preview.name }}
              </div>
            </v-card>
          </v-col>
        </template>
      </draggable>
      <div v-else class="ma-1 text-subtitle-1">
        Nie masz jeszcze obrazów do wyświetlania. Dodaj używając opcji powyżej.
      </div>
      <br />
      <v-row dense>
        <v-col col="6">
          <v-card class="align-end" height="100%">
            <v-card-title class="text-left"> Moja płeć: </v-card-title>
            <v-card-action>
              <v-radio-group v-model="accountData.sex" column>
                <v-radio
                  label="Kobieta"
                  color="blue"
                  value="female"
                  density="default"
                ></v-radio>
                <v-radio
                  label="Mężczyzna"
                  color="blue"
                  value="male"
                  density="default"
                ></v-radio>
              </v-radio-group>
            </v-card-action>
          </v-card>
        </v-col>
        <v-col col="6">
          <v-card class="align-end" height="100%">
            <v-card-title class="text-left"> Pożądana płeć pary: </v-card-title>
            <v-card-action>
              <v-checkbox
                v-model="accountData.target_sex"
                label="Kobieta"
                value="female"
                hideDetails
                density="compact"
                class="ml-2"
              ></v-checkbox>
              <v-checkbox
                v-model="accountData.target_sex"
                label="Mężczyzna"
                value="male"
                hideDetails
                density="compact"
                class="ml-2"
              ></v-checkbox>
            </v-card-action>
          </v-card>
        </v-col>
        <v-col col="6">
          <v-card class="align-end" height="100%">
            <v-card-title class="text-left"> Czynność: </v-card-title>
            <v-card-action>
              <v-checkbox
                v-model="accountData.target_activity"
                label="Na piwo"
                value="beer"
                hideDetails
                density="compact"
                class="ml-2"
              ></v-checkbox>
              <v-checkbox
                v-model="accountData.target_activity"
                label="Na życie"
                value="life"
                hideDetails
                density="compact"
                class="ml-2"
              ></v-checkbox>
              <v-checkbox
                v-model="accountData.target_activity"
                label="Do projektu"
                value="project"
                hideDetails
                density="compact"
                class="ml-2"
              ></v-checkbox>
            </v-card-action>
          </v-card>
        </v-col>
      </v-row>
      <v-btn class="mt-2 float-right" @click="sendAccountData()"
        >Zapisz zmiany!</v-btn
      >
    </v-card>
  </v-container>
</template>
