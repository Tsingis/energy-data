<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script lang="ts">
  import { defineComponent, onUnmounted, ref, watch } from "vue"
  import { Chart, ChartConfiguration, registerables } from "chart.js"
  import "chartjs-adapter-date-fns"

  // Register all Chart.js components
  Chart.register(...registerables)

  export default defineComponent({
    name: "TimeSeriesChart",
    props: {
      datasets: {
        type: Object as () => { labels: string[]; datasets: any[] },
        required: true,
      },
      yAxisLabel: {
        type: String,
        required: false,
      },
      minTimestamp: {
        type: Date,
        required: false,
        default: undefined,
      },
      maxTimestamp: {
        type: Date,
        required: false,
        default: undefined,
      },
    },
    setup(props) {
      const chartCanvas = ref<HTMLCanvasElement | null>(null)
      let chartInstance: Chart | null = null

      const updateChart = () => {
        if (
          props.datasets &&
          props.datasets.labels &&
          props.datasets.datasets
        ) {
          const chartConfig: ChartConfiguration<"line"> = {
            type: "line",
            data: {
              labels: props.datasets.labels,
              datasets: props.datasets.datasets,
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: { display: true, position: "top" },
                tooltip: {
                  enabled: true,
                  mode: "nearest",
                  intersect: false,
                  callbacks: {
                    label: (tooltipItem) => {
                      return `Value: ${tooltipItem.raw}`
                    },
                  },
                },
              },
              scales: {
                x: {
                  type: "time",
                  time: {
                    unit: "minute",
                    tooltipFormat: "HH:mm",
                  },
                  ticks: {
                    autoSkip: false,
                    stepSize: 15,
                    callback: (value) => {
                      const date = new Date(value as number)
                      return date.toLocaleTimeString(undefined, {
                        timeZone:
                          Intl.DateTimeFormat().resolvedOptions().timeZone,
                        hour: "2-digit",
                        minute: "2-digit",
                        hour12: false,
                      })
                    },
                  },
                  min: props.minTimestamp
                    ? props.minTimestamp.getTime()
                    : undefined,
                  max: props.maxTimestamp
                    ? props.maxTimestamp.getTime()
                    : undefined,
                },
                y: {
                  title: {
                    display: true,
                    text: props.yAxisLabel,
                  },
                  ticks: {
                    callback: function (value) {
                      return value
                    },
                  },
                },
              },
            },
          }

          if (chartCanvas.value) {
            chartInstance = new Chart(chartCanvas.value, chartConfig)
          }
        }
      }

      watch(
        () => props.datasets,
        (newValue) => {
          if (newValue) {
            updateChart()
          }
        },
        { immediate: true }
      )

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
    width: 100%;
    height: 100%;
    max-width: 100vw;
    max-height: 100vh;
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style>
