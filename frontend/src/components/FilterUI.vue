<template>
  <div>
    <div class="row my-4">
      <div class="col-md-12">
        {{ $gettext("Please use the filter on the left hand side to narrow down your search results. Select the parties to be contacted and click the Contact button below the table to send a message") }}
      </div>
    </div>
    <b-form class="row my-4">
      <b-form-group
        class="col-md"
        :label="$gettext('Country-Code')"
        label-for="location_country_code"
        :state="errorMessages.location_country_code.length === 0"
        :invalid-feedback="errorMessages.location_country_code.join(' ')"
      >
        <b-form-select
          id="location_country_code"
          v-model="location.countryCode"
          @change="fetchResults"
          :state="errorMessages.location_country_code.length === 0"
          :options="filterModel.location.location_country_code.map(e => ({ value: e[0], text: e[1] }))">
        </b-form-select>
      </b-form-group>
      <b-form-group
        class="col-sm"
        :label="$gettext('ZIP-Code')"
        label-for="location_zipcode"
        :state="errorMessages.location_zipcode.length === 0"
        :invalid-feedback="errorMessages.location_zipcode.join(' ')"
      >
        <b-input id="location_zipcode" v-model="location.zipCode" @input="fetchResults" :state="errorMessages.location_zipcode.length === 0"></b-input>
      </b-form-group>
      <b-form-group
        class="col-sm"
        :label="$gettext('Distance')"
        label-for="location_distance"
        :state="errorMessages.location_distance.length === 0"
        :invalid-feedback="errorMessages.location_distance.join(' ')"
      >
        <b-form-select
          id="location_distance"
          v-model="location.distance"
          @change="fetchResults"
          :state="errorMessages.location_distance.length === 0"
          :options="filterModel.location.location_distance.map(e => ({ value: e[0], text: e[1] }))"
        >
        </b-form-select>
      </b-form-group>
    </b-form>
    <div class="row my-5">
      <div class="col-lg-2 filter-search-criteria">
        <faceted-filter :filter-model="filterModel" @updateQuery="updateQuery" ref="filter" />
      </div>
      <div class="col-lg-10 filter-search-results">
        <div class="card">
          <h5 class="card-header"> <b-spinner small variant="primary" v-if="loading" :label="$gettext( 'Loading...' )"> </b-spinner>{{ $gettext('Search Results') }}</h5>
          <div class="card-body">
            <filter-results
              :field-labels="fieldLabels"
              :filter-model="filterModel"
              :results="results"
              :current-page="currentPage"
              :total-rows="numberOfResults"
              :items-per-page="itemsPerPage"
              ref="results"
              @pageChanged="pageChanged">
            </filter-results>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import FacetedFilter from './FilterUIFacetedFilter'
import FilterResults from './FilterUIResults'
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
      numberOfResults: 0,
      itemsPerPage: 10,
      urls: {
        filterModel: '',
        participantList: '',
        tableLayout: '',
      },
      lastFetchRequestAbortController: new AbortController(),
      initialURLParameters: new URLSearchParams(window.location.search),
      filterModelPromise: null,
      loading: false,
      currentPage: 1,
      fieldLabels: [],
      errorMessages: {
        location_country_code: [],
        location_zipcode: [],
        location_distance: [],
      },
    }
  },
  components: {
    FacetedFilter,
    FilterResults,
  },
  methods: {
    updateQuery(event) {
      this.componentQueryStrings[event.path] = event.queryString
      console.debug('Updated queryString from component',event)
      this.$refs.results.clearSelection()
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
    pageChanged(page) {
      this.fetchResults(true, page )
    },
    fetchResults: _.debounce(function (saveState = true, page = 1) {
      console.debug('Fetch Results',{ saveState, page })
      page = Math.max(1,page)
      if (page > 1 && page === this.currentPage) return
      this.loading = true
      this.lastFetchRequestAbortController.abort() // abort old requests
      this.lastFetchRequestAbortController = new AbortController()
      let signal = this.lastFetchRequestAbortController.signal

      let mandatoryParameters = [
        ['location_country_code', this.location.countryCode],
        ['location_zipcode', this.location.zipCode],
        ['location_distance', this.location.distance],
        ['limit', this.itemsPerPage],
        ['offset', (page - 1 ) * this.itemsPerPage],
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
        console.debug('Pushing state to history', { searchParameters: parameters })
      }
      for (let fieldId in this.errorMessages) {
        this.errorMessages[fieldId] = [] // clear error messages
      }
      let response = null
      fetch(`${ this.urls.participantList }?${ urlParameters.toString() }`, { signal })
        .then( r => {
          response = r
          return r.json()
        })
        .then( jsonData => {
          if (response.status === 200) {
            this.results = jsonData.results
            this.numberOfResults = jsonData.count
            this.currentPage = page
          } else {
            for (let fieldId in jsonData) {
              if (Object.prototype.hasOwnProperty.call(this.errorMessages,fieldId)) {
                this.errorMessages[fieldId] = jsonData[fieldId]
              }
            }
            this.numberOfResults = 0
            this.currentPage = 1
          }
        })
        .catch(error => {
          if (error.name !== 'AbortError') {
            console.error('Error retrieving results', error)
          }
        })
        .finally(() => { this.loading = false })
    },250,{ leading:true, trailing: true }), // throttle for 500 ms, execute a last time after thorttling window has elapsed
  },
  mounted() {
    this.buildFilterfromURL(this.initialURLParameters)
    window.addEventListener('popstate', (event) => {
      if (event.state && event.state.searchParameters) {
        this.buildFilterfromURL(new URLSearchParams(event.state.searchParameters))
      }
    })
  },
  beforeMount() {
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
