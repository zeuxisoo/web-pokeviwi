<template>
    <div id="home">

        <div id="login" v-if="this.player === null">
            <div class="panel panel-default panel-auth-method">
                <div class="panel-heading">Auth Method</div>
                <div class="panel-body">
                    <form class="form-horizontal">
                        <div class="form-group">
                            <div class="col-sm-12">
                                <select class="form-control" id="auth-method" v-model="auth_method">
                                    <option value="ptc">Ptc</option>
                                    <option value="google">Google</option>
                                </select>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <div class="panel panel-default">
                <div class="panel-heading">Location</div>
                <div class="panel-body">
                    <div class="form-inline">
                        <div class="form-group">
                            <label class="sr-only" for="latitude">Latitude</label>
                            <input type="latitude" class="form-control" id="latitude" placeholder="Latitude" v-model="latitude">
                        </div>
                        <div class="form-group">
                            <label class="sr-only" for="longitude">Longitude</label>
                            <input type="longitude" class="form-control" id="longitude" placeholder="Longitude" v-model="longitude">
                        </div>
                        <button type="button" class="btn btn-default" v-on:click="currentLocation" id="current-location">Current Location</button>
                    </div>
                </div>
            </div>

            <div class="panel panel-default" v-bind:class="{ 'hide': this.auth_method != 'ptc' }">
                <div class="panel-heading">Pokemon Trainer Club</div>
                <div class="panel-body">
                    <div class="form-inline">
                        <div class="form-group">
                            <label class="sr-only" for="username">Username</label>
                            <input type="username" class="form-control" id="username" placeholder="Username" v-model="username">
                        </div>
                        <div class="form-group">
                            <label class="sr-only" for="password">Password</label>
                            <input type="password" class="form-control" id="password" placeholder="Password" v-model="password">
                        </div>
                        <button type="button" class="btn btn-default" v-on:click="loginPtc" id="login-ptc">Login</button>
                    </div>
                </div>
            </div>

            <div class="panel panel-default" v-bind:class="{ 'hide': this.auth_method != 'google' }">
                <div class="panel-heading">Google</div>
                <div class="panel-body">
                    <div class="form-inline">
                        <div class="form-group">
                            <a href="https://accounts.google.com/o/oauth2/auth?client_id=848232511240-73ri3t7plvk96pj4f85uj8otdat2alem.apps.googleusercontent.com&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&scope=openid%20email%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email" target="_blank" class="btn btn-primary">Get Auth Code</a>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" id="auth-code" placeholder="Paste Auth Code Here" v-model="auth_code">
                        </div>
                        <button type="button" class="btn btn-default" v-on:click="loginGoogle" id="login-google">Login</button>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel panel-default" v-if="player !== null">
            <div class="panel-heading">{{ player.username }}</div>
            <div class="panel-body">
                <div class="row">
                    <div class="col-xs-12 col-md-4 text-center button-block">
                        <button type="button" class="btn btn-md btn-danger full-width" v-on:click="logout" id="logout">Logout</a>
                    </div>
                    <div class="col-xs-12 col-md-4 text-center button-block">
                        <button type="button" class="btn btn-md btn-info full-width" v-on:click="showPlayerStats" id="show-player-stats">Show Player Stats</a>
                    </div>
                    <div class="col-xs-12 col-md-4 text-center button-block">
                        <button type="button" class="btn btn-md btn-default full-width" v-on:click="showPokemons" id="show-pokemons">Show Pokemons</a>
                    </div>
                </div>

                <hr>
                <span class="text-success">Currency</span>:
                <span class="text-muted">
                    [ Conis: {{ player.currencies.pokecoin }}, Stardust: {{ player.currencies.stardust }} ]
                </span>

                <span v-if="player_stats != null">
                    -
                    <span class="text-success">Profile</span>:
                    <span class="text-muted">
                        [ Level: {{ player_stats.profile_data.level }}, PokeStop: {{ player_stats.profile_data.poke_stop_visits }}, Captured: {{ player_stats.profile_data.pokemons_captured }} ]
                    </span>

                    -
                    <span class="text-success">PokeBall</span>:
                    <span class="text-muted">
                        [ Base: {{ player_stats.poke_balls.base }}, Great: {{ player_stats.poke_balls.great }}, Ultra: {{ player_stats.poke_balls.ultra }} ]
                    </span>

                    -
                    <span class="text-success">Next LvExp</span>:
                    <span class="text-muted">
                        {{ player_stats.profile_data.next_level_xp - player_stats.profile_data.experience }}
                    </span>
                </span>
            </div>
        </div>

        <div class="pokemon-info" v-if="pokemons.length > 0">
            <div class="panel panel-default">
                <div class="panel-body">
                    <div class="row">
                        <div class="col-md-12">
                            <span class="text-info">Total Pokemon</span>:
                            {{ pokemons.length }}

                            <strong>,</strong>
                            <span class="text-info">Good IV (>= 80%)</span>:
                            {{ stats.total_80_perfect_iv }}

                            <strong>,</strong>
                            <span class="text-info">Good CP (>= 80%)</span>:
                            {{ stats.total_80_perfect_cp }}

                            <strong>,</strong>
                            <span class="text-info">Highest CP</span>:
                            {{ stats.highest_pokemon.cp }}
                        </div>
                    </div>
                </div>
            </div>

            <div class="table-responsive">
                <table class="table table-striped table-bordered table-hover">
                    <thead>
                        <tr>
                            <th>Pokemon</th>
                            <th>Fast</th>
                            <th>Special</th>
                            <th>Level</th>
                            <th v-on:click="sortBy('cp')">CP</th>
                            <th>HP</th>
                            <th class="attack">ATK</th>
                            <th class="defense">DEF</th>
                            <th class="stamina">STA</th>
                            <th v-on:click="sortBy('piv')">IV%</th>
                            <th v-on:click="sortBy('pcp')">CP%</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="pokemon in pokemons | orderBy sortKey -1">
                            <td>
                                <div class="name pull-left">
                                    <img v-bind:src="pokemon.pokemon_id | pokemonIcon" v-on:click="rename($event, pokemon.id)" data-pokemon-icon="{{ pokemon.pokemon_id | pokemonIcon }}">
                                    {{ pokemon.name | formatName }}
                                </div>
                            </td>
                            <td>
                                <span class="pull-left" data-toggle="tooltip" data-placement="top" title="{{ pokemon.move1InformationString }}">{{ pokemon.move1Name | formatName }}</span>
                                <label class="label label-default pull-right visible-md-block visible-lg-block">{{ pokemon.move1 }}</label>
                            </td>
                            <td>
                                <span class="pull-left" data-toggle="tooltip" data-placement="top" title="{{ pokemon.move2InformationString }}">{{ pokemon.move2Name | formatName }}</span>
                                <label class="label label-default pull-right visible-md-block visible-lg-block">{{ pokemon.move2 }}</label>
                            </td>
                            <td>{{ pokemon.level }}</td>
                            <td>{{ pokemon.cp }}</td>
                            <td>
                                <span data-toggle="tooltip" data-placement="top" title="{{ pokemon.hp }} / {{ pokemon.hp_max }}">
                                    {{ pokemon.hp_max }}
                                </span>
                            </td>
                            <td class="attack">{{ pokemon.attack }}</td>
                            <td class="defense">{{ pokemon.defense }}</td>
                            <td class="stamina">{{ pokemon.stamina }}</td>
                            <td>{{ pokemon.perfectIV | formatPercentageWith2Fixed }}</td>
                            <td>
                                <span data-toggle="tooltip" data-placement="top" title="{{ pokemon.maxAndPerfectCPString }}">
                                    {{ pokemon.perfectCP | formatPercentageWith2Fixed }}
                                </span>
                            </td>
                            <td>
                                <button type="button" class="btn btn-xs btn-release" v-on:click="release($event, pokemon.id)" data-pokemon-name="{{ pokemon.name | formatName }}">Transfer</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <a href="#" class="scroll-to-top">&uarr;</a>
    </div>
