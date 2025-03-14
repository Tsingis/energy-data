<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script lang="ts">
  import { defineComponent, onUnmounted, ref, watch, type PropType } from "vue"
  import {
    Chart,
    type ChartConfiguration,
    type ChartDataset,
    type LegendItem,
    type Point,
    type TooltipItem,
    registerables,
  } from "chart.js"
  import annotationPlugin from "chartjs-plugin-annotation"
  import "chartjs-adapter-date-fns"

  // Register all Chart.js components
  Chart.register(...registerables)
  Chart.register(annotationPlugin)

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
      yAxisLabelLeft: {
        type: String,
        required: false,
        default: "",
      },
      yAxisLabelRight: {
        type: String,
        required: false,
        default: "",
      },
      yAxisMinValueRight: {
        type: Number,
        required: false,
        default: 0,
      },
      minTimestamp: {
        type: Date as PropType<Date | null | undefined>,
        required: false,
        default: undefined,
      },
      maxTimestamp: {
        type: Date as PropType<Date | null | undefined>,
        required: false,
        default: undefined,
      },
    },
    setup(props) {
      const chartCanvas = ref<HTMLCanvasElement | null>(null)
      let chartInstance: Chart | null = null

      const tz = Intl.DateTimeFormat().resolvedOptions().timeZone

      const sortDatasetsAlphabetically = (
        datasets: ChartDataset<"line", (number | Point | null)[]>[]
      ) => {
        return datasets.sort((a, b) => {
          const aLabel = a.label || ""
          const bLabel = b.label || ""
          return aLabel.localeCompare(bLabel)
        })
      }

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
          const sortedDatasets = sortDatasetsAlphabetically(
            props.datasets.datasets
          )

          const chartConfig: ChartConfiguration<"line"> = {
            type: "line",
            data: {
              labels: props.datasets.labels,
              datasets: sortedDatasets,
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  display: true,
                  position: "top",
                  labels: {
                    boxWidth: 20,
                    usePointStyle: true,
                    generateLabels: (chart) => {
                      return chart.data.datasets.map((dataset, i) => ({
                        text: dataset.label ?? `Dataset ${i}`,
                        fillStyle: dataset.borderColor,
                        strokeStyle: dataset.borderColor,
                        lineWidth: 3,
                        datasetIndex: i,
                      })) as LegendItem[]
                    },
                  },
                },
                tooltip: {
                  enabled: true,
                  mode: "nearest",
                  intersect: false,
                  usePointStyle: true,
                  callbacks: {
                    label: (tooltipItem: TooltipItem<"line">) => {
                      const { y } = tooltipItem.raw as { y: number }
                      return `Value: ${y}`
                    },
                  },
                },
                annotation: {
                  annotations: {
                    currentTimeLine: {
                      type: "line",
                      xMin: new Date().getTime(),
                      xMax: new Date().getTime(),
                      borderColor: "rgba(169, 169, 169, 0.5)",
                      borderWidth: 2,
                      borderDash: [5, 5],
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
                    callback: (value, index) => {
                      if (index % 4 === 0) {
                        const date = new Date(value as number)
                        const minutes = date.getMinutes()
                        const roundedMinutes = Math.floor(minutes / 15) * 15
                        date.setMinutes(roundedMinutes, 0, 0)
                        return date.toLocaleTimeString(undefined, {
                          timeZone: tz,
                          hour: "2-digit",
                          minute: "2-digit",
                          hour12: false,
                        })
                      }
                      return ""
                    },
                  },
                  min: props.minTimestamp
                    ? new Date(props.minTimestamp).toLocaleString(undefined, {
                        timeZone: tz,
                      })
                    : undefined,
                  max: props.maxTimestamp
                    ? new Date(props.maxTimestamp).toLocaleString(undefined, {
                        timeZone: tz,
                      })
                    : undefined,
                },
                y: {
                  title: {
                    display: true,
                    text: props.yAxisLabelLeft,
                  },
                  ticks: {
                    maxTicksLimit: 5,
                    callback: (value) => {
                      return value
                    },
                  },
                },
                y2: {
                  position: "right",
                  title: {
                    display: true,
                    text: props.yAxisLabelRight,
                  },
                  ticks: {
                    maxTicksLimit: 5,
                    callback: (value) => {
                      return value
                    },
                  },
                  min: props.yAxisMinValueRight,
                  grid: {
                    offset: true,
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
