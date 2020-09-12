<template>
  <accordion :label="options.label" :badgeContent="selected === '0' ? null : 1" ref="accordion">
    <div class="form-group">
      <select
        v-model="selected"
        class="form-control form-control-sm"
        :name="namePath"
        :id="namePath"
        @change="selectionChanged"
      >
        <option value="0"></option>
        <option value="1">Muss ausgewählt sein</option>
        <option value="2">Darf nicht ausgewählt sein</option>
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
const defaultValue = '0'

export default {
  extends: BaseProperty,
  name : 'TextProperty',
  components: {
    Accordion
  },
  data: function () {
    return {
      selected: defaultValue
    }
  },
  methods: {
    selectionChanged() {
      this.$emit('updateQuery',this.buildQueryParametersFromSelection())
    },
    clear() {
      this.selected = defaultValue
      this.selectionChanged()
      this.$refs.accordion.hide()
    },
    buildFilterfromURL(urlParameters) {
      this.selected = defaultValue
      const parameter = `${ this.namePath }`
      if (urlParameters.has(parameter)) {
        this.selected = urlParameters.get(parameter) === 'true' ? 1 : 2
      }

      this.selected !== defaultValue ? this.$refs.accordion.show() : this.$refs.accordion.hide()
      return [this.buildQueryParametersFromSelection()]
    },
    buildQueryParametersFromSelection() {
      return {
        path: this.namePath,
        queryString: this.selected !== defaultValue ? [[this.namePath, this.selected === '1']] : []
      }
    }
  },
}
</script>
