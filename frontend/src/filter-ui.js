import Vue from 'vue'
import App from './components/FilterUI.vue'
import MultipleChoiceProperty from './components/filter/MultipleChoiceProperty.vue'
Vue.config.productionTip = false
Vue.component('multiple-choice-property', MultipleChoiceProperty)
document.addEventListener('DOMContentLoaded', () => {
    new Vue({
        render: (h) => h(App),
    }).$mount('#app')
})
