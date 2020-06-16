<template>
  <div id="app">
    <b-navbar toggleable="sm" type="dark" variant="dark">
        <b-navbar-brand href="/" variant="light">EventService</b-navbar-brand>
        <b-navbar-nav class="ml-auto">
            <template v-if="user.id">
              <b-nav-item>{{user.username}}</b-nav-item>
              <b-nav-item button @click="logout"><b-icon icon="door-closed"></b-icon></b-nav-item>
            </template>
            <template v-else>
              <b-nav-item @click="openModal('log')">Войти</b-nav-item>
              <b-nav-item @click="openModal('reg')">Регистрация</b-nav-item>
            </template>
        </b-navbar-nav>
    </b-navbar>
    <table-events ref="tableevents"></table-events>
    <login-modal ref="loginmodal"></login-modal>
    <create-modal ref="createmodal"></create-modal>
  </div>
</template>

<script>
/* eslint-disable */
import {HTTP} from './assets/js/common'
import TableEvents from './components/TableEvents'
import LoginModal from './components/LoginModal'
import CreateModal from './components/CreateModal'
export default {
  name: 'App',
  components: {
    'table-events': TableEvents,
    'login-modal': LoginModal,
    'create-modal': CreateModal
  },
  computed: {
    user: {
      get: function(){
        return {id: localStorage.getItem('user_id'), username: localStorage.getItem('user_username')} || {}
      },
      set: function(data){
        localStorage.setItem('user_id', data.id)
        localStorage.setItem('user_username', data.username)
      }
    },
    token: {
      get: function(){
        return localStorage.getItem('token') || ""
      },
      set: function(token){
        localStorage.setItem('token', token)
      }
    }
  },
  methods: {
    logout: function(){
      localStorage.removeItem('token')
      localStorage.removeItem('user_id')
      localStorage.removeItem('user_username')
      document.location.reload(true);
    },
    openModal: function (type) {
      this.$refs.loginmodal.openModal(type)
    },
    saveUser: function(user){
      this.user = user
      this.token = user.token
    }
  }
}
</script>
