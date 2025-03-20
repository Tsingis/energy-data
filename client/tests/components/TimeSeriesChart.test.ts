import { render } from "@testing-library/vue"
import { describe, it, expect } from "vitest"
import TimeSeriesChart from "../../src/components/TimeSeriesChart.vue"

describe("TimeSeriesChart.vue", () => {
  it("renders correctly with empty values", () => {
    const { container } = render(TimeSeriesChart, {
      props: {
        datasets: {
          labels: [],
          datasets: [],
        },
        minTimestamp: new Date(),
        maxTimestamp: new Date(),
      },
    })

    const chartContainer = container.querySelector(".chart-container")
    expect(chartContainer).toBeTruthy()

    const canvas = container.querySelector("canvas")
    expect(canvas).toBeTruthy()
  })
})
