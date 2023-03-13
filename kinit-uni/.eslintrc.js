module.exports = {
  env: {
    browser: true,
    es6: true,
    node: true
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/recommended',
    'prettier',
    'plugin:prettier/recommended'
  ],
  parserOptions: {
    ecmaVersion: 2018,
    sourceType: 'module'
  },
  globals: {
    uni: true,
    wx: true,
    ROUTES: true
  },
  plugins: ['vue', 'prettier'],
  rules: {
    'vue/multi-word-component-names': 'off',
    'prettier/prettier': 'error',
    'vue/html-indent': ['error', 2],
    'vue/max-attributes-per-line': 'off',
    'no-console': 'off',
    'no-unused-vars': ['warn', { args: 'none' }],
    'arrow-parens': ['error', 'always'],
    'comma-dangle': ['error', 'never'],
    quotes: ['error', 'single'],
    semi: ['error', 'never'],
    'object-curly-spacing': ['error', 'always'],
    indent: ['error', 2, { SwitchCase: 1 }]
  }
}
