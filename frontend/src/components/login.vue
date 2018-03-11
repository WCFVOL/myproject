<template>
  <div>
      <div class="login-wrap" v-show="showLogin">
            <h3>登录</h3>
              <p v-show="showTishi">{{tishi}}</p>
              <input type="text" placeholder="请输入用户名" v-model="username">
              <input type="password" placeholder="请输入密码" v-model="password" @keyup.enter='login'>
              <button v-on:click="login">登录</button>
              <span v-on:click="ToRegister">没有账号？马上注册</span>
              <span v-on:click="findPwd">找回密码</span>
      </div>
      <div class="login-wrap" v-show="showRegister">
          <h3>注册</h3>
          <p v-show="showTishi">{{tishi}}</p>
          <input type="text" placeholder="请输入用户名" v-model="newUsername">
          <input type="password" placeholder="请输入密码" v-model="newPassword">
          <input type="password" placeholder="请再次输入密码" v-model="newPassword2">
          <input type="file" name="avatar"
            v-on:change="changeImage($event)"
            accept="image/gif,image/jpeg,image/jpg,image/png"
            ref="avatarInput"
          >
          <input type="email" placeholder="请输入邮箱" v-model="email" @keyup.enter='register'>
          <button v-on:click="register">注册</button>
          <span v-on:click="ToLogin">已有账号？马上登录</span>
      </div>
  </div>
</template>

<script>
import axios from 'axios'
axios.defaults.headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}
export default {
  data () {
    return {
      showLogin: true,
      showRegister: false,
      showTishi: false,
      tishi: '',
      username: '',
      password: '',
      newUsername: '',
      newPassword: '',
      newPassword2: '',
      email: '',
      image: ''
    }
  },
  methods: {
    changeImage (e) {
      var file = e.target.files[0]
      var reader = new FileReader()
      var that = this
      reader.readAsDataURL(file)
      reader.onload = function (e) {
        that.image = this.result
      }
    },
    findPwd () {

    },
    ToRegister () {
      this.showRegister = true
      this.showLogin = false
    },
    ToLogin () {
      this.showRegister = false
      this.showLogin = true
    },
    register () {
      let reg = /^[a-zA-Z0-9_-]+@([a-zA-Z0-9]+\.)+(com|cn|net|org)$/
      if (this.newUsername === '' || this.newPassword === '') {
        alert('用户名或密码为空')
      } else if (this.newPassword !== this.newPassword2) {
        this.newPassword = ''
        this.newPassword2 = ''
        alert('两次密码不一致')
      } else if (!reg.test(this.email)) {
        alert('邮箱格式不正确')
        this.email = ''
      } else {
        // let data = {'username': this.newUsername, 'password': this.newPassword, 'email': this.email, 'image': this.image}
        var data = new FormData()
        data.append('username', this.newUsername)
        data.append('password', this.newPassword)
        data.append('email', this.email)
        data.append('image', this.$refs.avatarInput.files[0])
        axios.post('/vueapi/register', data, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then((res) => {
          console.log(res)
          if (res.data['data'] === 'ok') {
            this.tishi = '注册成功'
            this.showTishi = true
            this.newUsername = ''
            this.newPassword = ''
            this.newPassword2 = ''
            this.email = ''
            setTimeout(function () {
              this.showRegister = false
              this.showLogin = true
              this.showTishi = false
            }.bind(this), 1000)
          } else {
            this.tishi = res.data['data']
            this.showTishi = true
            this.newUsername = ''
            this.newPassword = ''
            this.newPassword2 = ''
            this.email = ''
          }
        })
      }
    },
    login () {
      if (this.username === '' || this.password === '') {
        alert('用户名或密码为空')
      } else {
        let data = {'username': this.username, 'password': this.password}
        axios.post('/vueapi/login', data).then((res) => {
          console.log(res)
          if (res.data['data'] === 'ok') {
            this.$emit('userSignIn', res.data)
            this.tishi = '登录成功，即将跳转'
            this.showTishi = true
            setTimeout(function () {
              this.$router.push({ path: '/main', query: {id: 0} })
            }.bind(this), 500)
          } else {
            this.tishi = '与服务器断开连接'
            this.showTishi = true
          }
        })
      }
    }

  }
}
</script>

<style scoped>
.login-wrap{
  text-align:center;
}
.register-wrap{text-align:center;}
input{display:block; width:300px; height:40px; line-height:40px; margin:0 auto; margin-bottom: 10px; outline:none; border:1px solid #888; padding:10px; box-sizing:border-box;}
p{color:red;}
button{display:block; width:300px; height:40px; line-height: 40px; margin:0 auto; border:none; background-color:#41b883; color:#fff; font-size:16px; margin-bottom:5px;}
span{cursor:pointer;}
.cannot-login{
  display: inline-block;
  float: right;
}
span:hover{color:#41b883;}
</style>
