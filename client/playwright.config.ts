/// <reference types="node" />
import { defineConfig, devices, type ViewportSize } from "@playwright/test"

const baseUrl = "http://localhost:3000"

const viewports: Record<string, ViewportSize> = {
  mobile: { width: 390, height: 844 },
  tablet: { width: 768, height: 1024 },
  desktop: { width: 1440, height: 900 },
}

const browsers = [
  { name: "chromium", device: devices["Desktop Chrome"] },
  { name: "firefox", device: devices["Desktop Firefox"] },
  { name: "webkit", device: devices["Desktop Safari"] },
]

export default defineConfig({
  testDir: "./tests/playwright",
  fullyParallel: true,
  reporter: "list",
  timeout: 60_000,
  retries: process.env.CI ? 5 : 0,
  workers: Number(process.env.WORKERS) || undefined,
  expect: {
    timeout: 10_000,
    toHaveScreenshot: {
      maxDiffPixelRatio: Number(process.env.MAX_DIFF_PIXEL_RATIO) || 0,
      animations: "disabled",
    },
  },
  webServer: [
    {
      command: "npm run preview",
      reuseExistingServer: !process.env.CI,
      stdout: "ignore",
      stderr: "pipe",
      timeout: 60_000,
      url: "http://localhost:3000",
    },
  ],
  projects: browsers.flatMap(({ name, device }) =>
    Object.entries(viewports).map(([viewportName, viewport]) => ({
      name: `${name}-${viewportName}`,
      use: {
        ...device,
        baseURL: baseUrl,
        viewport,
        screenshot: "off",
        video: "off",
        trace: "off",
      },
    }))
  ),
})
