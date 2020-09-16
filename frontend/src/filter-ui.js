import Vue from 'vue'
import FilterUIComponentDefinition from './components/FilterUI'
import { FilterComponentManager } from './utils/FilterComponentManager'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

/*
Fugly, but need to get the global object, if imported the way it should be
all the added functions from bootstrap would be missing, and as we want to use
them, there is no choice
*/
const globalBootstrapJQuery = window.$
Vue.prototype.$jQuery = globalBootstrapJQuery
FilterComponentManager.registerComponents(Vue)

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

document.addEventListener('DOMContentLoaded', () => {
    const FilterUI = Vue.extend(FilterUIComponentDefinition)
    new FilterUI({ el: '#app'})
})
