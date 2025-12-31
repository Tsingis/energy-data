<template>
  <div class="loading-container" data-testid="loading" aria-label="loading">
    <PhCube :size="size" class="spin" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, type PropType } from "vue"
  import { PhCube } from "@phosphor-icons/vue"

  export default defineComponent({
    name: "Loading",
    components: { PhCube },
    props: {
      size: {
        type: [String, Number] as PropType<string | number>,
        default: 100,
      },
    },
  })
</script>

<style scoped>
  .loading-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50vh;
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
