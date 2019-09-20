import firebase from 'firebase'

import Vue from 'vue'
import Router from 'vue-router'
import UtilsPing from '@/components/UtilsPing'
import UserHome from '@/components/UserHome'
import UserSettings from '@/components/UserSettings'
import MainAbout from '@/components/MainAbout'
import MainDocs from '@/components/MainDocs'
import PublicLogin from '@/components/PublicLogin'

Vue.use(Router);

const router = new Router({
  routes: [
    {
        path: '*',
        redirect: '/public/404'
    },
    {
        path: '/',
        redirect: '/public/login',
    },
    {
        path: '/public/login',
        name: 'PublicLogin',
        component: PublicLogin,
    },
    {
        path: '/user/home',
        name: 'Home',
        component: UserHome,
        meta: {
          requiresAuth: true
        }
    },
      {
        path: '/user/settings',
        name: 'UserSettings',
        component: UserSettings,
        meta: {
          requiresAuth: true
        },

    },
    {
        path: '/main/about',
        name: 'MainAbout',
        component: MainAbout,
        meta: {
          requiresAuth: true
        }
    },

    {
        path: '/main/docs',
        name: 'MainDocs',
        component: MainDocs,
        meta: {
          requiresAuth: true
        }
    },

    {
        path: '/utils/ping',
        name: 'UtilsPing',
        component: UtilsPing,
        meta: {
          requiresAuth: true
        },
    },
  ],
  mode: 'history'
});

// Navigation Guard

router.beforeEach((to, from, next) => {

    const user = firebase.auth().currentUser;
    const auth = to.matched.some(
        record => record.meta.requiresAuth
    );
    if (auth && !user) {
        next() // next('login')
    } else if (!auth && user) {
        next()
    } else {
        next()
    }
});

export default router;