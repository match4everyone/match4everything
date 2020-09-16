<template>
  <div>

    <pre style="overflow-y:auto; overflow-x:auto; max-height:200px;">
      {{ items | pretty }}
    </pre>

    <b-table
      striped
      small
      responsive
      :items="items"
      :fields="tableFields"
      primary-key="uuid"
    >
      <!-- A custom formatted column -->
      <template v-slot:cell(uuid)="data">
        <b class="text-info">{{ data }}</b>, <b>{{ data }}</b>
      </template>
    </b-table>


    Page: {{ currentPage }} / {{ pages }}
    <button @click="previous">Previous</button>
    <button @click="next">Next</button>


  </div>
</template>
<script>
/* eslint-disable no-prototype-builtins */
export default {
  name: 'FilterUIResults',
  props: [ 'filterModel','fieldLabels','items','pages','currentPage'],
  computed: {
    flattenedFilterModel() {
      let map = new Map()
      this.flattenFilterModelTree(this.filterModel).forEach(
        pathNodeTuple => map.set(pathNodeTuple.path,pathNodeTuple.node)
      )
      return map
    },
    tableFields() {
      const items = this.items
      if (items === null || (Array.isArray(items) && items.length === 0)) return []

      return this.fieldLabels.filter(field => this.flattenedFilterModel.has(field.key))
    },
  },
  methods: {
    next() {
      this.$emit('next')
    },
    previous() {
      this.$emit('previous')
    },
    flattenFilterModelTree(node,currentPath = []) {
      let pathList = []
      if (currentPath.length !== 0) { // do not add root node
        pathList.push({ path: currentPath.join('--'), node: node })
      }

      if (node.hasOwnProperty('properties')) {
        for (let child of node.properties) {
          pathList.push(...this.flattenFilterModelTree(child,[...currentPath, child.name]))
        }
      }
      return pathList
    }
  },
  filters: {
    pretty: function(value) {
      return JSON.stringify(value, null, 2)
    },
  }
}
</script>
