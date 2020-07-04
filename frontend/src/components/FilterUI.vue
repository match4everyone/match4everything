<template>
  <div id="app">
    <p>
      <img alt="Vue logo" src="../assets/logo.png">
    </p>
    <p>
      Liebe Grüße an die Pythons und schönen Urlaub!
    </p>
    <form>
      <div class="form-group">
      <multiple-choice-property
        :options="mockOptions"
        caption="Please choose a Prefered area of help:"
        id="sampleFieldPoCNr1MyDearestPropertyofThemAll"
        @input="valueSelected"
      ></multiple-choice-property>
      </div>
    </form>
  </div>
</template>

<script>

import mockOptions from '../mockUpData/MultipleChoicePropertyOptions'

export default {
  name: 'App',
  data: function () {
    return {
      mockOptions : mockOptions,
    }
  },
  methods: {
    valueSelected: function (value) {
      console.log(value)
    }
  },
  mounted: function () {
    console.log(mockOptions)
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
