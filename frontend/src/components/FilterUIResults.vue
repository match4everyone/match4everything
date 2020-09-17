<template>
  <div>
    <h2>Before transformation</h2>
    <pre style="overflow-y:auto; overflow-x:auto; max-height:200px;">
      {{ results | pretty }}
    </pre>

    <h2>After transformation</h2>
    <pre style="overflow-y:auto; overflow-x:auto; max-height:200px;">
      {{ items | pretty }}
    </pre>

    <b-table
      striped
      small
      responsive
      :items="items"
      :fields="fields"
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

/**
 * Dictionary for data transformators creator functions. Each property is a function that can be called
 * with a property from the filter model and its complete path
 *
 * @returns a dataTransformation function accepting sourceRow and targetRow parameters, which will
 * map the source data to the correct target data format, e.g. by reducing multiple true/false columns
 * for a multiple choice property to a string containing the labels for the selected entries
 * A: true, B: false, C: true => "Label For A, Label For C"
 *
 * The function shall fulfill the following contract
 * param sourceRow a reference to the source row object
 * param targetRow a reference to the target row object, will set the value under the key of the properties path
 * returns the target row reference
 */
const dataTransformators = {
  'multiple-choice': (path,property) => {
    return (sourceRow,targetRow) => {
      targetRow[path] = Object
        .keys(property.choices)
        .filter(choice => sourceRow.hasOwnProperty(`${ path }-${ choice }`) && sourceRow[`${ path }-${ choice }`] === true)
        .map(choiceKey => property.choices[choiceKey])
        .sort()
        .join(', ')
      return targetRow
    }
  },
  'ordered-single-choice': (path,property) => {
    return (sourceRow,targetRow) => {
      targetRow[path] = property.choices[sourceRow[path]]
      return targetRow
    }
  },
  'boolean': (path) => {
    return (sourceRow,targetRow) => {
      targetRow[path] = sourceRow[path]
      return targetRow
    }
  },
  'text': (path,property) => [{
    key: `${ path }`,
    label: property.label
  }],
}
dataTransformators.conditional = dataTransformators.text = dataTransformators.boolean // same logic for all three

export default {
  name: 'FilterUIResults',
  props: [ 'filterModel','fieldLabels','results','pages','currentPage'],
  computed: {
    flattenedFilterModel() {
      let map = new Map()
      this.flattenFilterModelTree(this.filterModel).forEach(
        pathNodeTuple => map.set(pathNodeTuple.path,pathNodeTuple.node)
      )
      return map
    },
    items() {
      let sourceData = this.results
      if (sourceData === null) return []

      let transformers = []
      this.flattenedFilterModel.forEach((property,path) => {
        if (dataTransformators.hasOwnProperty(property.type)) {
          let newTransformers = dataTransformators[property.type](path,property)
          transformers.push(newTransformers)
        }
      })
      let transformedData = sourceData.map(
        sourceRow => transformers.reduce(
          (targetObject, transformer) => transformer(sourceRow, targetObject),
          {}
        )
      )

      return transformedData
    },
    fields() {
      if (this.items.length === 0 ) return []
      let firstItem = this.items[0]
      return Array.from(this.flattenedFilterModel)
        .filter(keyPropertyTuple => firstItem.hasOwnProperty(keyPropertyTuple[0]))
        .map(keyPropertyTuple => ({
          key: keyPropertyTuple[0],
          label: keyPropertyTuple[1].label,
        }))
    }
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
