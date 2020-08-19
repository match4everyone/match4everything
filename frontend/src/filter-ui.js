import Vue from 'vue'
import FilterUIComponentDefinition from './components/FilterUI'
import { FilterComponentManager } from './utils/FilterComponentManager'

/*
Fugly, but need to get the global object, if imported the way it should be
all the added functions from bootstrap would be missing, and as we want to use
them, there is no choice
*/
const globalBootstrapJQuery = window.$
Vue.prototype.$jQuery = globalBootstrapJQuery

FilterComponentManager.registerComponents(Vue)

document.addEventListener('DOMContentLoaded', () => {
    const FilterUI = Vue.extend(FilterUIComponentDefinition)
    new FilterUI({ el: '#app'})
})
