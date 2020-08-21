<template>
  <div>
    <h1>Filter</h1>
    <component
      v-for="property in filterModel.properties"
      :is="convertTypeToComponentName(property.type)"
      :key="property.name"
      :options="property"
      @updateQuery="forwardEvent">
    </component>
  </div>
</template>

<script>
import { FilterComponentManager } from '../../utils/FilterComponentManager'

export default {
  props: [ 'filterModel' ],
  methods: {
    convertTypeToComponentName(typeName) {
      return FilterComponentManager.getComponentForType(typeName)
    },
    forwardEvent(event) {
      this.$emit('updateQuery',event)
    },
  },
}
</script>
