import Base from './base'

export default class Auth extends Base {

    constructor(vue) {
        super();

        this.vue = vue
    }

    loginPtc(params) {
        return this.vue.http.post(this.apiUrl('/auth/login/ptc'), params)
    }

    loginGoogle(params) {
        return this.vue.http.post(this.apiUrl('/auth/login/google'), params)
    }

    logout(data) {
        return this.vue.http.get(this.apiUrl('/auth/logout'), data)
    }

}
