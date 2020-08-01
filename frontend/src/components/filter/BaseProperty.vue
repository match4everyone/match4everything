<script>

import { KebabCaseConverter } from '../../utils/KebabCaseConverter'

export default {
  props: [ 'options', 'parent_name' ],
  computed: {
    namePath() {
      // Concatenate the current component path for creating filters
      // the resulting name is all previous components concatenated with --
      return [this.parent_name, this.options.name].filter( part => part !== undefined ).join('--')
    }
  },
  methods: {
    /**
     * Converts the typeName to kebab case, e.g. MyCustomComponent -> my-custom-component
     * for converting a Python Class to the corresponding Vue.js component
     */
    convertTypeToComponentName(typeName) {
      return KebabCaseConverter.convertFromPascalCase(typeName)
    }
  }
}
</script>
