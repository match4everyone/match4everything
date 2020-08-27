<template>
  <div>
    <h1>Filter</h1>
    <component
      v-for="property in filterModel.properties"
      ref="childComponents"
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
    buildFilterfromURL(urlParameters) {
      if (!Array.isArray(this.$refs.childComponents)) return []

      let returnArray = new Array()
      this.$refs.childComponents.forEach(childComponent => {
        if (childComponent.buildFilterfromURL) {
          returnArray.push(...childComponent.buildFilterfromURL(urlParameters))
        }
      })
      return returnArray
    },
  },
  mounted() {
    console.log('Filter mounted')
  },
  created() {
    console.log('Filter created')
  }
}
</script>
