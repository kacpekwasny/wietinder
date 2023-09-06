import { getJson } from '@/common/requests'
import { defineStore } from 'pinia'
import { Profile } from './ProfilesStore'


// How long the cache is valid expressed in miliseconds
const PROFILES_CACHE_TIMEOUT_MS = 1000 * 60 * 30 // Thirty minutes

// How many profiles can be stored inside
const PROFILES_MAX_CACHE_SIZE = 1000 // the profiles

// Store for keeping data of other profiles that has been returned from API.
// This store will implement an interface that will help with caching.
export const useProfilesStore = defineStore('Profiles', {
    state() {
        return {
            _chats: new Array<Chat>(),
        }
    },
    actions: {
        async loadChats() {
            const resp = await getJson('/who-likes-me')
            const chats: Chat[] = await resp.json()
            this._chats = new Array()
            this._chats.push(...chats)
            this._chats.sort((ch1, ch2) => (ch1.messages[0].datetime - ch2.messages[0].datetime))
        },
        toTopOfChatOrder(selector: number|string) {
            let idx = 0
            if (typeof selector === "string") {
                for (let [i, chat] of this._chats.entries()) {
                    if (chat.profile.public_id == selector) {
                        idx = i
                        break
                    }
                }
            } else {
                idx = selector
            }
            let newTopChat = this._chats.splice(idx, 1)[0]
            this._chats.unshift(newTopChat)
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