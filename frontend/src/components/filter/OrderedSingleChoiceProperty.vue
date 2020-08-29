<template>
  <accordion :label="options.label" :badgeContent="selectionCount" ref="accordion">
    <div class="form-group">
      <label for="min">Mindestens:</label>
      <select class="form-control form-control-sm" v-model="min" id="min" @change="selectionChanged">
        <option
          v-for="(value, key) in options.choices"
          :key="key"
          :value="key"
        >{{ value }}</option>
      </select>
    </div>
    <div class="form-group">
      <label for="max">Höchstens:</label>
      <select class="form-control form-control-sm" v-model="max" id="max" @change="selectionChanged">
        <option
          v-for="(value, key) in options.choices"
          :key="key"
          :value="key"
        >{{ value }}</option>
      </select>
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
      internal: {
        // should only be accessed using the computed min and max properties to ensure consistency between selections
        min: null,
        max: null,
      }
    }
  },
  computed: {
    min: {
      get() {
        return this.internal.min
      },
      set(newValue) {
        this.internal.min = newValue
        if (this.internal.max === null) this.internal.max = this.highestIndex
        this.internal.max = `${ Math.max(this.internal.min, this.internal.max) }`
      }
    },
    max: {
      get() {
        return this.internal.max
      },
      set(newValue) {
        this.internal.max = newValue
        if (this.internal.min === null) this.internal.min = this.lowestIndex
        this.internal.min = `${ Math.min(this.internal.min, this.internal.max) }`
      }
    },
    selectionCount() {
      let min = Number.parseInt(this.min)
      let max = Number.parseInt(this.max)
      return !Number.isNaN(min) && !Number.isNaN(max) ? 1 + max - min : null
    },
    lowestIndex() {
      // Admittedly this is relatively lazy coding and relies on the ES6 ordering of propertys
      // but as the Python Backend contractually should only send integer keys in this object
      // in the correct order this should be sufficient
      let lowestIndex
      for (let choice in this.options.choices) {
        lowestIndex = choice
        break
      }
      return lowestIndex
    },
    highestIndex() {
      // see lowest Index
      let highestIndex
      for (let choice in this.options.choices) {
        highestIndex = choice
      }
      return highestIndex
    }
  },
  methods: {
    selectionChanged() {
      this.$emit('updateQuery',this.buildQueryParametersFromSelection())
    },
    clear() {
      this.internal.min = this.internal.max = null
      this.$refs.accordion.hide()
      this.selectionChanged()
    },
    buildFilterfromURL(urlParameters) {
      this.internal.min = this.internal.max = null // in this case we really want to reset the selection to nothing selected without using the setters

      let possibleURLParameters = [{
        key: `${ this.namePath }__gte`,
        updatePropertyFromParameter: (value) => this.min = value,
      },
      {
        key: `${ this.namePath }__lte`,
        updatePropertyFromParameter: (value) => this.max = value,
      }]

      // Check whether any of the possible URL parameters are present
      possibleURLParameters.forEach( parameter => {
        if (!urlParameters.has(parameter.key)) return
        let value = Number.parseInt(urlParameters.get(parameter.key))
        if (Number.isNaN(value) || !(value in this.options.choices)) return
        // If all checks are valid, update this instances property
        parameter.updatePropertyFromParameter(value)
      }); // one of the few semicolons that may not be omitted, look up ASI (Automatic Semicolon Insertion) if interested why that is

      (this.min !== null ||this.max !== null) ? this.$refs.accordion.show() : this.$refs.accordion.hide()
      return [this.buildQueryParametersFromSelection()]
    },
    buildQueryParametersFromSelection() {
      let queryStringArray = []
      let min = Number.parseInt(this.min)
      let max = Number.parseInt(this.max)

      let addQueryParameterToArray = (targetArray,lookupExpression,value) => {
        if (!Number.isInteger(value)) return
        targetArray.push([
          `${ this.namePath }__${ lookupExpression }`,
          value
        ])
      }

      addQueryParameterToArray(queryStringArray,'gte',min)
      addQueryParameterToArray(queryStringArray,'lte',max)

      return {
        path: this.namePath,
        queryString: queryStringArray,
      }
    }
  },
}
</script>
