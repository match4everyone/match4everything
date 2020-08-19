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
        <input type="text" class="form-control" id="location_country_code" v-model="countryCode">
      </div>
      <div class="form-group col">
        <label for="location_zipcode">ZIP-Code</label>
        <input type="text" class="form-control" id="location_zipcode" v-model="zipCode">
      </div>
      <div class="form-group col">
        <label for="location_distance">Distance</label>
        <div class="input-group">
          <input type="text" class="form-control" id="location_distance" v-model="distance">
          <div class="input-group-append">
            <span class="input-group-text">km</span>
          </div>
        </div>
      </div>
    </div>
    <div class="row my-5">
      <div class="col-lg-3 filter-search-criteria">
        <h1>Filter</h1>
        <component
          v-for="property in filterModel.properties"
          :is="convertTypeToComponentName(property.type)"
          :key="property.name"
          :options="property">
        </component>
      </div>
      <div class="col-lg-9 filter-search-results">
        <div class="card">
          <h5 class="card-header">Results</h5>
          <div class="card-body">
            Bla bla bla
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FilterComponentManager } from '../utils/FilterComponentManager'

export default {
  name: 'FilterUI',
  data() {
    return {
      filterModel: {
        properties: []
      },
      countryCode: 'DE',
      zipCode: '',
      distance: 10,
    }
  },
  methods: {
    valueSelected(value) {
      console.log(value)
    },
    convertTypeToComponentName(typeName) {
      return FilterComponentManager.getComponentForType(typeName)
    }
  },
  beforeMount() {
    fetch(this.$el.getAttribute('data-filter-model-url'))
      .then( response => response.json() )
      .then( jsonData => this.filterModel = jsonData)
  }

}
</script>

<style>
</style>
