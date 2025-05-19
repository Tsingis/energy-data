<template>
  <h1>Energy in Finland</h1>
  <Loading v-if="loading" size="6x" />
  <TimeSeriesChart
    v-if="!loading"
    :datasets="chartDatasets"
    y-axis-label-left="MW"
    y-axis-label-right="c/kWh"
    :min-timestamp="new Date(range[0])"
    :max-timestamp="new Date(range[1])"
    :current-date="date.getDate()"
  />
  <DateRangeSlider
    v-if="!loading"
    :model-value="[new Date(range[0]), new Date(range[1])]"
    :step="15 * 60 * 1000"
    :min="minTimestamp"
    :max="maxTimestamp"
    :format-value="(value) => formattedDateTime(value, true)"
    @update:model-value="onRangeUpdate"
  />
</template>

<script lang="ts">
  import { defineComponent, ref, onMounted, watch } from "vue"
  import TimeSeriesChart from "./components/TimeSeriesChart.vue"
  import DateRangeSlider from "./components/DateRangeSlider.vue"
  import Loading from "./components/Loading.vue"
  import { useFetchData } from "./composables/useFetchData"
  import { useDate } from "./composables/useDate"
  import {
    type PriceData,
    type PriceModel,
    type EnergyData,
    type EnergyModel,
    type Dataset,
    type ChartData,
  } from "./types"
  import { DATASET_COLORS, DATASET_LABELS } from "./constants"
  import { formattedDateTime } from "./composables/dateUtil"

  export default defineComponent({
    name: "App",
    components: {
      TimeSeriesChart,
      DateRangeSlider,
      Loading,
    },
    setup() {
      const chartDatasets = ref<ChartData | undefined>(undefined)
      const minTimestamp = ref<Date | undefined>(undefined)
      const maxTimestamp = ref<Date | undefined>(undefined)
      const range = ref<[number, number]>([0, 0])

      const fetchFunction = async () => {
        const apiUrl =
          import.meta.env.VITE_API_URL?.trim() || "http://localhost:8000"
        const energyResponse = await fetch(`${apiUrl}/api/energy`)
        if (!energyResponse.ok) throw new Error("Failed to fetch energy data")

        const priceResponse = await fetch(`${apiUrl}/api/price`)
        if (!priceResponse.ok) throw new Error("Failed to fetch price data")

        const energyData: EnergyData = await energyResponse.json()
        const priceData: PriceData = await priceResponse.json()

        return transformDataForChart(energyData, priceData)
      }

      const { data, loading, error, fetchData } = useFetchData(fetchFunction)
      const date = useDate()

      watch(data, (newData) => {
        if (newData) {
          chartDatasets.value = newData
          if (newData.minTimestamp && newData.maxTimestamp) {
            minTimestamp.value = newData.minTimestamp
            maxTimestamp.value = newData.maxTimestamp

            const now = date.getDate()
            const start = new Date(now)
            start.setHours(now.getHours() - 5)

            const end = new Date(now)
            end.setHours(now.getHours() + 5)

            range.value = [
              Math.max(start.getTime(), newData.minTimestamp.getTime()),
              Math.min(end.getTime(), newData.maxTimestamp.getTime()),
            ]
          }
        }
      })

      onMounted(fetchData)

      const transformDataForChart = (
        energyData: Record<string, EnergyModel[]>,
        priceData: PriceModel[]
      ): ChartData => {
        const labels: string[] = []
        const datasets: Dataset[] = []
        let order = 1

        let min: Date | null = null
        let max: Date | null = null

        for (const [dataset, datasetData] of Object.entries(energyData)) {
          const datasetValues = datasetData.map((entry) => {
            const timestamp = new Date(entry.timestamp)
            if (min === null || timestamp < min) min = timestamp
            if (max === null || timestamp > max) max = timestamp
            return {
              x: timestamp.getTime(),
              y: entry.value,
            }
          })

          datasets.push({
            type: "line",
            label: DATASET_LABELS[dataset] || `Dataset ${dataset}`,
            data: datasetValues,
            borderColor: DATASET_COLORS[dataset] || "#ccc",
            backgroundColor: DATASET_COLORS[dataset] || "#ccc",
            borderWidth: 2,
            fill: false,
            order: order,
          })

          order++
        }

        const priceDatasetValues = priceData.map((entry) => ({
          x: new Date(entry.timestamp).getTime(),
          y: entry.value,
        }))

        datasets.push({
          type: "bar",
          label: DATASET_LABELS["prices"],
          data: priceDatasetValues,
          borderColor: DATASET_COLORS["prices"] || "yellow",
          backgroundColor: DATASET_COLORS["prices"] || "yellow",
          yAxisID: "y2",
          order: order,
        })

        return {
          labels,
          datasets,
          minTimestamp: min ? new Date(min) : null,
          maxTimestamp: max ? new Date(max) : null,
        }
      }

      const onRangeUpdate = (value: [Date, Date]) => {
        range.value = [value[0].getTime(), value[1].getTime()]
      }

      return {
        chartDatasets,
        loading,
        error,
        minTimestamp,
        maxTimestamp,
        range,
        onRangeUpdate,
        formattedDateTime,
        date,
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
    height: 80vh;
  }
</style>
