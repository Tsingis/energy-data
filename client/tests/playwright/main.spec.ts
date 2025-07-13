import { test, expect } from "@playwright/test"
import { setupMocks } from "./mockSetup"

test("Page works", async ({ page }) => {
  await setupMocks(page)

  await page.goto("/")
  await expect(page).toHaveTitle("Energy in Finland")

  await page.waitForLoadState()
  await page.waitForLoadState("networkidle")

  const title = page.locator("h1:first-of-type")
  await expect(title).toBeVisible()

  const chart = page.getByTestId("timeseries-chart")
  await expect(chart).toBeVisible()

  const slider = page.getByTestId("range-slider")
  await expect(slider).toBeVisible()

  await expect(page).toHaveScreenshot("page.png")
})
