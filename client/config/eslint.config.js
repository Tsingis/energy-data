import js from "@eslint/js"
import parser from "@typescript-eslint/parser"
import globals from "globals"
import vue from "eslint-plugin-vue"

export default [
  js.configs.recommended,
  {
    files: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"],
    ignores: ["dist", "**/*.test.tsx", "**/eslint.config.js"],
    languageOptions: {
      ...vue.configs.flat.recommended.languageOptions,
      parser: parser,
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
        ecmaVersion: "latest",
        sourceType: "module",
        globals: {
          ...globals.browser,
          ...globals.node,
        },
      },
    },
    plugins: {},
    rules: {
      semi: ["error", "never"],
      "no-undef": "warn",
      "no-unused-vars": "warn",
    },
    settings: {
      vue: {
        version: "detect",
      },
    },
  },
]
