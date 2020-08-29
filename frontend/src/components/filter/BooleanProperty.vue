<template>
  <accordion :label="options.label" badgeContent="" ref="accordion">
    <div>
      Template BooleanProperty
    </div>
  </accordion>
</template>
<script>
import BaseProperty from './BaseProperty'
import Accordion from '../Accordion'

export default {
  name: 'BooleanProperty',
  extends: BaseProperty,
  components: {
    Accordion
  }
}
</script>
