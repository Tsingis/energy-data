import { test, expect } from "@playwright/test"

test("Page works", async ({ page }) => {
  await page.goto("http://localhost:3000")
  await expect(page).toHaveTitle("Energy in Finland")

  const title = page.locator("h1:first-of-type")
  await expect(title).toBeVisible()

  await expect(page).toHaveScreenshot("page.png")
})
