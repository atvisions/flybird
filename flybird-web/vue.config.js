const { defineConfig } = require('@vue/cli-service')
const path = require('path')

module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
  chainWebpack: config => {
    // 设置页面标题
    config.plugin('html').tap(args => {
      args[0].title = '飞鸟简历'
      return args
    })
  },
  configureWebpack: {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    }
  },
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://192.168.2.25:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api'
        },
        onProxyReq(proxyReq) {
          // 添加调试日志
          console.log('Proxy Request:', {
            method: proxyReq.method,
            path: proxyReq.path,
            headers: proxyReq.getHeaders()
          })
        }
      }
    }
  }
})