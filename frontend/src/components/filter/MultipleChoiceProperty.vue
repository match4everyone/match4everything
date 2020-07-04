<template>
<div>
    <label :for="id">{{ caption }}</label>
    <select :id="id" v-model="selected" @change="valueSelected" class="form-control">
        <option v-for="option in options" :key="option.value" :value="option.value">{{ option.caption }}</option>
    </select>
</div>
</template>

<script>
export default {
    name : 'MultipleChoiceProperty',
    props: [
        'id',
        'caption',
        'options',
    ],
    data: function () {
        return {
            selected: null
        }
    },
    methods: {
        valueSelected: function () {
            this.$emit('input',{
                id: this.id,
                selected: this.selected
            })
        }
    }

}
</script>
