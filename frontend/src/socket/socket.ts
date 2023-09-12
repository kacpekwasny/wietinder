import { Socket, io } from "socket.io-client";
import { reactive } from "vue";
import { defineStore } from 'pinia'
import { getBackendHostname, getJson } from "@/common/requests";
import { throwStatement } from "@babel/types";
import { Message, useChatsStore } from "@/stores/ChatsStore";
import { useUserAccountStore } from "@/stores/AccountDataStore";
import { timer } from "@/common/timer";


const AUTH_KEY_JWT_WS = '__flask_auth_jwt_ws'

export const useSocketStore = defineStore('SocketStore', {
    state() {
        return {
          jwt: "",
          messages: [],
          socket: null as Socket,
          tryConnected: false,
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

      openConnectionToMyRoom() {
        this.socket = io(getBackendHostname())
        this.enter_my_room()
      },

      enter_my_room() {
        this._emit_with_jwt('enter_my_room')
      },

      async keepConnectionToMyRoom() {
        this.tryConnected = true
        
        if (this.socket.connected) {
          return this.enter_my_room()
        }

        this.socket.on("connect", () => {
          (async () => {
            console.log('background job running!')
            while (this.tryConnected) {
              while (this.socket?.connected) {
                await timer(15000);
                this.enter_my_room()
              }
              this.openConnectionToMyRoom()
            }
            this.socket.close()
            console.log('background job exiting!', this.socket.connected)
          })()
        });
        
        this.socket.on("disconnect", async () => {
          await this.refreshJWT()
          console.log('disconnect')
        });

        const chatsStore = useChatsStore()
        const userAccountStore = useUserAccountStore()

        this.socket.on("client_message", (...args) => {
          const msg: Message = args[0]
          let chat = undefined
          if (msg.author === userAccountStore.accountData.public_id) {
            chat = chatsStore.getChat(msg.recepient_id)
          } else {
            chat = chatsStore.getChat(msg.author)
          }

          chat.messages.unshift(msg)
        });

        this.socket.on("jwt_refresh", (...args) => {
          let jwt = args[0]
          if ((typeof jwt.jwt) === "string") {
            this.jwt = jwt.jwt
          }
        });

        this.socket.on("enter_my_room", (...args) => {
          console.log("Entered my room.")
          console.log(args)
        })
      },

      async emit(key: string, ...data: any[]) {
        if (key !== 'background_keep_alive') {
          console.log('emit', key)
          console.log(data)
        }
        this._emit_with_jwt(key, ...data)
      },

      _emit_with_jwt(key: string, ...data: any[]) {
        this.socket.emit(key,
          {[AUTH_KEY_JWT_WS]: this.jwt},
          ...data)
      }

    },
})

