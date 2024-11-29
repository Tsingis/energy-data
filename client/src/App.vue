<template>
  <h1>Hello world</h1>
  <LineChart />
</template>

<script lang="ts">
import { defineComponent } from "vue"
import LineChart from "./components/LineChart.vue"

export default defineComponent({
  name: "App",
  components: {
    LineChart,
  },
})
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 600px;
  font-family: Arial, sans-serif;
}
</style>
