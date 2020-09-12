<template>
  <accordion :label="options.label" :badgeContent="searchText === '' ? null : 1" ref="accordion">
    <div class="form-group">
      <input
        class="form-control form-control-sm"
        type="text"
        :name="namePath"
        :id="`${ namePath }`"
        v-model="searchText"
        @input="selectionChanged">
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
  name : 'TextProperty',
  components: {
    Accordion
  },
  data: function () {
    return {
      searchText: ''
    }
  },
  methods: {
    selectionChanged() {
      this.$emit('updateQuery',this.buildQueryParametersFromSelection())
    },
    clear() {
      this.searchText = ''
      this.selectionChanged()
      this.$refs.accordion.hide()
    },
    buildFilterfromURL(urlParameters) {
      const parameter = `${ this.namePath }__icontains`
      if (urlParameters.has(parameter)) {
        this.searchText = urlParameters.get(parameter)
      }

      this.searchText !== '' ? this.$refs.accordion.show() : this.$refs.accordion.hide()
      return [this.buildQueryParametersFromSelection()]
    },
    buildQueryParametersFromSelection() {
      return {
        path: this.namePath,
        queryString: this.searchText !== '' ? [[`${ this.namePath }__icontains`, this.searchText]] : []
      }
    }
  },
}
</script>
