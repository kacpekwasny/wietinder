import { defineStore } from 'pinia'

export const usePanelStore = defineStore('SidePanel', {
    state() {
        return {
            showSidePanel: true as boolean,
        }
    },
    actions: {
        toggleSidePanel(){
            this.showSidePanel = !this.showSidePanel;
        }
    }
},
)