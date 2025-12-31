<template>
  <div class="loading-container" data-testid="loading" aria-label="loading">
    <PhCube class="spin" />
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue"
  import { PhCube } from "@phosphor-icons/vue"

  export default defineComponent({
    name: "Loading",
    components: { PhCube },
  })
</script>

<style scoped>
  .loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 7.5em;
  }

  svg {
    width: 40vw;
    height: 40vh;
  }

  .spin {
    display: inline-block;
    transform-origin: center;
    animation: spin 3s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
</style>
