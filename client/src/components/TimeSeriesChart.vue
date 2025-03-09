<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script lang="ts">
  import { defineComponent, onUnmounted, ref, watch } from "vue"
  import {
    Chart,
    ChartConfiguration,
    ChartDataset,
    Point,
    registerables,
  } from "chart.js"
  import { toZonedTime } from "date-fns-tz"
  import "chartjs-adapter-date-fns"

  // Register all Chart.js components
  Chart.register(...registerables)

  export default defineComponent({
    name: "TimeSeriesChart",
    props: {
      datasets: {
        type: Object as () => {
          labels: string[]
          datasets: ChartDataset<"line", (number | Point | null)[]>[]
        },
        required: true,
        default: () => ({
          labels: [],
          datasets: [],
        }),
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

      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone

      const updateChart = () => {
        if (
          !props.datasets ||
          !props.datasets.labels ||
          !props.datasets.datasets
        ) {
          return
        }

        if (chartInstance) {
          chartInstance.destroy()
        }

        if (chartCanvas.value) {
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
                      const value = tooltipItem.raw as number
                      return `Value: ${value}`
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
                        timeZone: tz,
                        hour: "2-digit",
                        minute: "2-digit",
                        hour12: false,
                      })
                    },
                  },
                  min: props.minTimestamp
                    ? toZonedTime(props.minTimestamp, tz).getTime()
                    : undefined,
                  max: props.maxTimestamp
                    ? toZonedTime(props.maxTimestamp, tz).getTime()
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

          chartInstance = new Chart(chartCanvas.value, chartConfig)
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

      watch(
        () => [props.minTimestamp, props.maxTimestamp],
        ([newMin, newMax]) => {
          if (newMin && newMax) {
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
    max-width: 90vw;
    max-height: 100vh;
    margin: auto;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  @media (max-width: 800px) {
    .chart-container {
      min-height: 50vh;
    }
  }

  canvas {
    width: 100% !important;
    height: 100% !important;
  }
</style>
