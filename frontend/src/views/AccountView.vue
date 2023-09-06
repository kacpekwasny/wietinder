<script lang="ts">
import draggable from "vuedraggable";
import { getBackendHostname, getJson, postJson } from "../common/requests";
import axios from "axios";
import router from "../router"; //dałem do testu, do wywalenia jakbym zapomniał

import { useUserAccountStore } from "../stores/AccountDataStore";
import { mapState } from "pinia";

export default {
  data() {
    const userAccountStore = useUserAccountStore()
    return {
      userAccountStore,
      imageView: null,
      selectedImages: [] as File[],
      imagePreviews: [] as { file: File; url: string }[],
      overlay: false,
      rules: [
        (files: File[]) => {
          if (files.length + userAccountStore.accountData.images.length > 9) {
            return "Można mieć maksymalnie 9 zdjęć w sumie.";
          }
          let MB = 1_024_000;
          for (let f of files) {
            if (f.size > 2 * MB) {
              return `Images should be smaller than 2MB. ${f.name} has size: ${(
                f.size / MB
              ).toFixed(2)} MB.`;
            }
          }
          return;
        },
      ] as ValidationRule[],
      allPossibleFieldsOfStudyAGH: [] as string[],
      css: {
        dispImgMaxHeight: "150px",
      },
    };
  },

  methods: {
    addImagesChanged(_: Event) {
      this.imagePreviews = this.selectedImages.map((imgFile) => {
        return { file: imgFile, url: URL.createObjectURL(imgFile) };
      });
    },

    async sendAccountData() {
      let resp = await postJson("/account-data", this.accountData);
      let json = await resp.json();
      if (json.ok === undefined) {
        this.accountData = json
      }
    },

    async uploadImages() {
      const formData = new FormData();
      for (let i = 0; i < this.selectedImages.length; i++) {
        formData.append("images", this.selectedImages[i]);
      }
      const resp = await axios.post(
        `${getBackendHostname()}/upload-images`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          withCredentials: true,
        }
      );
      if (resp.status != 200) {
        console.log('uploadImages returned status: ', resp.status)
        return
      }
      this.selectedImages = [];
      this.userAccountStore.refreshUserData(true);
    },

    async removeImageFromRemote(index: number) {
      const removedImageName = this.accountData.images[index];
      this.accountData.images.splice(index, 1);

      const resp = await postJson("/delete-image", {
        removed_image_name: removedImageName,
      });
      const data = await resp.json();
      if (!data.ok) {
        return alert("Nie powiodło się, Error :( ");
      }
    },

    removeImageFromUploadList(index: number) {
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

  computed: {
    accountData: {
      get() {
        return this.userAccountStore.accountData
      },
      set(v) {
        this.userAccountStore.$patch({accountData: v})
      }
    },
    imagesToUploadValid() {
      if (this.selectedImages.length == 0
      ||  this.selectedImages.length + this.userAccountStore.accountData.images.length > 9) {
        return false
      }
      return true
    }
  },

  async created() {
    this.userAccountStore.refreshUserData();

    getJson("/static/agh-fields-of-study").then(async resp => {
      this.allPossibleFieldsOfStudyAGH = await resp.json();
    })
  },
};
</script>

<!-- zrobic zeby zdjecia sie wyswietlaly, check box kogo szukam, piwo/etc, nie widac boxów :(()) -->

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-textarea
      hide-details
      class="elevation-3 rounded"
      label="Opis profilu"
      v-model="accountData.bio"
    ></v-textarea>
    <v-card class="pa-3 mt-2 mb-2 elevation-3">
      <div>
        <div class="text-h5 mb-2">Dodaj zdjęcia</div>
        <v-file-input
          class="ml-2"
          chips
          multiple
          :rules="rules"
          prepend-icon="mdi-camera"
          accept="image/*"
          label="Wybierz zdjęcia"
          v-model="selectedImages"
          @change="addImagesChanged"
        ></v-file-input>
        <v-row class="pa-2">
          <v-col
            v-for="(file, index) in selectedImages"
            cols="6"
            sm="4"
            class="pa-2"
          >
            <v-card>
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
          color="yellow"
          @click="uploadImages()"
          :disabled="!imagesToUploadValid"
          >Wyślij
          {{ selectedImages.length == 1 ? "zdjęcie" : "zdjęcia" }}</v-btn
        >
      </div>
      <br />
      <br />
      <div class="">
        <v-divider class="mt-4 mb-4"></v-divider>
        <div class="text-h5">Moje zdjęcia</div>
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
              <v-card density="compact" :height="css.dispImgMaxHeight">
                <v-img
                  :src="remoteURL(preview)"
                  :max-height="css.dispImgMaxHeight"
                >
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
          Nie masz jeszcze obrazów do wyświetlania. Dodaj używając opcji
          powyżej.
        </div>
      </div>
      <v-divider class="mb-4 mt-4"></v-divider>
      <v-row dense>
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
        <v-col col="6">
          <v-card class="align-end" height="100%"  style="min-width: 14em;">
            <v-card-title class=""> Kierunek: </v-card-title>
            <v-card-action>
              <v-select
                class="ma-1"
                v-model="accountData.fields_of_study"
                :items="allPossibleFieldsOfStudyAGH"
                chips
                label="Kierunki studiów:"
                multiple
              ></v-select>
            </v-card-action>
          </v-card>
        </v-col>
      </v-row>
      <v-btn color="yellow" class="mt-5 float-right" @click="sendAccountData()"
        >Zapisz zmiany!</v-btn
      >
    </v-card>
  </v-container>
</template>
