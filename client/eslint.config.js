import globals from "globals"
import js from "@eslint/js"
import parser from "@typescript-eslint/parser"
import vueParser from "vue-eslint-parser"
import tsPlugin from "@typescript-eslint/eslint-plugin"
import vuePlugin from "eslint-plugin-vue"
import importPlugin from "eslint-plugin-import"
import securityPlugin from "eslint-plugin-security"
import playwrightPlugin from "eslint-plugin-playwright"
import sonarPlugin from "eslint-plugin-sonarjs"

export default [
  js.configs.recommended,
  ...vuePlugin.configs["flat/strongly-recommended"],
  {
    ...playwrightPlugin.configs["flat/recommended"],
    files: ["tests/playwright/**"],
    rules: {
      ...playwrightPlugin.configs["flat/recommended"].rules,
    },
  },
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
      vue: vuePlugin,
      import: importPlugin,
      security: securityPlugin,
      sonarjs: sonarPlugin,
    },
    rules: {
      ...tsPlugin.configs.recommended.rules,
      ...importPlugin.configs.recommended.rules,
      ...securityPlugin.configs.recommended.rules,
      ...sonarPlugin.configs.recommended.rules,
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { prefer: "type-imports" },
      ],
      "import/no-unresolved": "off",
      "security/detect-object-injection": "off",
      "sonarjs/todo-tag": "off",
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
    ignores: ["**/dist/**", "**/node_modules/**"],
  },
]
