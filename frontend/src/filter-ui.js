import Vue from 'vue'
import App from './components/FilterUI'
import PropertyGroup from './components/filter/PropertyGroup'
import MultipleChoiceProperty from './components/filter/MultipleChoiceProperty'
import OrderedSingleChoiceProperty from './components/filter/OrderedSingleChoiceProperty'
import BooleanProperty from './components/filter/BooleanProperty'
import TextProperty from './components/filter/TextProperty'
import { KebabCaseConverter } from './utils/KebabCaseConverter'

fetch('/matching/api/helper/info/filter-options/')
    .then( response => response.json() )
    .then( jsonData => Vue.prototype.$propertyConfiguration = jsonData)

registerComponents({
    PropertyGroup,
    MultipleChoiceProperty,
    OrderedSingleChoiceProperty,
    BooleanProperty,
    TextProperty
})

document.addEventListener('DOMContentLoaded', () => {
    new Vue({
        render: (h) => h(App),
    }).$mount('#app')
})


function registerComponents(components) {
    let componentName
    for (componentName in components) {
        let kebap_case_name = KebabCaseConverter.convertFromPascalCase(componentName)
        let component = components[componentName]
        Vue.component(kebap_case_name,component)
    }
}