</template>

<style>
.name {
    display: inline;
}

.button-block {
    padding-top: 2px;
    padding-bottom: 2px;
}

.full-width {
    width: 100%;
}

.scroll-to-top {
    position: fixed;
    bottom: 40px;
    right: 40px;
    z-index: 9999;
    width: 32px;
    height: 32px;
    text-align: center;
    line-height: 30px;
    background: #f5f5f5;
    color: #444;
    cursor: pointer;
    border: 0;
    border-radius: 2px;
    text-decoration: none;
    transition: opacity 0.2s ease-out;
    opacity: 0;
}

.scroll-to-top:hover {
    background: #e9ebec;
}

.scroll-to-top.show {
    opacity: 1;
}

.scroll-to-top a {
    text-decoration: none;
}

#login .panel-auth-method .form-group {
    margin-bottom: 0px;
}

th, td {
    text-align: center;
}

/* th */
th.attack {
    color: #FFFFFF;
    background-color: #8F1D21;
}

th.defense {
    color: #FFFFFF;
    background-color: #003171;
}

th.stamina {
    color: #FFFFFF;
    background-color: #006442;
}

/* td */
td.attack {
    color: #FFFFFF;
    background-color: #DC3023;
}

td.defense {
    color: #FFFFFF;
    background-color: #1F4788;
}

