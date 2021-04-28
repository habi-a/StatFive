import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: [],
    connected: false,
    admin: false,
    barColor: 'rgba(0, 0, 0, .8), rgba(0, 0, 0, .8)',
    barImage: 'https://demos.creative-tim.com/material-dashboard/assets/img/sidebar-1.jpg',
    drawer: null,
  },
  mutations: {
    SET_BAR_IMAGE (state, payload) {
      state.barImage = payload
    },
    SET_DRAWER (state, payload) {
      state.drawer = payload
    },
    SET_STATUS (state, payload) {
      state.connected = payload
    },
    SET_ADMIN (state, payload) {
      state.admin = payload
    },
    SET_USER (state, payload) {
      state.user = payload
    },
  },
  actions: {

  },
  plugins: [createPersistedState()],
})
