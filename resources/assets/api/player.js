import Base from './base'

export default class Player extends Base {

    constructor(vue) {
        super();

        this.vue = vue
    }

    stats(params) {
        return this.vue.http.post(this.apiUrl('/player/stats'), params)
    }

}
