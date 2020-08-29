<template>
  <accordion :label="options.label" :badgeContent="selected.length ? selected.length : null" ref="accordion">
    <div class="form-group">
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
    <div class="form-group">
      <button type="button" class="btn btn-secondary btn-sm" @click="clear"><span class="fa fa-trash-o"></span> Zurücksetzen</button>
    </div>
  </accordion>
</template>

<script>
import BaseProperty from './BaseProperty'
import Accordion from '../Accordion'

export default {
  extends: BaseProperty,
  name : 'MultipleChoiceProperty',
  components: {
    Accordion
  },
  data: function () {
    return {
      selected: []
    }
  },
  methods: {
    selectionChanged() {
      this.$emit('updateQuery',this.buildQueryParametersFromSelection())
    },
    clear() {
      this.selected = []
      this.selectionChanged()
      this.$refs.accordion.hide()
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