td.stamina {
    color: #FFFFFF;
    background-color: #26A65B;
}

/* overwrite */
.table-striped > tbody > tr:nth-of-type(odd) {
    background-color: #fbfbfb;
}

.btn-release {
    color: #FFFFFF;
    background-color: #f1c40f;
}

.text-release {
    color: #0D5E86;
}

.table-hover > tbody > tr:hover {
    background: rgba(111, 232, 49, 0.39);
}
</style>

<script>
import api from '../api'
import MessageHelper from '../helpers/message'
import * as filters from '../filters'

import LevelToCPM from '../data/level-to-cpm.json'
import PokemonData from '../data/pokemon-data.json'
import Moves from '../data/moves.json'

export default {

    created() {
        let scrollTrigger = 100
        let backToTop = () => {
            let scrollTop = jQuery(window).scrollTop()

            if (scrollTop > scrollTrigger) {
                jQuery('.scroll-to-top').addClass('show')
            }else{
                jQuery('.scroll-to-top').removeClass('show')
            }
        }

        backToTop()

        jQuery(window).on('scroll', () => {
            backToTop()
        })

        jQuery("body").on('click', '.scroll-to-top', (e) => {
            e.preventDefault()

            jQuery('html,body').animate({
                scrollTop: 0
            }, 700)
        })
    },

    data() {
        return {
            username     : "",
            password     : "",
            auth_method  : "ptc",
            latitude     : 0,
            longitude    : 0,
            auth_code    : "",
            sorted_column: 'cp',
            player       : null,
            pokemons     : [],
            player_stats : null,
            stats        : {
                highest_pokemon    : null,
                total_80_perfect_iv: 0,
                total_80_perfect_cp: 0,
            }
        }
    },

    computed: {
        sortKey: {
            get() {
                return this.sorted_column
            }
        }
    },

    methods: {
        currentLocation() {
            if (navigator.geolocation) {
                var currentLocationButton = jQuery("button#current-location")

                currentLocationButton.html("Finding...")
                currentLocationButton.prop("disabled", true)

                navigator.geolocation.getCurrentPosition(
                    position => {
                        let coords    = position.coords
                        let latitude  = coords.latitude
                        let longitude = coords.longitude

                        this.latitude  = latitude
                        this.longitude = longitude

                        currentLocationButton.html("Current Location")
                        currentLocationButton.prop("disabled", false)
                    },
                    () => {
                        this.alertError('Unable to retrieve your location')

                        currentLocationButton.html("Current Location")
                        currentLocationButton.prop("disabled", false)
                    }
                )
            }else{
                this.alertError('Geolocation is not supported by your browser')
            }
        },

        loginPtc() {
            if (this.username === "") {
                this.alertError("Please enter username")
            }else if (this.password === "") {
                this.alertError("Please enter password")
            }else if ($.inArray(this.auth_method, ['ptc', 'google']) === false) {
                this.alertError("Please select your account auth method")
            }else{
                var loginButton = jQuery("button#login-ptc")

                loginButton.html("Signing...")
                loginButton.prop("disabled", true)

                api.auth.loginPtc({
                    username : this.username,
                    password : this.password,
                    latitude : this.latitude,
                    longitude: this.longitude
                }).then(
                    response => {
                        let data   = response.data
                        let player = data.player

                        this.player = player

                        loginButton.html("Login")
                        loginButton.prop('disabled', false)
                    },

                    response => {
                        let data    = response.data
                        let message = ""

                        if (data.ok == false) {
                            if (data.message != "")  {
                                message = data.message
                            }else{
                                message = 'Unable to access response from login server, Please try later'
                            }
                        }else{
                            message = 'Unknow error'
                        }

                        this.alertError(message)

                        loginButton.html("Login")
                        loginButton.prop("disabled", false)
                    }
                )
            }
        },

        loginGoogle() {
            if (this.auth_code === "") {
                this.alertError("Please get the auth code first")
            }else{
                var loginButton = jQuery("button#login-google")

                loginButton.html("Signing...")
                loginButton.prop("disabled", true)

                api.auth.loginGoogle({
                    auth_code: this.auth_code,
                    latitude : this.latitude,
                    longitude: this.longitude
                }).then(
                    response => {
                        let data   = response.data
                        let player = data.player

                        this.player = player

                        loginButton.html("Login")
                        loginButton.prop('disabled', false)
                    },

                    response => {
                        let data    = response.data
                        let message = ""

                        if (data.ok == false) {
                            if (data.message != "")  {
                                message = data.message
                            }else{
                                message = 'Unable to access response from login server, Please try later'
                            }
                        }else{
                            message = 'Unknow error'
                        }

                        this.alertError(message)

                        loginButton.html("Login")
                        loginButton.prop("disabled", false)
                    }
                )
            }
        },

        logout() {
            api.auth.logout({}).then(
                response => {
                    this.player       = null
                    this.pokemons     = []
                    this.player_stats = null
                    this.auth_code    = ""
                },

                response => {
                    let data = response.data

                    if (data.ok === false) {
                        let message = ""

                        if (data.message && data.message != "")  {
                            message = data.message
                        }else{
                            message = 'Cannot logout from application'
                        }

                        this.alertError(message)
                    }
                }
            )
        },

        showPlayerStats() {
            var showButton = jQuery("button#show-player-stats")

            showButton.html("Loading...")
            showButton.prop("disabled", true)

            api.player.stats({}).then(
                response => {
                    let data         = response.data
                    let player_stats = data.player_stats

                    this.player_stats = player_stats

                    showButton.html("Show Player Stats")
                    showButton.prop("disabled", false)
                },

                response => {
                    showButton.html("Show Player Stats")
                    showButton.prop("disabled", false)

                    this.alertError('Cannot show the player stats')
                }
            )
        },

        showPokemons() {
            if (this.player === null) {
                this.alertError("Please login first")
            }else{
                var showButton = jQuery("button#show-pokemons")

                showButton.html("Loading...")
                showButton.prop("disabled", true)

                var moves = this.generateMovesList()

                api.pokemon.all({
                    username   : this.username,
                    password   : this.password,
                    auth_method: this.auth_method,
                }).then(
                    response => {
                        let data     = response.data
                        let pokemons = data.pokemons

                        this.stats.total_80_perfect_iv = 0
                        this.stats.total_80_perfect_cp = 0

                        for(let i=0; i<pokemons.length; i++) {
                            let pokemon = pokemons[i]

                            pokemons[i].name      = pokemon.nickname || this.findPokemonDataById(pokemon.pokemon_id).name || ""
                            pokemons[i].level     = this.determineLevel(pokemon.cp_multiplier)
                            pokemons[i].perfectIV = this.determinePerfectIV(pokemon)
                            pokemons[i].perfectCP = this.determinePerfectCP(pokemon.pokemon_id, pokemon.attack, pokemon.defense, pokemon.stamina)

                            pokemons[i].move1Name = moves[pokemon.move1].Name
                            pokemons[i].move2Name = moves[pokemon.move2].Name

                            pokemons[i].move1InformationString = this.generateMovesInformationString(moves[pokemon.move1])
                            pokemons[i].move2InformationString = this.generateMovesInformationString(moves[pokemon.move2])
                            pokemons[i].maxAndPerfectCPString  = this.generateMaxAndPerfectCPString(pokemon.pokemon_id, pokemon.attack, pokemon.defense, pokemon.stamina)

                            if (this.stats.highest_pokemon === null || this.stats.highest_pokemon.cp < pokemon.cp) {
                                this.stats.highest_pokemon = pokemon
                            }

                            if (pokemon.perfectIV > 0.8) {
                                this.stats.total_80_perfect_iv++
                            }

                            if (pokemon.perfectCP > 0.8) {
                                this.stats.total_80_perfect_cp++
                            }
                        }

                        this.pokemons = pokemons

                        showButton.html("Show Pokemons")
                        showButton.prop("disabled", false)
                    },
                    response => {
                        showButton.html("Show Pokemons")
                        showButton.prop("disabled", false)

                        this.alertError('Cannot show the pokemon list')
                    }
                )
            }
        },

        release(event, pokemonId) {
            let pokemonName = jQuery(event.currentTarget).data('pokemonName')

            if (pokemonId === null || pokemonId === "") {
                this.alertError('Not found pokemon id')
            }else{
                api.pokemon.release({
                    pokemon_id: pokemonId
                }).then(
                    response => {
                        let data  = response.data
                        let candy = data.candy

                        // Remove transfered pokemon in pokemon list
                        this.pokemons = this.pokemons.filter(pokemon => {
                            return pokemon.id !== pokemonId
                        });

                        MessageHelper.success(`Pokemon: <strong class='text-release'>${pokemonName}</strong> transferred, Candy: <strong class='text-release'>${candy}</strong>`)
                    },
                    response => {
                        this.alertError('Transfer action failed!')
                    }
                )
            }
        },

        rename(event, pokemonId) {
            let pokemonName = filters.formatName(this.findPokemonById(pokemonId).name)
            let pokemonIcon = jQuery(event.currentTarget).data('pokemonIcon')

            swal({
                title: "Rename pokemon",
                text: `
                    <p><img src='${pokemonIcon}'></p>
                    <br>
                    <small>${pokemonName}</small>
                `,
                html: true,
                type: "input",
                showCancelButton: true,
                closeOnConfirm: false,
                animation: "slide-from-top",
                inputPlaceholder: pokemonName,
            }, newName => {
                if (newName === false || newName === "") {
                    swal.showInputError("Please eneter pokemon name to rename")
                    return false
                }else{
                    swal.close()

                    api.pokemon.rename({
                        pokemon_id: pokemonId,
                        name      : newName
                    }).then(
                        response => {
                            this.pokemons.forEach(pokemon => {
                                if (pokemon.id == pokemonId) {
                                    pokemon.name = newName
                                }
                            })

                            MessageHelper.success(`Rename <strong>${pokemonName}</strong> to <strong>${newName}</strong> success`)
                        },
                        response => {
                            this.alertError('Rename action failed!')
                        }
                    )
                }
            })
        },

        sortBy(name) {
            let sortMap = {
                'cp' : 'cp',
                'piv': 'perfectIV',
                'pcp': 'perfectCP'
            }

            let column = sortMap[name]

            this.sorted_column = column
            this.pokemons.sort((a, b) => {
                let compareA = a[column]
                let compareB = b[column]

                if (compareA < compareB) return 1
                if (compareA > compareB) return -1

                return 0
            })
        },

        findPokemonById(pokemonId) {
            let pokemon

            for(let i=0; i<this.pokemons.length; i++) {
                if (this.pokemons[i].id == pokemonId) {
                    pokemon = this.pokemons[i]
                    break
                }
            }

            return pokemon
        },

        findPokemonDataById(pokemonId) {
            let pokemon

            for(let i=0; i<PokemonData.length; i++) {
                if (PokemonData[i].id == pokemonId) {
                    pokemon = PokemonData[i]
                    break
                }
            }

            return pokemon
        },

        determineLevel(cpm) {
            let ret = 0

            for(let level in LevelToCPM) {
                if (Math.abs(cpm - LevelToCPM[level]) < 0.0001) {
                    ret = parseFloat(level)
                }
            }

            return ret
        },

        determinePerfectIV(pokemon) {
            if (Math.abs(pokemon.cp_multiplier + pokemon.additional_cp_multiplier) < 0) {
                return (pokemon.attack + pokemon.defense + pokemon.stamina) / 45.0
            }

            let maxCp = this.calculateMaxCpMultiplier(pokemon.pokemon_id)
            let minCp = this.calculateMinCpMultiplier(pokemon.pokemon_id)
            let nowCp = this.calculateCpMultiplier(pokemon)

            return (nowCp - minCp) / (maxCp - minCp)
        },

        determinePerfectCP(pokemonId, individualAttack, individualDefense, individualStamina) {
            let pokemon = this.findPokemonDataById(pokemonId)

            let baseAttack  = pokemon.stats.attack
            let baseDefense = pokemon.stats.defense
            let baseStamina = pokemon.stats.stamina

            let perfectCp = (baseAttack + 15) * Math.pow((baseDefense + 15), 0.5) * Math.pow((baseStamina + 15), 0.5) * (Math.pow(LevelToCPM['40'], 2) / 10)
            let maxCp     = (baseAttack + individualAttack) * Math.pow((baseDefense + individualDefense), 0.5) * Math.pow((baseStamina + individualStamina), 0.5) * (Math.pow(LevelToCPM['40'], 2) / 10)

            return maxCp / perfectCp
        },

        generateMaxAndPerfectCPString(pokemonId, individualAttack, individualDefense, individualStamina) {
            let pokemon = this.findPokemonDataById(pokemonId)

            let baseAttack  = pokemon.stats.attack
            let baseDefense = pokemon.stats.defense
            let baseStamina = pokemon.stats.stamina

            let perfectCp = (baseAttack + 15) * Math.pow((baseDefense + 15), 0.5) * Math.pow((baseStamina + 15), 0.5) * (Math.pow(LevelToCPM['40'], 2) / 10)
            let maxCp     = (baseAttack + individualAttack) * Math.pow((baseDefense + individualDefense), 0.5) * Math.pow((baseStamina + individualStamina), 0.5) * (Math.pow(LevelToCPM['40'], 2) / 10)

            return Math.round(maxCp) + " / " + Math.round(perfectCp)
        },

        generateMovesInformationString(moves) {
            let attack   = moves.Power
            let cooldown = moves.DurationMs / 1000
            let dps      = (moves.Power / moves.DurationMs) * 1000

            return [
                "Atk: " + attack,
                "CD : " + cooldown.toFixed(2),
                "DPS: " + dps.toFixed(2)
            ].join(" - ")
        },

        generateMovesList() {
            let moveList = [];

            for(let i=0; i<Moves.length; i++) {
                let moves = Moves[i];

                moveList[moves.Id] = moves;
            }

            return moveList;
        },

        calculateMaxCpMultiplier(pokemonId) {
            let baseStats = this.findPokemonDataById(pokemonId).stats

            return (baseStats.attack + 15) * Math.sqrt(baseStats.defense + 15) * Math.sqrt(baseStats.stamina + 15)
        },

        calculateMinCpMultiplier(pokemonId) {
            let baseStats = this.findPokemonDataById(pokemonId).stats

            return baseStats.attack * Math.sqrt(baseStats.defense) * Math.sqrt(baseStats.stamina)
        },

        calculateCpMultiplier(pokemon) {
            let baseStats = this.findPokemonDataById(pokemon.pokemon_id).stats

            return (baseStats.attack + pokemon.attack) *
                    Math.sqrt(baseStats.defense + pokemon.defense) *
                    Math.sqrt(baseStats.stamina + pokemon.stamina)
        },

        alertError(message) {
            swal("Error!", message, "error")
        }
    }

}
</script>
