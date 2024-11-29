import globals from "globals"
import js from "@eslint/js"
import plugin from "@typescript-eslint/eslint-plugin"
import parser from "@typescript-eslint/parser"
import pluginVue from "eslint-plugin-vue"
import pluginPrettier from "eslint-plugin-prettier"

export default [
  js.configs.recommended,
  ...pluginVue.configs["flat/strongly-recommended"],
  {
    files: ["**/*.{js,ts,vue}"],
    ignores: ["dist", "**/eslint.config.js", "**/*d.ts"],
    languageOptions: {
      parserOptions: {
        parser: parser,
        ecmaVersion: "latest",
        sourceType: "module",
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      vue: pluginVue,
      prettier: pluginPrettier,
      "@typescript-eslint": plugin,
    },
    rules: {
      "prettier/prettier": "error",
      semi: ["error", "never"],
      "no-undef": "warn",
      "no-unused-vars": "warn",
      "vue/html-self-closing": "off",
    },
    settings: {
      vue: {
        version: "detect",
      },
    },
  },
]
