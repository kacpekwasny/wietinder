import { getJson } from '@/common/requests'
import { defineStore } from 'pinia'


// How long the cache is valid expressed in miliseconds
const PROFILES_CACHE_TIMEOUT_MS = 1000 * 60 * 30 // Thirty minutes

// How many profiles can be stored inside
const PROFILES_MAX_CACHE_SIZE = 1000 // the profiles

// Store for keeping data of other profiles that has been returned from API.
// This store will implement an interface that will help with caching.
export const useProfilesStore = defineStore('Profiles', {
    state() {
        return {
            _profiles: new Map<string, Profile>(),
        }
    },
    actions: {
        async profile(publicId: string, fetch: boolean = false): Promise<Profile | undefined> {
            let p = this._profiles.get(publicId)

            if (fetch || p === undefined || Date.now() - p._last_fetched > PROFILES_CACHE_TIMEOUT_MS) {
                p = await this.fetchProfile(publicId)
                if (p === undefined) {
                    return undefined
                }
                this._profiles.set(publicId, p)
            }
            this.cacheSizeManagment()

            p._last_checked = Date.now()
            return p
        },

        async fetchProfile(publicId: string): Promise<Profile | undefined> {
            const resp = await getJson(`/profile/${publicId}`)
            if (resp.status != 200) {
                return undefined
            }
            const json: Profile = await resp.json()
            json._last_fetched = Date.now()
            return json
        },

        async cacheSizeManagment() {
            if (this._profiles.size < PROFILES_MAX_CACHE_SIZE) {
                return
            }

            // The cache is too big, delete the profiles that have
            // `_last_checked` the oldest.
            const profilesArr = Array.from(this._profiles.values())

            // sort from oldest to newest `_last_checked`
            profilesArr.sort((a, b) => a._last_checked - b._last_checked)

            for (let p of profilesArr.slice(0, -PROFILES_MAX_CACHE_SIZE)) {
                this._profiles.delete(p.public_id)
            }
        },

        addProfilesToCache(profiles: Profile[]) {
            for (let p of profiles) {
                if (!this._profiles.has(p.public_id)) {
                    this._profiles.set(p.public_id, p)
                }
            }
        }
    },
})


export interface Profile {
    // Timestamp of the last time the profile was fetched from server
    _last_fetched: number

    // Timestamp of the last readout.
    _last_checked: number

    public_id: string
    name: string
    bio: string
    sex: string

    images: string[]
    target_sex: string[]
    fields_of_study: string[]
    target_activity: string[]

}