<script lang="ts">
import draggable from "vuedraggable";
import { getBackendHostname, getJson, postJson } from "../common/requests";
import { assertExpressionStatement } from "@babel/types";
import axios from "axios";

export default {
  data() {
    return {
      selectedImages: [],
      images: [],
      imageView: null,
      bio: "",
      mySex: "",
      collegeMajor: "",
      targetSex: [],
      targetActivity: [],
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
      this.imagePreviews = this.selectedImages.map((img) => {
        return { img: img, url: URL.createObjectURL(img) };
      });
    },

    submitForm() {
      this.selectedImages = []
      postJson("/account-data", this.buildAccountDataObject())
        .then((response) => response.json())
        .then((data) => {
          if (data.ok === undefined) {
            return this.setAccountData(data);
          }
          alert("Not saved, Error :( ");
        });

    },

    uploadImages(){
      const formData = new FormData();
      for (let i = 0; i < this.selectedImages.length; i++) {
        formData.append('images', this.selectedImages[i]);
      }
      axios.post(`${getBackendHostname()}/upload-images`, formData, {
        headers: {
                'Content-Type': 'multipart/form-data'
                    
        },
        withCredentials:true

      }).then(response =>{
          console.log(response);
          this.selectedImages = [];

        getJson("/get-images")
        .then((response) => response.json())
        .then((data) => {
          if (data.ok === undefined) {
            console.log(data.images)
            return this.images = data.images;;
          }
          alert("Not saved, Error :( ");
        });
        })
    },

    removeImage(index){
      console.log(this.images)
      const removedImageName = this.images[index];
      console.log(removedImageName)
      this.images.splice(index, 1);
      const data = {
        removed_image_name: removedImageName
      };
      postJson("/delete-image", data)
      .then((response) => response.json())
        .then((data) => {
          if (!data.ok) {
            return alert("Not saved, Error :( ");
          }
        });
    },

    getImageURL(imageName: string) {
      return `${getBackendHostname()}/uploads/${imageName}`;
    },

    makeURL(file: File) {
      return this.getImageURL(file)
      return URL.createObjectURL(file);
    },

    setAccountData(accountJson: Object) {
    console.log(accountJson)
      this.bio = accountJson.bio;
      this.collegeMajor = accountJson.college_major;
      this.mySex = accountJson.my_sex;
      this.targetSex = accountJson.target_sex;
      this.targetActivity = accountJson.target_activity;
      this.images = accountJson.images;
    },
    
    buildAccountDataObject(): Object {
      return {
        bio: this.bio,
        college_major: this.collegeMajor,
        my_sex: this.mySex,
        target_sex: this.targetSex,
        target_activity: this.targetActivity,
        images: this.images
      }
    },

    fetchData: function() {
      axios.get("/account-data")
      .then(function(response){
        console.log(response)
      }
      )
    }

    
  },

  async created() {
    let accountData = await getJson("/account-data");
    this.setAccountData(await accountData.json());
  },

  components: {
    draggable,
  },
};
</script>

<!-- zrobic zeby zdjecia sie wyswietlaly, check box kogo szukam, piwo/etc, nie widac boxów :(()) -->

<template>
  <v-container fluid class="d-flex flex-column" style="max-width: 800px">
    <v-textarea label="Opis profilu" v-model="bio"></v-textarea>
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
    <v-btn class="mt-2 mb-2" @click="uploadImages">Dodaj zdjęcia</v-btn>
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
      v-model="images" 
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
            <v-img :src="makeURL(preview)" max-height="150px">
              <v-btn icon @click="removeImage(index)">
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
    <v-row dense>
      <v-col col="6">
        <v-card class="align-end" height="100%">
          <v-card-title class="text-left"> Moja płeć: </v-card-title>
          <v-card-action>
            <v-radio-group v-model="mySex" column>
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
              v-model="targetSex"
              label="Kobieta"
              value="female"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
            <v-checkbox
              v-model="targetSex"
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
              v-model="targetActivity"
              label="Na piwo"
              value="beer"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
            <v-checkbox
              v-model="targetActivity"
              label="Na życie"
              value="life"
              hideDetails
              density="compact"
              class="ml-2"
            ></v-checkbox>
            <v-checkbox
              v-model="targetActivity"
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
    <v-btn class="mt-2 mb-2" @click="submitForm">Zapisz zmiany!</v-btn>
  </v-container>
</template>
