import { render } from "@testing-library/vue"
import { describe, it, expect } from "vitest"
import Loading from "../../src/components/Loading.vue"

describe("Loading.vue", () => {
  it("renders correctly with default props", () => {
    const { container } = render(Loading)
    const loading = container.querySelector("[data-testid='loading']")
    const spinnerIcon = loading?.querySelector("svg")
    expect(spinnerIcon).toBeTruthy()
    expect(spinnerIcon?.classList.contains("fa-1x")).toBe(true)
  })
})
