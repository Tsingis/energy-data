import { render } from "@testing-library/vue"
import { describe, it, expect } from "vitest"
import TimeSeriesChart from "../../src/components/TimeSeriesChart.vue"

describe("TimeSeriesChart.vue", () => {
  it("renders correctly with empty values", () => {
    const { getByTestId } = render(TimeSeriesChart, {
      props: {
        datasets: {
          labels: [],
          datasets: [],
        },
        minTimestamp: new Date(),
        maxTimestamp: new Date(),
      },
    })

    const chartContainer = getByTestId("timeseries-chart")
    expect(chartContainer).toBeTruthy()

    const canvas = chartContainer.querySelector("canvas")
    expect(canvas).toBeTruthy()
  })
})
