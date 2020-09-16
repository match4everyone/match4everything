<template>
  <div>
    <div class="row my-4">
      <div class="col-md-12">
        Allgemeiner Text für den Filter
      </div>
    </div>
    <div class="row my-4">
      <div class="form-group col">
        <label for="location_country_code">Country-Code</label>
        <select class="form-control" id="location_country_code" v-model="location.countryCode" @change="fetchResults" >
          <option
            v-for="countryCode in filterModel.location.location_country_code"
            :value="countryCode[0]"
            :key="countryCode[0]"
          >
            {{countryCode[1]}}
          </option>
        </select>
      </div>
      <div class="form-group col">
        <label for="location_zipcode">ZIP-Code</label>
        <input type="text" class="form-control" id="location_zipcode" v-model="location.zipCode" @input="fetchResults">
      </div>
      <div class="form-group col">
        <label for="location_distance">Distance</label>
        <select class="form-control" id="location_distance" v-model="location.distance" @change="fetchResults" >
          <option
            v-for="distance in filterModel.location.location_distance"
            :value="distance[0]"
            :key="distance[0]"
          >
            {{distance[1]}}
          </option>
        </select>
      </div>
    </div>
    <div class="row my-5">
      <div class="col-lg-3 filter-search-criteria">
        <faceted-filter :filter-model="filterModel" @updateQuery="updateQuery" ref="filter" />
      </div>
      <div class="col-lg-9 filter-search-results">
        <div class="card">
          <h5 class="card-header"><i v-if="loading" class="fa fa-spinner fa-pulse fa-fw"></i>Results</h5>
          <div class="card-body">
            <pre>{{ results | pretty }}</pre>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FacetedFilter from './filter/FacetedFilter'
const _ = require('lodash')

export default {
  name: 'FilterUI',
  data() {
    return {
      filterModel: {
        properties: [],
        location: {
          location_country_code: [],
          location_distance: [],
        },
      },
      location: {
        countryCode: 'DE',
        zipCode: '',
        distance: 10,
      },
      componentQueryStrings: {},
      results: null,
      urls: {
        filterModel: '',
        participantList: '',
        tableLayout: '',
      },
      lastFetchRequestAbortController: new AbortController(),
      initialURLParameters: new URLSearchParams(window.location.search),
      filterModelPromise: null,
      loading: false,
      fieldLabels: [],
    }
  },
  components: {
    FacetedFilter
  },
  methods: {
    updateQuery(event) {
      this.componentQueryStrings[event.path] = event.queryString
      console.log('Updated queryString from component',event)
      this.fetchResults()
    },
    buildFilterfromURL(anURLSearchParams) {
      let parameters = anURLSearchParams
      this.location.zipCode = parameters.get('location_zipcode')
      this.location.distance = parameters.get('location_distance')
      this.location.countryCode = parameters.get('location_country_code')

      this.filterModelPromise.then(() => {
        let queryParameters = this.$refs.filter.buildFilterfromURL(anURLSearchParams)
        queryParameters.forEach((queryParameter) => this.componentQueryStrings[queryParameter.path] = queryParameter.queryString )
        this.fetchResults(false)
      })
    },
    fetchResults: _.debounce(function (saveState = true) {
      console.log('Fetch Results')
      this.loading = true
      this.lastFetchRequestAbortController.abort() // abort old requests
      this.lastFetchRequestAbortController = new AbortController()
      let signal = this.lastFetchRequestAbortController.signal

      let mandatoryParameters = [
        ['location_country_code', this.location.countryCode],
        ['location_zipcode', this.location.zipCode],
        ['location_distance', this.location.distance],
      ]

      let componentParameters = []
      for (let key in this.componentQueryStrings) {
        componentParameters.push(...this.componentQueryStrings[key])
      }

      const parameters = [
        ...mandatoryParameters,
        ...componentParameters,
      ]
      const urlParameters = new URLSearchParams(parameters)

      if (saveState) {
        history.pushState({ searchParameters: parameters },'',`?${ urlParameters.toString() }`)
        console.log('Pushing state to history', { searchParameters: parameters })
      }
      fetch(`${ this.urls.participantList }?${ urlParameters.toString() }`, { signal })
        .then( response => response.json() )
        .then( jsonData => this.results = jsonData)
        .catch(error => {
          if (error.name !== 'AbortError') {
            console.error('Error retrieving results', error)
          }
        })
        .finally(() => { this.loading = false })
    },250,{ leading:true, trailing: true }), // throttle for 500 ms, execute a last time after thorttling window has elapsed
  },
  mounted() {
    console.log('Main UI Mounted')
    this.buildFilterfromURL(this.initialURLParameters)

    window.addEventListener('popstate', (event) => {
      if (event.state && event.state.searchParameters) {
        this.buildFilterfromURL(new URLSearchParams(event.state.searchParameters))
      }
    })

  },
  beforeMount() {
    console.log('Main UI created')
    this.urls.filterModel = this.$el.getAttribute('data-filter-model-url')
    this.urls.participantList = this.$el.getAttribute('data-get-participant-url')
    this.urls.tableLayout = this.$el.getAttribute('data-table-layout-url')
    this.filterModelPromise = fetch(this.urls.filterModel)
      .then( response => response.json() )
      .then( jsonData => this.filterModel = jsonData )
    fetch(this.urls.tableLayout)
      .then( response => response.json() )
      .then( jsonData => {
        this.fieldLabels = Object.keys(jsonData).map( k => ({
          key: k,
          label: String(jsonData[k]),
        }))
      })
  },
}
</script>

<style>
</style>
