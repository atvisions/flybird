module.exports = {
  presets: [
    '@vue/cli-plugin-babel/preset'
  ],
  plugins: [
    ['@babel/plugin-transform-object-rest-spread', { useBuiltIns: true }]
  ]
}
