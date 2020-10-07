<template>
  <v-container
    id="dashboard"
    fluid
    tag="section"
  >
    <v-row>
      <v-col
        cols="12"
        md="6"
      >
        <base-material-card
          color="warning"
          class="px-5 py-3"
        >
          <template v-slot:heading>
            <div class="display-2 font-weight-light">
              Liste des matchs
            </div>
          </template>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="matchs"
              :single-expand="true"
              :expanded.sync="expanded"
              show-expand
              class="elevation-1"
              @click:row="clickedExpand"
              item-key="match_id"
            >
              <template
              v-slot:expanded-item="{headers, item}"
              >
                <td
                :colspan="headers.length"
                >
                  {{ item.blue.team_name }} vs {{ item.red.team_name }}
                </td>
              </template>
            </v-data-table>
          </v-card-text>
        </base-material-card>
      </v-col>
    <template v-if="showStat">
      <v-col
        cols="12"
        sm="6"
        lg="3"
      >
        <base-material-stats-card
          color="red"
          icon="mdi-counter"
          :title="expanded[0].red.team_name"
          :value="expanded[0].red.goals + ' but(s)'"
        />
      </v-col>
      <v-col
        cols="12"
        sm="6"
        lg="3"
      >
        <base-material-stats-card
          color="blue"
          icon="mdi-counter"
          :title="expanded[0].blue.team_name"
          :value="expanded[0].blue.goals + ' but(s)'"
        />
      </v-col>
      <v-col
        cols="12"
        sm="6"
        lg="3"
      >
        <base-material-stats-card
          color="red"
          icon="mdi-soccer"
          title="Possession"
          :value="expanded[0].red.possesion + '%'"
        />
      </v-col>
      <v-col
        cols="12"
        sm="6"
        lg="3"
      >
        <base-material-stats-card
          color="blue"
          icon="mdi-soccer"
          title="Possession"
          :value="expanded[0].blue.possesion + '%'"
        />
      </v-col>
    </template>
    </v-row>
  </v-container>
</template>

<script>
  import axios from 'axios'

  export default {
    name: 'DashboardDashboard',

    data () {
      return {
        expanded: [],
        showStat: false,
        stats: [],
        matchs: [],
        headers: [
          {
            sortable: false,
            text: 'ID',
            value: 'match_id',
          },
          {
            sortable: false,
            text: 'Nom',
            value: 'match_name',
          },
          {
            sortable: false,
            text: 'Durée (minute)',
            value: 'durée',
          },
        ],
        list: {
          0: false,
          1: false,
          2: false,
        },
      }
    },

    created () {
      return axios.get('https://api.statfive.fr/matchs')
        .then((res) => {
          if (res.status === 200) {
            this.matchs = res.data
          }
        })
        .catch((e) => {
          console.log(e)
        })
    },

    methods: {
      clickedExpand (value) {
        console.log(this.expanded)
        this.showStat = true
        const newExpand = value
        const oldExpand = this.expanded

        if (oldExpand.length === 0) this.expanded.push(newExpand)
        else {
          if (oldExpand[0].id !== newExpand.id) {
            this.expanded.pop()
            this.expanded.push(newExpand)
          } else {
            this.expanded.pop()
          }
        }
      },
      complete (index) {
        this.list[index] = !this.list[index]
      },
    },
  }
</script>
