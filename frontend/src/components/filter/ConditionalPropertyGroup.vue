<template>
  <div class="my-3 mx-2">
      <h2>{{ options.label }}</h2>
      {{ options.help_text }}

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
</template>
<script>
import BaseProperty from './BaseProperty'

export default {
  extends: BaseProperty,
  name: 'PropertyGroup',
  methods: {
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
  }
}
</script>
