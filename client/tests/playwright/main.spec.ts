import { test, expect } from "@playwright/test"
import { setupMocks } from "./mockSetup"

test("Page works", async ({ page }) => {
  await setupMocks(page)

  await page.goto("http://localhost:3000")
  await expect(page).toHaveTitle("Energy in Finland")

  const title = page.locator("h1:first-of-type")
  await expect(title).toBeVisible()

  const chart = page.getByTestId("timeseries-chart")
  await expect(chart).toBeVisible()

  await page.waitForLoadState()
  await page.waitForLoadState("networkidle")

  await expect(page).toHaveScreenshot("page.png")
})
