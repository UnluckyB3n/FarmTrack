import { defineStore } from 'pinia'

export const useMainStore = defineStore('main', {
  state: () => ({
    // Add your state properties here
    user: null,
    isAuthenticated: false,
    // ...other state
  }),
  actions: {
    setUser(user) {
      this.user = user
      this.isAuthenticated = !!user
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
    },
    // ...other actions
  },
  getters: {
    // Example getter
    username: (state) => state.user?.name || '',
  },
})
