import { io } from "socket.io-client";
import { reactive } from "vue";
import { defineStore } from 'pinia'
import { getBackendHostname, getJson } from "@/common/requests";


export const useSockerStore = defineStore('SocketStore', {
    state() {
        return {
          jwt: "",

        }
    },
    actions: {
      requestJWT() {
        
        
      }
    },
})

export const state = reactive({
  connected: false,
  fooEvents: [],
  barEvents: []
});

export const socket = io(getBackendHostname());


socket.on("connect", () => {
  state.connected = true;
  console.log('connect')
});

socket.on("disconnect", () => {
  state.connected = false;
  console.log('disconnect')
});

socket.on("chats-list", (...args) => {
  state.fooEvents.push(args);
  console.log('chats-list')
  console.log(args)
});

socket.on("bar", (...args) => {
  state.barEvents.push(args);
  console.log('bar')
});

