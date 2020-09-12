<template>
  <div class="my-3 mx-2">
    <div class="form-check">
      <input
        class="form-check-input"
        type="checkbox"
        :name="namePath"
        v-model="selected"
        @change="selectionChanged">
      <label
        class="form-check-label"
        :for="namePath">
        {{ options.label }}
      </label>
    </div>
    <div class="collapse" ref="collapsible">
      <div>
        <PropertyGroup :options="options" :parent-name="parentName" ref="propertyGroup" @updateQuery="forwardEvent"/>
      </div>
    </div>
  </div>
</template>
<script>
import BaseProperty from './BaseProperty'
import PropertyGroup from './PropertyGroup'

export default {
  extends: BaseProperty,
  name: 'ConditionalPropertyGroup',
  components: {
    PropertyGroup
  },
  data() {
    return {
      selected: false
    }
  },
  methods: {
    toggle() {
      this.$jQuery(this.$refs.collapsible).collapse('toggle')
    },
    show() {
      this.$jQuery(this.$refs.collapsible).collapse('show')
    },
    hide() {
      this.$jQuery(this.$refs.collapsible).collapse('hide')
    },
    selectionChanged() {
      if (this.selected) {
        this.show()
      } else {
        this.hide()
        this.$refs.propertyGroup.clear()
      }
      this.$emit('updateQuery',this.buildQueryParametersFromSelection())
    },
    clear() {
      this.selected = false
      this.selectionChanged()
      this.$refs.propertyGroup.clear()
    },
    forwardEvent(event) {
      this.$emit('updateQuery',event)
    },
    buildFilterfromURL(urlParameters) {
      this.selected = urlParameters.has(`${ this.namePath }-cond`) && urlParameters.get(`${ this.namePath }-cond`) === 'true'
      this.selected ? this.show() : this.hide()

      return [
        this.buildQueryParametersFromSelection(),
        ...this.$refs.propertyGroup.buildFilterfromURL(urlParameters)
      ]
    },
    buildQueryParametersFromSelection() {
      return {
        path: this.namePath,
        queryString: this.selected ? [[`${ this.namePath }-cond`, true]]: []
      }
    }

  },
}
</script>
