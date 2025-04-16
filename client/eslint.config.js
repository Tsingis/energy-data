import globals from "globals"
import js from "@eslint/js"
import parser from "@typescript-eslint/parser"
import vueParser from "vue-eslint-parser"
import tsPlugin from "@typescript-eslint/eslint-plugin"
import vuePlugin from "eslint-plugin-vue"
import importPlugin from "eslint-plugin-import"

export default [
  js.configs.recommended,
  ...vuePlugin.configs["flat/strongly-recommended"],
  {
    files: ["**/*.{js,ts,vue}"],
    languageOptions: {
      parser: vueParser,
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
      "@typescript-eslint": tsPlugin,
      import: importPlugin,
      vue: vuePlugin,
    },
    rules: {
      ...tsPlugin.configs.recommended.rules,
      ...importPlugin.configs.recommended.rules,
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { prefer: "type-imports" },
      ],
      "import/no-unresolved": "off",
      semi: ["error", "never"],
      "no-undef": "warn",
      "no-unused-vars": "warn",
      "vue/html-self-closing": "off",
      "vue/max-attributes-per-line": "off",
      "vue/multi-word-component-names": "off",
    },
    settings: {
      vue: {
        version: "detect",
      },
    },
  },
  {
    ignores: ["dist"],
  },
]
