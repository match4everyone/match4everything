import Vue from 'vue'
import FilterUIComponentDefinition from './components/FilterUI'
import { FilterComponentManager } from './utils/FilterComponentManager'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import django from 'django'

/*
Fugly, but need to get the global object, if imported the way it should be
all the added functions from bootstrap would be missing, and as we want to use
them, there is no choice
*/
const globalBootstrapJQuery = window.$
Vue.prototype.$jQuery = globalBootstrapJQuery

/*
A little bit of the same for django translations. This (re)uses the django approach.
There are a lot better solutions for javascript by itself but this way we can keep
all the translations in the same place as the django ones.

Docs: https://docs.djangoproject.com/en/3.1/topics/i18n/translation/#internationalization-in-javascript-code
(Requires a separate webpack configuration to create a special build with unmodified function names and w/o source-maps)
*/
Vue.prototype.$gettext  = django.gettext
Vue.prototype.$ngettext = django.ngettext
Vue.prototype.$interpolate = django.interpolate

/* Provide a mechanism to get csrf token in all components easily */
import Cookies from 'js-cookie'
Vue.prototype.$getToken = () => Cookies.get('csrftoken')

/* Register FilterUI Components */
FilterComponentManager.registerComponents(Vue)

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

document.addEventListener('DOMContentLoaded', () => {
    const FilterUI = Vue.extend(FilterUIComponentDefinition)
    new FilterUI({ el: '#app'})
})
