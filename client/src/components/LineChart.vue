<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onUnmounted, ref } from "vue"
import { Chart, type ChartConfiguration, registerables } from "chart.js"

// Register all Chart.js components
Chart.register(...registerables)

export default defineComponent({
  name: "LineChart",
  setup() {
    const chartCanvas = ref<HTMLCanvasElement | null>(null)
    let chartInstance: Chart | null = null

    // Chart.js configuration
    const chartConfig: ChartConfiguration<"line"> = {
      type: "line",
      data: {
        labels: ["January", "February", "March", "April", "May", "June"],
        datasets: [
          {
            label: "Sample Data",
            data: [10, 20, 15, 30, 25, 40],
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: true, position: "top" },
        },
      },
    }

    onMounted(() => {
      if (chartCanvas.value) {
        chartInstance = new Chart(chartCanvas.value, chartConfig)
      }
    })

    onUnmounted(() => {
      if (chartInstance) {
        chartInstance.destroy()
      }
    })

    return { chartCanvas }
  },
})
</script>

<style scoped>
.chart-container {
  max-width: 600px;
  height: 400px;
  margin: auto;
}

canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
