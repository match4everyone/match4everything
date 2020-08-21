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
        <input type="text" class="form-control" id="location_country_code" v-model="location.countryCode" @change="fetchResults">
      </div>
      <div class="form-group col">
        <label for="location_zipcode">ZIP-Code</label>
        <input type="text" class="form-control" id="location_zipcode" v-model="location.zipCode" @change="fetchResults">
      </div>
      <div class="form-group col">
        <label for="location_distance">Distance</label>
        <div class="input-group">
          <input type="text" class="form-control" id="location_distance" v-model="location.distance" @change="fetchResults">
          <div class="input-group-append">
            <span class="input-group-text">km</span>
          </div>
        </div>
      </div>
    </div>
    <div class="row my-5">
      <div class="col-lg-3 filter-search-criteria">
        <faceted-filter :filter-model="filterModel" @updateQuery="updateQuery" />
      </div>
      <div class="col-lg-9 filter-search-results">
        <div class="card">
          <h5 class="card-header">Results</h5>"
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
const abortController = new AbortController() // Used to cancel fetch requests

export default {
  name: 'FilterUI',
  data() {
    return {
      filterModel: {
        properties: []
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
      },
      lastFetchRequestAbortController: new AbortController(),
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
    fetchResults() {
      this.lastFetchRequestAbortController.abort() // abort old requests
      this.lastFetchRequestAbortController = new AbortController()
      let signal = abortController.signal

      let mandatoryParameters = [
        ['location_country_code', this.location.countryCode],
        ['location_zipcode', this.location.zipCode],
        ['location_distance', this.location.distance],
      ]

      let componentParameters = []
      for (let key in this.componentQueryStrings) {
        componentParameters.push(...this.componentQueryStrings[key])
      }

      const parameters = new URLSearchParams([
        ...mandatoryParameters,
        ...componentParameters,
      ])


      fetch(`${ this.urls.participantList }?${ parameters.toString() }`, { signal })
        .then( response => response.json() )
        .then( jsonData => this.results = jsonData)
    }
  },
  beforeMount() {

    this.urls.filterModel = this.$el.getAttribute('data-filter-model-url')
    this.urls.participantList = this.$el.getAttribute('data-get-participant-url')

    fetch(this.urls.filterModel)
      .then( response => response.json() )
      .then( jsonData => this.filterModel = jsonData)
  },
  filters: {
    pretty: function(value) {
      return JSON.stringify(value, null, 2)
    },
  }
}
</script>

<style>
</style>
