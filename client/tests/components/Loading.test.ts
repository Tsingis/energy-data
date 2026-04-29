import { render } from "@testing-library/vue"
import { describe, it, expect } from "vitest"
import Loading from "../../src/components/Loading.vue"

describe("Loading.vue", () => {
  it("renders correctly with default props", () => {
    const { getByTestId } = render(Loading)
    const loading = getByTestId("loading")
    const spinnerIcon = loading?.querySelector("svg")
    expect(spinnerIcon).toBeTruthy()
    expect(spinnerIcon?.classList.contains("spin")).toBe(true)
  })
})
