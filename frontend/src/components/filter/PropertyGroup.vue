<template>
  <div>
      Template PropertyGroup<br>
      Child Components:<br>
      <ul>
        <li v-for="child_property in options.properties" :key="child_property.name">{{ child_property.name }}:
          <component :is="convertTypeToComponentName(child_property.type)" :options="child_property" :parent_name="namePath">
          </component>
        </li>
      </ul>
  </div>
</template>
<script>
import BaseProperty from './BaseProperty'

export default {
  extends: BaseProperty
}
</script>
