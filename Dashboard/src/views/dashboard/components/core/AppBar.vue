<template>
  <v-app-bar
    id="app-bar"
    absolute
    app
    color="transparent"
    flat
    height="100"
  >
    <v-btn
      class="mr-3"
      elevation="1"
      fab
      small
      @click="setDrawer(!drawer)"
    >
      <v-icon v-if="value">
        mdi-view-quilt
      </v-icon>

      <v-icon v-else>
        mdi-dots-vertical
      </v-icon>
    </v-btn>

    <v-toolbar-title
      class="hidden-sm-and-down font-weight-light"
      v-text="$route.name"
    />

    <v-spacer />

    <v-text-field
      :label="$t('search')"
      color="secondary"
      hide-details
      style="max-width: 165px;"
    >
      <template
        v-if="$vuetify.breakpoint.mdAndUp"
        v-slot:append-outer
      >
        <v-btn
          class="mt-n2"
          elevation="1"
          fab
          small
        >
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
      </template>
    </v-text-field>

    <div class="mx-3" />

    <div
    style="width: 15%; text-align: center"
    v-if="!connected"
    >
    <v-dialog
      v-model="login"
      persistent
      max-width="600px"
      >
          <template v-slot:activator="{ on, attrs }">
              <div
              style="display: inline-block"
              >
                  <v-btn
                    class="ml-2"
                    min-width="0"
                    text
                    v-bind="attrs"
                    v-on="on"
                  >Connexion
                  </v-btn>
              </div>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">Connexion</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                        color="indigo"
                        label="Email*"
                        required
                        v-model="email"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                        color="indigo"
                        label="Mot de passe*"
                        required
                        v-model="password"
                        type="password"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                  <small>*Champs obligatoires</small>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                  color="indigo"
                  text
                  @click="login = false"
                  >Fermer</v-btn>
                  <v-btn
                  color="indigo"
                  text
                  @click="auth()"
                  >Connexion</v-btn>
                </v-card-actions>
              </v-card>
              <v-snackbar
                v-model="snackbar"
                :multi-line="multiLine"
              >
                {{ text }}

                <template v-slot:action="{ attrs }">
                  <v-btn
                    color="red"
                    text
                    v-bind="attrs"
                    @click="snackbar = false"
                  >
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-dialog>

    <v-dialog
      v-model="register"
      persistent
      max-width="600px"
      >
              <template v-slot:activator="{ on, attrs }">
              <div
              style="display: inline-block"
              >
                   <v-btn
                    class="ml-2"
                    min-width="0"
                    text
                    v-bind="attrs"
                    v-on="on"
                    >Inscription
                  </v-btn>
              </div>
              </template>
              <v-card>
                <v-card-title>
                  <span class="headline">Inscription</span>
                </v-card-title>
                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <v-text-field
                        label="Email*"
                        color="indigo"
                        required
                        v-model="email"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                        color="indigo"
                        label="Nom*"
                        required
                        v-model="lastname"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                        color="indigo"
                        label="Prénom*"
                        required
                        v-model="firstname"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                        color="indigo"
                        label="Mot de passe*"
                        required
                        v-model="password"
                        type="password"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12">
                        <v-text-field
                          label="Confirmation mot de passe*"
                          color="indigo"
                          type="password"
                          required
                          v-model="passwordConfirmation"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-container>
                  <small>*Champs obligatoires</small>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                  color="indigo"
                  text
                  @click="register = false"
                  >Fermer</v-btn>
                  <v-btn
                  color="indigo"
                  text
                  @click="signin()"
                  >Inscription</v-btn>
                </v-card-actions>
              </v-card>
              <v-snackbar
                v-model="snackbar"
                :multi-line="multiLine"
              >
                {{ text }}

                <template v-slot:action="{ attrs }">
                  <v-btn
                    color="red"
                    text
                    v-bind="attrs"
                    @click="snackbar = false"
                  >
                    Close
                  </v-btn>
                </template>
              </v-snackbar>
            </v-dialog>
    </div>

    <div v-else>

    <v-btn
      class="ml-2"
      min-width="0"
      text
      to="/"
    >
      <v-icon>mdi-view-dashboard</v-icon>
    </v-btn>

    <v-btn
      class="ml-2"
      min-width="0"
      text
      to="/pages/user"
    >
      <v-icon>mdi-account</v-icon>
    </v-btn>
    </div>
  </v-app-bar>
</template>

<script>
  // Utilities
  import { mapState, mapMutations } from 'vuex'
  import axios from 'axios'

  export default {
    name: 'DashboardCoreAppBar',

    components: {
    },

    props: {
      value: {
        type: Boolean,
        default: false,
      },
    },

    data: () => ({
      multiLine: true,
      snackbar: false,
      text: '',
      login: false,
      register: false,
      username: '',
      email: '',
      password: '',
      passwordConfirmation: '',
      firstname: '',
      lastname: '',
    }),

    computed: {
      ...mapState(['drawer', 'connected', 'admin']),
    },

    methods: {
      ...mapMutations({
        setDrawer: 'SET_DRAWER',
        setStatus: 'SET_STATUS',
        setUser: 'SET_USER',
        setAdmin: 'SET_ADMIN',
      }),

      auth () {
        return axios.post('https://api.statfive.fr/login', {
          email: this.email,
          password: this.password,
        },
        )
          .then((res) => {
            if (res.status === 200) {
              if (res.data.Connected) {
                this.setStatus(res.data.Connected)
                this.setUser(res.data.User[0])
                if (res.data.User[0].role === 1) {
                  console.log(this.admin)
                  this.setAdmin(true)
                  console.log(this.admin)
                }
                this.login = true
              } else {
                this.snackbar = true
                this.text = 'Erreur mail/mot de passe'
              }
            }
          })
          .catch((e) => {
            console.log(e)
          })
      },

      signin () {
        return axios.post('https://api.statfive.fr/addUser', {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          firstname: this.firstname,
          lastname: this.lastname,
          email: this.email,
          password: this.password,
          c_password: this.passwordConfirmation,
        },
        )
          .then((res) => {
            if (res.data.about === 'Mail exist') {
              this.snackbar = true
              this.text = 'Email déjà utilisé'
            } else {
              this.register = false
              this.login = true
              console.log(res)
            }
          })
          .catch((e) => {
            console.log(e)
          })
      },
    },
  }
</script>
