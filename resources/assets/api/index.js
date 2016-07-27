import Vue from 'vue'
import VueResource from 'vue-resource'
import Pokemon from './pokemon'

Vue.use(VueResource)

export default {

    pokemon: new Pokemon(Vue),

}
