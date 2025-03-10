<template>
  <h1>Energy Data in Finland</h1>
  <TimeSeriesChart
    :datasets="chartDatasets"
    y-axis-label-left="MW"
    y-axis-label-right="c/kWh"
    :min-timestamp="chartDatasets?.minTimestamp"
    :max-timestamp="chartDatasets?.maxTimestamp"
  />
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted } from "vue"
  import { type ChartDataset } from "chart.js"
  import TimeSeriesChart from "./components/TimeSeriesChart.vue"
  import {
    type PriceData,
    type PriceModel,
    type EnergyData,
    type EnergyModel,
  } from "./types"
  import { DATASET_COLORS, DATASET_LABELS } from "./constants"

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
          const energyResponse = await fetch(`${apiUrl}/energy`)
          if (!energyResponse.ok) {
            throw new Error("Network response was not ok")
          }

          const priceResponse = await fetch(`${apiUrl}/price`)

          const energyData: EnergyData = await energyResponse.json()
          const priceData: PriceData = await priceResponse.json()

          const formattedData = transformDataForChart(
            energyData.data,
            priceData.data
          )
          chartDatasets.value = formattedData
        } catch (error) {
          console.error(error)
        }
      })

      const transformDataForChart = (
        energyData: Record<string, EnergyModel[]>,
        priceData: PriceModel[]
      ) => {
        const labels: Date[] = []
        const datasets: ChartDataset[] = []

        let min: Date | null = null
        let max: Date | null = null

        for (const [datasetId, datasetData] of Object.entries(energyData)) {
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
            backgroundColor: DATASET_COLORS[datasetId] || "#ccc",
            borderWidth: 2,
            fill: false,
          })
        }

        const priceDatasetValues = priceData.map((entry) => ({
          x: new Date(entry.timestamp).getTime(),
          y: entry.value,
        }))

        datasets.push({
          label: DATASET_LABELS["prices"],
          data: priceDatasetValues,
          borderColor: DATASET_COLORS["prices"] || "yellow",
          backgroundColor: DATASET_COLORS["prices"] || "yellow",
          borderWidth: 2,
          fill: false,
          borderDash: [5, 5],
          yAxisID: "y2",
        })

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
