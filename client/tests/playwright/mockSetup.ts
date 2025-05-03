import { type Page } from "@playwright/test"
import { MOCK_NOW, mockEnergyData, mockPriceData } from "./mockData"

declare global {
  interface Window {
    useDate: () => {
      getDate: () => Date
    }
    Date: DateConstructor
  }
}

export async function setupMocks(page: Page) {
  await page.addInitScript(
    ({ mockDate }: { mockDate: Date }) => {
      window.useDate = () => ({
        getDate: () => mockDate,
      })
      const RealDate = Date
      const MockDate = class extends RealDate {
        constructor()
        constructor(...args: unknown[]) {
          if (args.length === 0) {
            super(mockDate)
          } else {
            super(...(args as []))
          }
        }
      }
      window.Date = MockDate as DateConstructor
    },
    { mockDate: MOCK_NOW }
  )
  await page.route("**/data/energy", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(mockEnergyData),
    })
  })

  await page.route("**/data/price", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(mockPriceData),
    })
  })
}
