module.exports = {
    parser: 'vue-eslint-parser',
    parserOptions: {
      parser: '@babel/eslint-parser', // Use '@babel/eslint-parser' instead of 'babel-eslint'
      requireConfigFile: false, // Allows ESLint to function without a Babel config file
    },
    extends: [
      'plugin:vue/vue3-recommended', // or 'plugin:vue/essential' for Vue 2 projects
      'eslint:recommended'
    ],
    rules: {
      // Your custom ESLint rules
    }
  };
  