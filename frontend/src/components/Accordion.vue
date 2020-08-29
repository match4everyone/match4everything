<template>
  <div class="vue-accordion">
    <div class="p-2" @click="toggle">
      {{ label }}
      <span v-if="badgeContent === 0 || badgeContent" class="badge badge-primary">{{ badgeContent}}</span>
      <span class="fa fa-caret-down" style="float:right"></span>
    </div>
    <div class="collapse" ref="collapsible">
      <div class="p-2">
        <slot></slot>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: {
    label: String,
    badgeContent: { },
  },
  methods: {
    toggle() {
      this.$jQuery(this.$refs.collapsible).collapse('toggle')
    },
    show() {
      this.$jQuery(this.$refs.collapsible).collapse('show')
    },
    hide() {
      this.$jQuery(this.$refs.collapsible).collapse('hide')
    },
  }
}
</script>
