const { defineConfig } = require('@vue/cli-service')
const path = require('path')
require('dotenv').config()

module.exports = defineConfig({
  transpileDependencies: true,
  runtimeCompiler: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
        'vue$': 'vue/dist/vue.esm-bundler.js'
      }
    }
  },
  chainWebpack: config => {
    // 设置页面标题
    config.plugin('html').tap(args => {
      args[0].title = '飞鸟简历'
      return args
    })
  },
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://192.168.3.16:8000',
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          '^/api': '/api'
        }
      }
    }
  }
})