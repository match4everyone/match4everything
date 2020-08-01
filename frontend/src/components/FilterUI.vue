<template>
  <div id="app">
    <p>
      <img alt="Vue logo" src="../assets/logo.png" width="100px" />
    </p>
    <p>Liebe Grüße an die Pythons und schönen Urlaub!</p>
    <form>
      <div class="form-group">
        <component
          v-for="property in mockOptions"
          :is="convertTypeToComponentName(property.type)"
          :key="property.name"
          :options="property">
        </component>
      </div>
    </form>
    </div>
</template>

<script>
import { mockOptions } from '../mockUpData/MockFilterOptions'
import { KebabCaseConverter } from '../utils/KebabCaseConverter'

export default {
  name: 'App',
  data() {
    return {
      mockOptions: mockOptions
    }
  },
  methods: {
    valueSelected(value) {
      console.log(value)
    },
    convertTypeToComponentName(typeName) {
      return KebabCaseConverter.convertFromPascalCase(typeName)
    }

  },
  mounted() {}
}
</script>

<style>
</style>
