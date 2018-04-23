<template>
  <div id="app">
    <keep-alive>
      <router-view @userSignIn='userSignIn'></router-view>
    </keep-alive>
  </div>
</template>

<script>
import axios from 'axios'
axios.defaults.baseURL = BASE_URL
export default {
  data () {
    return {
      nickname: sessionStorage.nickname,
      username: sessionStorage.username,
      email: sessionStorage.email,
      image: sessionStorage.image,
      userID: sessionStorage.userID
    }
  },
  methods: {
    userSignIn (userinfo) {
      sessionStorage.nickname = userinfo.nickname
      sessionStorage.username = userinfo.username
      sessionStorage.email = userinfo.email
      sessionStorage.image = userinfo.image
      sessionStorage.userID = userinfo.userID
      this.nickname = sessionStorage.nickname
      this.username = sessionStorage.username
      this.email = sessionStorage.email
      this.image = sessionStorage.image
      this.userID = sessionStorage.userID
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
