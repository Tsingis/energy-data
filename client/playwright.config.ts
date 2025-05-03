import { defineConfig, devices } from "@playwright/test"

export default defineConfig({
  testDir: "./tests/playwright",
  fullyParallel: true,
  reporter: "list",
  timeout: 180_000,
  retries: 1,
  expect: {
    timeout: 60_000,
  },
  webServer: [
    {
      command: "npm run dev:testing",
      reuseExistingServer: !process.env.CI,
      stdout: "ignore",
      stderr: "pipe",
      timeout: 60_000,
    },
  ],
  projects: [
    {
      name: "firefox",
      use: {
        ...devices["Desktop Firefox"],
        viewport: { width: 1280, height: 800 },
        screenshot: "off",
        video: "off",
        trace: "off",
      },
    },
    {
      name: "webkit",
      use: {
        ...devices["Desktop Safari"],
        viewport: { width: 1280, height: 800 },
        screenshot: "off",
        video: "off",
        trace: "off",
      },
    },
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        viewport: { width: 1280, height: 800 },
        screenshot: "off",
        video: "off",
        trace: "off",
      },
    },
  ],
})
