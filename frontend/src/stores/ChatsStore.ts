import { getJson } from '@/common/requests'
import { defineStore } from 'pinia'
import { Profile } from './ProfilesStore'


// Store for keeping data of other profiles that has been returned from API.
// This store will implement an interface that will help with caching.
export const useChatsStore = defineStore('ChatsStore', {
    state() {
        return {
            _chats: new Map<string, Chat>(),
        }
    },
    actions: {
        async loadChats() {
            const resp = await getJson('/chats') // To chyba nie powinno dawać ID użytkowników tylko liste Chatów
            const chats: Chat[] = await resp.json()
            chats.sort((ch1, ch2) => (ch1.messages[0].datetime + ch2.messages[0].datetime))
            chats.forEach(ch => {
                this._chats.set(ch.profile.public_id, ch)
            })
        },

        toTopOfChatOrder(publicId: string) {
            let chat = this._chats.get(publicId)
            if (!this._chats.delete(publicId)) {
                return
            }
            this._chats.set(publicId, chat)
        },

        toList(): Chat[] {
            const chats = new Array<Chat>()
            this._chats.forEach(ch => {
                chats.push(ch)
            })
            return chats.reverse()
        }

    },
})



export interface Chat {
    profile:    Profile
    messages:   Message[]
}

export interface Message {
    id:         number
    
    // 
    datetime:   number

    author:     string
    message:    string
}