<template>
  <div class="form-group">
    {{ options.label }}
    <div v-for="option in options.choices" class="form-check" :key="option.value">
      <input
        class="form-check-input"
        type="checkbox"
        @change="valueSelected"
        :name="namePath"
        :id="`${ namePath }-${ option.value }`"
        :value="option.value" >
      <label
        class="form-check-label"
        :for="`${ namePath }-${ option.value }`"
        :key="`label-${ option.value }`">
        {{ option.caption }}
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
