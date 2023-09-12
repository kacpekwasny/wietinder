import { Socket, io } from "socket.io-client";
import { reactive } from "vue";
import { defineStore } from 'pinia'
import { getBackendHostname, getJson } from "@/common/requests";


const AUTH_KEY_JWT_WS = '__flask_auth_jwt_ws'

export const useSocketStore = defineStore('SocketStore', {
    state() {
        return {
          jwt: "",
          messages: [],
          socket: null as Socket,
          connected: false,
        }
    },
    actions: {
      async refreshJWT() {
        const resp = await getJson('/refresh-jwt')
        if (resp.status != 200) {
          return
        }
        this.jwt = (await resp.json())["jwt"]
      },

      async openSocket() {
        await this.refreshJWT()
        this.socket = io(getBackendHostname());

        this.socket.on("connect", () => {
          this.connected = true;
          console.log('connect')
        });
        
        this.socket.on("disconnect", () => {
          this.connected = false;
          console.log('disconnect')
        });
        
        this.socket.on("chats-list", (...args) => {
          console.log('chats-list')
          console.log(args)
        });
        
      },

      emit(key: string, ...data: any[]) {
        console.log('emit', key)
        console.log(data)
        this.socket.emit(key,
          {[AUTH_KEY_JWT_WS]: this.jwt},
          ...data)
      }

    },
})

