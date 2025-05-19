import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import { checker } from "vite-plugin-checker"

const args = process.argv.slice(3)
const useChecker = args.includes("--use-checker")

export default defineConfig({
  plugins: [
    vue(),
    useChecker &&
      checker({
        vueTsc: {
          tsconfigPath: "./tsconfig.json",
        },
        eslint: {
          lintCommand: "eslint . --config ./eslint.config.js",
          useFlatConfig: true,
        },
      }),
  ],
  root: "src",
  publicDir: "public",
  envDir: "../..",
  build: {
    outDir: "../dist",
    emptyOutDir: true,
    rollupOptions: {
      input: "src/index.html",
    },
  },
  server: {
    port: 3000,
    host: true,
    strictPort: true,
    watch: {
      usePolling: true,
    },
  },
  preview: {
    port: 3000,
    host: true,
    strictPort: true,
  },
})
