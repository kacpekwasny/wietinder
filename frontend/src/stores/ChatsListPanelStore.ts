import { defineStore } from 'pinia'

export const useChatsListPanelStore = defineStore('ChatsListPanel', {
    state() {
        return {
            showChatsListPanel: true as boolean,
        }
    },
    actions: {
        toggleChatsListPanel(){
            this.showChatsListPanel = !this.showChatsListPanel;
        },
        openChatsListPanel(open=true) {
            this.showChatsListPanel = open
        }
    }
},
)