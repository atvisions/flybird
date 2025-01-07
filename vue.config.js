const { defineConfig } = require('@vue/cli-service')
const path = require('path')

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
  // 使用 defineProperty 而不是 define
  chainWebpack: config => {
    config.plugin('define').tap(args => {
      Object.assign(args[0], {
        'import.meta.env.VITE_API_URL': JSON.stringify('http://192.168.3.16:8000')
      })
      return args
    })
    
    // 设置页面标题
    config.plugin('html').tap(args => {
      args[0].title = 'popo.work'
      return args
    })
  },
  devServer: {
    proxy: {
      '/v1': {
        target: 'http://192.168.3.16:8000',
        changeOrigin: true,
        ws: true,
        pathRewrite: {
          '^/v1': ''
        }
      }
    }
  }
})