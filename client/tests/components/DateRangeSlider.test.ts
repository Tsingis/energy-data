import { render, fireEvent } from "@testing-library/vue"
import { describe, it, expect } from "vitest"
import DateRangeSlider from "../../src/components/DateRangeSlider.vue"

describe("DateRangeSlider.vue", () => {
  it("renders correctly with default props", () => {
    const { container } = render(DateRangeSlider, {
      props: {
        modelValue: [new Date(0), new Date()],
      },
    })
    expect(container.querySelector("[data-testid='range-slider']")).toBeTruthy()
  })

  it("emits 'update:modelValue' when slider is moved", async () => {
    const { container, emitted } = render(DateRangeSlider, {
      props: {
        modelValue: [new Date(0), new Date()],
      },
    })

    const slider = container.querySelector("[data-testid='range-slider-track']")
    expect(slider).toBeTruthy()

    await fireEvent.mouseDown(slider!, { clientX: 50 })
    await fireEvent.mouseMove(globalThis, { clientX: 100 })
    await fireEvent.mouseUp(globalThis)

    expect(emitted()["update:modelValue"]).toBeTruthy()
  })

  it("emits 'start' and 'end' events on interaction", async () => {
    const { container, emitted } = render(DateRangeSlider, {
      props: {
        modelValue: [new Date(0), new Date()],
      },
    })

    const slider = container.querySelector("[data-testid='range-slider-track']")
    expect(slider).toBeTruthy()

    await fireEvent.mouseDown(slider!, { clientX: 50 })
    expect(emitted()["start"]).toBeTruthy()

    await fireEvent.mouseUp(globalThis)
    expect(emitted()["end"]).toBeTruthy()
  })

  it("respects min and max props", async () => {
    const minDate = new Date(0)
    const maxDate = new Date(1000000000)
    const { container, emitted } = render(DateRangeSlider, {
      props: {
        modelValue: [minDate, maxDate],
        min: minDate,
        max: maxDate,
      },
    })

    const slider = container.querySelector("[data-testid='range-slider-track']")
    expect(slider).toBeTruthy()

    await fireEvent.mouseDown(slider!, { clientX: 50 })
    await fireEvent.mouseMove(globalThis, { clientX: 100 })
    await fireEvent.mouseUp(globalThis)

    const emittedValue = (emitted()["update:modelValue"] as [Date[]][])[0][0]
    expect(emittedValue[0].getTime()).toBeGreaterThanOrEqual(minDate.getTime())
    expect(emittedValue[1].getTime()).toBeLessThanOrEqual(maxDate.getTime())
  })

  it("formats slider thumb date values with exact format", async () => {
    const formatValue = (date: Date) => {
      const options: Intl.DateTimeFormatOptions = {
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
      }
      return date.toLocaleString("en-US", options)
    }

    const { emitted } = render(DateRangeSlider, {
      props: {
        modelValue: [
          new Date("2025-01-01T15:55:00"),
          new Date("2025-12-31T23:59:00"),
        ],
        formatValue,
      },
    })

    const initialStartDate = formatValue(new Date("2025-01-01T15:55:00"))
    const initialEndDate = formatValue(new Date("2025-12-31T23:59:00"))

    expect(initialStartDate).toBe("Jan 1, 3:55 PM")
    expect(initialEndDate).toBe("Dec 31, 11:59 PM")

    expect(emitted()["update:modelValue"]).toBeUndefined()
  })
})
