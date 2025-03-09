<template>
  <h1>Energy Data in Finland</h1>
  <TimeSeriesChart
    :datasets="chartDatasets"
    yAxisLabel="MW"
    :minTimestamp="chartDatasets?.minTimestamp"
    :maxTimestamp="chartDatasets?.maxTimestamp"
  />
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted } from "vue"
  import TimeSeriesChart from "./components/TimeSeriesChart.vue"
  import { EnergyData, EnergyModel } from "./types"
  import { COLORS, DATASET_LABELS } from "./contants"

  export default defineComponent({
    name: "App",
    components: {
      TimeSeriesChart,
    },
    setup() {
      const chartDatasets = ref<any>(null)

      onMounted(async () => {
        try {
          const response = await fetch("http://localhost:8000/data")
          if (!response.ok) {
            throw new Error("Network response was not ok")
          }

          const data: EnergyData = await response.json()
          const formattedData = transformDataForChart(data.data)
          chartDatasets.value = formattedData
        } catch (error) {}
      })

      //TODO: Why all charts are "capped" at specific timestamp
      const transformDataForChart = (data: Record<string, EnergyModel[]>) => {
        const labels: string[] = []
        const datasets: any[] = []

        let min: Date | null = null
        let max: Date | null = null

        for (const [datasetId, datasetData] of Object.entries(data)) {
          const datasetLabels = datasetData.map((entry) => entry.timestamp)
          const values = datasetData.map((entry) => entry.value)

          if (labels.length === 0 && datasetLabels.length > 0) {
            labels.push(...datasetLabels)
          }

          datasetLabels.forEach((timestamp) => {
            const timestampValue = new Date(timestamp)
            if (min === null || timestampValue < min) {
              min = timestampValue
            }
            if (max === null || timestampValue > max) {
              max = timestampValue
            }
          })

          datasets.push({
            label: DATASET_LABELS[datasetId] || `Dataset ${datasetId}`,
            data: values,
            borderColor: COLORS[datasetId] || "#ccc",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderWidth: 2,
            fill: false,
          })
        }

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
