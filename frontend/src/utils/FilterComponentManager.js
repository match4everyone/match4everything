
import PropertyGroup from '../components/filter/PropertyGroup'
import MultipleChoiceProperty from '../components/filter/MultipleChoiceProperty'
import OrderedSingleChoiceProperty from '../components/filter/OrderedSingleChoiceProperty'
import BooleanProperty from '../components/filter/BooleanProperty'
import TextProperty from '../components/filter/TextProperty'


class FilterComponentManager {

    constructor() {
        this.componentMap = {
            'group': PropertyGroup,
            'conditional': null,
            'multiple-choice': MultipleChoiceProperty,
            'single-choice': null,
            'ordered-single-choice': OrderedSingleChoiceProperty,
            'text': TextProperty,
            'boolean': BooleanProperty,
        }
    }

    getComponentForType(djangoPropertyType) {
        return this.componentMap[djangoPropertyType]
    }

    registerComponents(Vue) {
        for ( let djangoTypeName in this.componentMap) {
            let component = this.getComponentForType(djangoTypeName)
            if (component) Vue.component(`${ djangoTypeName }-filter-selector`,component)
        }
    }
}

const instance = new FilterComponentManager()
Object.freeze(instance)
export { instance as FilterComponentManager }
