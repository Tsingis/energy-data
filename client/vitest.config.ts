import { defineConfig } from "vitest/config"
import vue from "@vitejs/plugin-vue"

export default defineConfig({
  plugins: [vue()],
  test: {
    environment: "jsdom",
    setupFiles: ["tests/vitest.setup.ts"],
    globals: true,
    include: ["tests/components/**/*.test.ts"],
  },
})
