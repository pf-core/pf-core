import "../css/lux.min.css";
import "../css/loader.css";
import 'vuesax/dist/vuesax.css'; // Vuesax styles
import 'material-icons/iconfont/material-icons.css';

import firebase from 'firebase/app';
import firebaseConfig from './secrets/firebase.json'

import Vue from 'vue'
import App from './App'
import router from './router'
import HighchartsVue from 'highcharts-vue'
import BootstrapVue from 'bootstrap-vue'
import VModal from 'vue-js-modal'
import VueMarkdown from 'vue-markdown'
import VueCarousel from 'vue-carousel'
import D3Chart from './assets/d3-chart-plugin.js'
import Vuesax from 'vuesax';
import VueFullPage from 'vue-fullpage.js';
import VueTagsInput from '@johmun/vue-tags-input';

Vue.config.productionTip = false;

Vue.use(VueTagsInput);
Vue.use(VueFullPage);
Vue.use(HighchartsVue);
Vue.use(Vuesax);
Vue.use(D3Chart);
Vue.use(VModal);
Vue.use(BootstrapVue);
Vue.use(VueCarousel);
Vue.use(VueMarkdown);


import SocketIO from  'socket.io-client'
import VueSocketIO from 'vue-socket.io'

Vue.use(new VueSocketIO({
    debug: true,
    connection: SocketIO('http://localhost:5000/')
  })
);

import Highcharts from 'highcharts'
import exportingInit from 'highcharts/modules/exporting'
import highchartsMore from 'highcharts/highcharts-more'

highchartsMore(Highcharts);
exportingInit(Highcharts);

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

let app = '';

firebase.auth().onAuthStateChanged(() => {
    if (!app) {
        new Vue({
            el: '#app',
            router,
            render: h => h(App)
        });
    }
});

