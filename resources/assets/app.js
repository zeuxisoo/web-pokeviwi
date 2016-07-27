import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

var Router = new VueRouter({
    hashbang: false,
    history: true,
    saveScrollPosition: true
})

Router.map({
    '/': {
        name     : 'home',
        component: require('./views/home.vue')
    },
})


var filters = require('./filters');

for(var filter in filters) {
    Vue.filter(filter, filters[filter]);
}

Router.start(Vue.extend(require('./views/app.vue')), '#app')
