import Base from './base'

export default class Player extends Base {

    constructor(vue) {
        super();

        this.vue = vue
    }

    inventory(params) {
        return this.vue.http.post(this.apiUrl('/player/inventory'), params)
    }

}
