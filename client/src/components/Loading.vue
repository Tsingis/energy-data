<template>
  <div class="loading-container" aria-label="loading">
    <font-awesome-icon :icon="faSpinner" :spin="true" :size="size" />
  </div>
</template>

<script lang="ts">
  import { defineComponent } from "vue"
  import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
  import { faSpinner } from "@fortawesome/free-solid-svg-icons"

  export default defineComponent({
    name: "Loading",
    components: {
      FontAwesomeIcon,
    },
    props: {
      size: {
        type: String,
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
