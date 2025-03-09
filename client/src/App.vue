<template>
  <h1>Energy Data in Finland</h1>
  <TimeSeriesChart
    :datasets="chartDatasets"
    y-axis-label="MW"
    :min-timestamp="chartDatasets?.minTimestamp"
    :max-timestamp="chartDatasets?.maxTimestamp"
  />
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted } from "vue"
  import { type ChartDataset } from "chart.js"
  import TimeSeriesChart from "./components/TimeSeriesChart.vue"
  import { type EnergyData, type EnergyModel } from "./types"
  import { DATASET_COLORS, DATASET_LABELS } from "./contants"

  export default defineComponent({
    name: "App",
    components: {
      TimeSeriesChart,
    },
    setup() {
      const chartDatasets = ref<any>(null)

      onMounted(async () => {
        try {
          const apiUrl =
            import.meta.env.VITE_API_URL?.trim() || "http://localhost:8000/data"
          const response = await fetch(`${apiUrl}/energy`)
          if (!response.ok) {
            throw new Error("Network response was not ok")
          }

          const data: EnergyData = await response.json()
          const formattedData = transformDataForChart(data.data)
          chartDatasets.value = formattedData
        } catch (error) {
          console.error(error)
        }
      })

      const transformDataForChart = (data: Record<string, EnergyModel[]>) => {
        const labels: Date[] = []
        const datasets: ChartDataset[] = []

        let min: Date | null = null
        let max: Date | null = null

        for (const [datasetId, datasetData] of Object.entries(data)) {
          const datasetLabels = datasetData.map(
            (entry) => new Date(entry.timestamp)
          )
          const values = datasetData.map((entry) => entry.value)

          datasetLabels.forEach((timestamp) => {
            if (
              !labels.some((label) => label.getTime() === timestamp.getTime())
            ) {
              labels.push(timestamp)
            }

            const timestampValue = timestamp
            if (min === null || timestampValue < min) {
              min = timestampValue
            }
            if (max === null || timestampValue > max) {
              max = timestampValue
            }
          })

          const datasetValues = datasetLabels.map((timestamp, index) => ({
            x: timestamp.getTime(),
            y: values[index],
          }))

          datasets.push({
            label: DATASET_LABELS[datasetId] || `Dataset ${datasetId}`,
            data: datasetValues,
            borderColor: DATASET_COLORS[datasetId] || "#ccc",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderWidth: 2,
            fill: false,
          })
        }

        labels.sort((a, b) => a.getTime() - b.getTime())

        return {
          labels,
          datasets,
          minTimestamp: min ? new Date(min) : null,
          maxTimestamp: max ? new Date(max) : null,
        }
      }

      return {
        chartDatasets,
      }
    },
  })
</script>

<style>
  #app {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
  }
</style>
