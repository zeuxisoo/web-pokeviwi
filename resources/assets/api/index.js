import Vue from 'vue'
import VueResource from 'vue-resource'
import Auth from './auth'
import Pokemon from './pokemon'

Vue.use(VueResource)

export default {

    auth   : new Auth(Vue),
    pokemon: new Pokemon(Vue),

}
