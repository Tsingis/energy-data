<template>
  <div class="loading-container" aria-label="loading">
    <font-awesome-icon :icon="faSpinner" :spin="true" :size="size" />
  </div>
</template>

<script lang="ts">
  import { defineComponent, type PropType } from "vue"
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
  import { faSpinner } from "@fortawesome/free-solid-svg-icons"

  export default defineComponent({
    name: "Loading",
    components: {
      FontAwesomeIcon,
    },
    props: {
      size: {
        type: String as PropType<
          | "2xs"
          | "xs"
          | "sm"
          | "lg"
          | "xl"
          | "2xl"
          | "1x"
          | "2x"
          | "3x"
          | "4x"
          | "5x"
          | "6x"
          | "7x"
          | "8x"
          | "9x"
          | "10x"
        >,
        default: "1x",
      },
    },
    setup() {
      return {
        faSpinner,
      }
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
</style>
