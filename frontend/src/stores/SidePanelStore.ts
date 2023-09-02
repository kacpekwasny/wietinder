import { defineStore } from 'pinia'

export const usePanelStore = defineStore('SidePanel', {
    state() {
        return {
            showSidePanel: true as boolean,
        }
    },
    actions: {
        toggleSidePanel(){
            console.log(this.showSidePanel)
            this.showSidePanel = !this.showSidePanel;
        }
    }
},
)