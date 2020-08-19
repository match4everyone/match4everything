<template>
  <div>
    <div v-for="(value, key) in options.choices" class="form-check" :key="key">
      <input
        class="form-check-input"
        type="checkbox"
        @change="valueSelected"
        :name="namePath"
        :id="`${ namePath }-${ key }`"
        :value="value" >
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
      selected: null
    }
  },
  methods: {
    valueSelected: function (event) {
      this.$emit('input',{
        id: this.id,
        selected: event.target.value
      })
    }
  }

}
</script>
