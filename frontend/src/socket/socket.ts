import { Socket, io } from "socket.io-client";
import { reactive } from "vue";
import { defineStore } from 'pinia'
import { getBackendHostname, getJson } from "@/common/requests";
import { throwStatement } from "@babel/types";
import { Message, useChatsStore } from "@/stores/ChatsStore";
import { useUserAccountStore } from "@/stores/AccountDataStore";


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
        if (this.connected) {
          return
        }

        this.socket = io(getBackendHostname());

        const chatsStore = useChatsStore()
        const userAccountStore = useUserAccountStore()

        this.socket.on("connect", () => {
          this.connected = true;
          (async () => {
            console.log('background job running!')
            while (this.connected) {
              await new Promise(r => setTimeout(r, 15_000));
              this.emit('background_keep_alive')
            }
            console.log('background job exiting!', this.connected)
          })()
        });
        
        this.socket.on("disconnect", () => {
          this.connected = false;
          console.log('disconnect')
        });
        
        this.socket.on("client_message", (...args) => {
          const msg: Message = args[0]
          let chat = undefined
          if (msg.author === userAccountStore.accountData.public_id) {
            chat = chatsStore.getChat(msg.recepient_id)
          } else {
            chat = chatsStore.getChat(msg.author)
          }
          console.log('recieved message', msg)
          chat.messages.unshift(msg)
        });

        this.socket.on("jwt_refresh", (...args) => {
          let jwt = args[0]
          if (jwt.jwt === undefined) {
            return
          }
          this.jwt = jwt.jwt
        });

        this.socket.on("join_room", (...args) => {
          console.log("received join_room")
          console.log(args)
        })
      },

      async emit(key: string, ...data: any[]) {
        if (key !== 'background_keep_alive') {
          console.log('emit', key)
          console.log(data)
        }
        if (!this.connected) {
          await this.openSocket()
        }
        this.socket.emit(key,
          {[AUTH_KEY_JWT_WS]: this.jwt},
          ...data)
      }

    },
})

