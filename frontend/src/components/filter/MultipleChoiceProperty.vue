<template>
  <div>
    <div v-for="(value, key) in options.choices" class="form-check" :key="key">
      <input
        class="form-check-input"
        type="checkbox"
        :name="namePath"
        :id="`${ namePath }-${ key }`"
        :value="key"
        v-model="selected"
        @change="selectionChanged">
      <label
        class="form-check-label"
        :for="`${ namePath }-${ key }`"
        :key="`label-${ value }`">
        {{ value }}
      </label>
    </div>
  </div>
</template>

<script>
import BaseProperty from './BaseProperty'

export default {
  extends: BaseProperty,
  name : 'MultipleChoiceProperty',
  data: function () {
    return {
      selected: []
    }
  },
  methods: {
    selectionChanged() {
      this.$emit('updateQuery',this.buildQueryParametersFromSelection())
    },
    buildFilterfromURL(urlParameters) {
      // Build an array of possible URL parameters for the selectable options
      let possibleURLParameters = Object.keys(this.options.choices).map(key => {
        return {
          key: key,
          parameter: `${ this.namePath }-${ key }`,
        }
      })

      // Check whether any of the possible URL parameters are present
      let presentURLParameters = possibleURLParameters.filter( keyParameterTuple => {
        return urlParameters.has(keyParameterTuple.parameter)
      })

      // Preset selection based on URL parameters and return query parameters for the selection
      this.selected = presentURLParameters.map(keyParameterTuple => keyParameterTuple.key )
      return [this.buildQueryParametersFromSelection()]
    },
    buildQueryParametersFromSelection() {
      return {
        path: this.namePath,
        queryString: this.selected.map(key => [`${ this.namePath }-${ key }`, true])
      }
    }
  },
}
</script>
