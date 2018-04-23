// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.config.productionTip = false
/* eslint-disable no-new */
Vue.use(ElementUI)
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
router.beforeEach((to, from, next) => {
  // 可以在路由元信息指定哪些页面需要登录权限
  const islogin = sessionStorage.nickname === undefined // 假设没有登录（这里应从接口获取）
  if (to.path === '/main' && islogin) { // 需要登录授权，这里还需要判断是否登录
    next('/') // 跳转到登录
    return
  }
  next()
})
