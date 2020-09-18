<template>
  <div>

    <div class="d-flex align-items-center justify-content-between flex-wrap">
      <div class="p-2">
        <h6 class="d-inline">Selected:</h6> <b-badge variant="primary">{{ selectedItems.length }}</b-badge>
      </div>
      <div class="p-2">
        <b-dropdown right class="m-2" html="<i class='fa fa-filter' aria-hidden='true'></i> Select Fields">
          <b-dropdown-form style="width:40rem">
            <b-form-checkbox-group class="mb-3 vertically-separate-children" switches :options="fieldSelector" v-model="selectedFields" stacked @change="fieldSelectionChanged">
            </b-form-checkbox-group>
            <b-form-group>
              <button type="button" class="btn btn-secondary btn-sm" @click="selectAllFields"><span class="fa fa-trash-o"></span> Zurücksetzen</button>
            </b-form-group>
          </b-dropdown-form>
        </b-dropdown>
      </div>
    </div>



    <b-table
      striped
      small
      responsive
      :items="items"
      :fields="filteredFields"
      ref="resultsTable"
      primary-key="uuid"
    >
      <template v-slot:cell()="data">
        <template v-if="data.value === true">
          <div class="text-center">
            <i class="fa fa-check-circle" aria-hidden="true"></i>
          </div>
        </template>
        <template v-else-if="data.value === false">
          <div class="text-center">
            <i class="fa fa-times-circle-o" aria-hidden="true"></i>
          </div>
        </template>

        <template v-else>
        {{ data.value }}
        </template>
      </template>
      <template v-slot:head(uuid)>
        <!-- Due to pagination select all will be rather confusing <b-form-checkbox></b-form-checkbox>-->
      </template>
      <template v-slot:cell(uuid)="data">
        <b-form-checkbox @change="toggleRowSelect(data)" :checked="selectedItems.includes(data.item.uuid)"></b-form-checkbox>
      </template>
    </b-table>

    <b-pagination
      :value="currentPage"
      :total-rows="totalRows"
      :per-page="itemsPerPage"
      class="mb-3"
      @change="pageChanged"
    ></b-pagination>

    <b-button :disabled="selectedItems.length === 0" primary @click="$refs.modal.show()">Contact {{ selectedItems.length }} selected</b-button>
    <send-message-modal :selectedUUIDs="selectedItems" ref="modal" @sent="sendSuccessful" @error="sendFailed" />
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
  'text': (path) => {
    return (sourceRow,targetRow) => {
      targetRow[path] = sourceRow[path]
      return targetRow
    }
  },
  'conditional': (path) => {
    return (sourceRow,targetRow) => {
      targetRow[path] = sourceRow[`${ path }-cond`]
      return targetRow
    }
  },
}
dataTransformators.boolean = dataTransformators.text // same logic

const selectedFieldsStorageKey = 'filter-ui-result-selected-fields'
import SendMessageModal from './FilterUISendMessageModal'
export default {
  name: 'FilterUIResults',
  components: {
    SendMessageModal
  },
  props: [ 'filterModel','fieldLabels','results','totalRows','currentPage','itemsPerPage'],
  data() {
    return {
      selectedFields: [],
      selectedItems: [],
    }
  },
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
      if (!sourceData) return []

      let transformers = [(sourceRow, targetObject) => {
        targetObject.uuid = sourceRow.uuid
        return targetObject
      }]

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
      transformedData.checkbox = false
      return transformedData
    },
    fields() {
      if (!this.flattenedFilterModel) return []
      let fieldsFromFilterModel = Array.from(this.flattenedFilterModel)
        .filter(keyPropertyTuple => dataTransformators.hasOwnProperty(keyPropertyTuple[1].type))
        .map(keyPropertyTuple => ({
          key: keyPropertyTuple[0],
          label: keyPropertyTuple[1].label,
        }))

      let headerFields = [
        {
          key: 'uuid',
          label: '',
        },
      ]

      return [...headerFields,...fieldsFromFilterModel]
    },
    fieldSelector() {
      return this.fields
        .filter(field => field.label && field.label.length > 0)
        .map(field => ({ text: field.label, value: field.key}))
    },
    filteredFields() {
      return this.fields.filter(field => this.selectedFields.includes(field.key))
    },
  },
  watch: {
    fields(newValue) {
      // Will be called after the available fields have been determined from the filter model (and the filterModel has actually been loaded)
      // Populates the field-selector control with the available fields
      let validFields = newValue.map(field => field.key)
      this.selectedFields = validFields // Create sensible default
      try {
        let fieldSelectionFromLocalStorage = JSON.parse(localStorage.getItem(selectedFieldsStorageKey))
        if (fieldSelectionFromLocalStorage && Array.isArray(fieldSelectionFromLocalStorage) && fieldSelectionFromLocalStorage.every(field => validFields.includes(field))) {
          // There is a field selection persisted to session storage, it is an Array and it only contains fields that are actually valid
          this.selectedFields = fieldSelectionFromLocalStorage
        }
      // eslint-disable-next-line no-empty
      } catch { /* we already set a sensible default beforehand. If JSON.parse fails, nothing to do */ }
    },
  },
  methods: {
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
    },
    pageChanged(page) {
      this.$emit('pageChanged',page)
    },
    selectAllFields() {
      this.selectedFields = this.fields.map(field => field.key)
    },
    clearSelection()  {
      this.selectedItems = []
    },
    toggleRowSelect(context) {
      let uuid = context.item.uuid
      if (this.selectedItems.includes(uuid)) {
        this.selectedItems = this.selectedItems.filter(item => item !== uuid)
      } else {
        this.selectedItems.push(uuid)
      }
    },
    toast(title, message,options) {
      this.$bvToast.toast(message, {
        title,
        toaster: 'b-toaster-top-center',
        solid: true,
        appendToast: true,
        ...options
      })
    },
    sendSuccessful(message) {
      this.toast('Messages sent',message,{ variant: 'success' })
    },
    sendFailed(message) {
      this.toast('Messages not sent',message,{ variant: 'danger', noAutoHide: true })
    },
    fieldSelectionChanged(checked) {
      localStorage.setItem(selectedFieldsStorageKey, JSON.stringify(checked))
    }
  },
  filters: {
    pretty: function(value) {
      return JSON.stringify(value, null, 2)
    },
  }
}
</script>
