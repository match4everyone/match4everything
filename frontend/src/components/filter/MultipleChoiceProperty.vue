<template>
  <div>
    <div v-for="(value, key) in options.choices" class="form-check" :key="key">
      <input
        class="form-check-input"
        type="checkbox"
        :name="namePath"
        :id="`${ namePath }-${ key }`"
        :value="key"
        v-model="selected"
        @change="selectionChanged">
      <label
        class="form-check-label"
        :for="`${ namePath }-${ key }`"
        :key="`label-${ value }`">
        {{ value }}
      </label>
    </div>
  </div>
</template>

<script>
import BaseProperty from './BaseProperty'

export default {
  extends: BaseProperty,
  name : 'MultipleChoiceProperty',
  data: function () {
    return {
      selected: []
    }
  },
  methods: {
    selectionChanged: function () {

      let queryParameters = this.selected.map(key => [`${ this.namePath }-${ key }`, true])
      this.$emit('updateQuery',{
        path: this.namePath,
        queryString: queryParameters
      })
    }
  }

}
</script>
