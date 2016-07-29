<template>
    <div id="app">
        <div class="navbar navbar-default navbar-fixed-top navbar-app" role="navigation">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target=".navbar-collapse">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand">PokeViwi</a>
            </div>
            <div class="collapse navbar-collapse">
                <ul class="nav navbar-nav navbar-left">
                    <li>
                        <a class="nav-link" href="/">
                            <i class="fa fa-home fa-lg" aria-hidden="true"></i> Home
                        </a>
                    </li>
                </ul>
            </div>
        </div>
        <div class="container-fluid">
            <router-view></router-view>
        </div>
        <div class="container-fluid">
            <hr>
            <small class="text-muted">&copy; Notim</small>
        </div>
    </div>
</template>

<style>
body {
    margin-top: 70px;
    margin-bottom: 20px;
}
</style>

<script>
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min'
import 'font-awesome/css/font-awesome.min.css'
import 'sweetalert/dist/sweetalert.css'
import 'toastr/build/toastr.min.css'
import '../css/app.css'

import 'bootstrap'
import 'sweetalert'

export default {

    ready() {
        jQuery('body').tooltip({
            selector: '[data-toggle="tooltip"]'
        })
    }

}
</script>
