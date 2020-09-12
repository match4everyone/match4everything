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
        <ul class="list-group my-2">
          <li
            v-for="child_property in options.properties"
            :key="child_property.name"
            class="list-group-item p-0"
          >
            <component :is="convertTypeToComponentName(child_property.type)" :options="child_property" :parentName="namePath" @updateQuery="forwardEvent" ref="childComponents">
            </component>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>
<script>
import BaseProperty from './BaseProperty'

export default {
  extends: BaseProperty,
  name: 'ConditionalPropertyGroup',
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
        this.$refs.childComponents.forEach(childComponent => childComponent.clear())
      }
      this.$emit('updateQuery',this.buildQueryParametersFromSelection())
    },
    clear() {
      this.selected = false
      this.selectionChanged()
      this.$refs.childComponents.forEach(childComponent => childComponent.clear())
    },
    forwardEvent(event) {
      this.$emit('updateQuery',event)
    },
    buildFilterfromURL(urlParameters) {
      let returnArray = new Array()
      this.selected = urlParameters.has(`${ this.namePath }-cond`) && urlParameters.get(`${ this.namePath }-cond`) === 'true'
      this.selected ? this.show() : this.hide()
      returnArray.push(this.buildQueryParametersFromSelection())

      if (!Array.isArray(this.$refs.childComponents)) return returnArray
      this.$refs.childComponents.forEach(childComponent => {
        if (childComponent.buildFilterfromURL) {
          returnArray.push(...childComponent.buildFilterfromURL(urlParameters))
        }
      })
      return returnArray
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
