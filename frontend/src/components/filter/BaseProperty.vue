<script>

import { FilterComponentManager } from '../../utils/FilterComponentManager'

export default {
  props: [ 'options', 'parentName' ],
  computed: {
    namePath() {
      // Concatenate the current component path for creating filters
      // the resulting name is all previous components concatenated with --
      return [this.parentName, this.options.name].filter( part => part !== undefined ).join('--')
    }
  },
  methods: {
    /**
     * Converts the typeName to kebab case, e.g. MyCustomComponent -> my-custom-component
     * for converting a Python Class to the corresponding Vue.js component
     */
    convertTypeToComponentName(typeName) {
      return FilterComponentManager.getComponentForType(typeName)
    },
    buildFilterfromURL() {
      // needs to be implemented in Sub-Components
      return []
    },
  }
}
</script>
