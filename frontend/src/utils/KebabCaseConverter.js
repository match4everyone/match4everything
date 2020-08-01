class KebabCaseConverter {

    convertFromPascalCase(pascalCaseString) {
        return this.convertFromCamelCase(pascalCaseString)
    }

    convertFromCamelCase(camelCaseString) {
        return camelCaseString.split(/(?=[A-Z])/).map(part => part.toLowerCase()).join('-')
    }

}

// ES6 Singleton Pattern
const instance = new KebabCaseConverter()
Object.freeze(instance)
export  { instance as KebabCaseConverter }
