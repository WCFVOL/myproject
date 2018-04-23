import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import login from '@/components/login'
import main from '@/components/main'
import NotFound from '@/components/NotFound'
import maintest from '@/components/maintest'
import test from '@/components/test'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/test',
      name: 'test',
      component: test
    },
    {
      path: '/',
      name: 'login',
      component: login
    },
    {
      path: '/main',
      name: 'main',
      component: main,
      children: [
        { path: '', component: main }
      ],
      meta: { requiresAuth: true }
    },
    {
      path: '/404',
      name: '404',
      component: NotFound
    },
    {
      path: '/maintest',
      name: 'maintest',
      component: maintest
    },
    {
      path: '*',
      redirect: '404'
    }
  ]
})
