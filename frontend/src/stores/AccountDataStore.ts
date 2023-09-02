import { getJson } from '@/common/requests'
import { defineStore } from 'pinia'

// You can name the return value of `defineStore()` anything you want,
// but it's best to use the name of the store and surround it with `use`
// and `Store` (e.g. `useUserStore`, `useCartStore`, `useProductStore`)
// the first argument is a unique id of the store across your application
export const useUserAccountStore = defineStore('UserAccount', {
    state() {
        return {
            
            // `_lastChecked` - keeps the date of when was the last `GET /account-data` sent.
            // It is a number representing the Unix timestamp, so ms since the date 01.01.1970
            // 0 - zero means we have never before checked for the state.
            // Date.now() will be set when we send a request.
            // check `refreshAccountData` method to understand purpose of this param.
            _lastChecked: 0 as number,
            
            loggedIn: false as boolean,
            accountData: {
                name: "" as string,
                public_id: "" as string,
                images: [] as string[],
                bio: "" as string,
                sex: "" as string,
                fields_of_study: [] as string[],
                target_sex: [] as string[],
                target_activity: [] as string[],
            },
            matches: {
        
            },
        }
    },
    actions: {
        refreshUserData(force: boolean=false) {

            if (!force && (Date.now() - this._lastChecked < 1000 * 30)) {
                // If we dont force
                // and to early for a new request
                // return.
                return
            }

            // We are either forcing or previous request was long time ago
            // so the data may have changed.
            getJson('/account-data').then(r => {
                this._lastChecked = Date.now()
                if (r.status != 200) {
                    this.loggedIn = false
                    this.resetAccoutnData()
                }
                this.loggedIn = true
                return r.json()
            }).then(j => {
                this.accountData = j;
            })
        },
        resetAccoutnData() {
            this.accountData = {
                name: "",
                public_id: "",
                images: [],
                bio: "",
                sex: "",
                fields_of_study: [],
                target_sex: [],
                target_activity: [],
            }
        }
    }
},
)