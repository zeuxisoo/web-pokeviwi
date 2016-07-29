import Base from './base'

export default class Pokemon extends Base {

    constructor(vue) {
        super();

        this.vue = vue
    }

    all(params) {
        return this.vue.http.post(this.apiUrl('/pokemon/all'), params)
    }

    release(params) {
        return this.vue.http.post(this.apiUrl('/pokemon/release'), params)
    }

}
