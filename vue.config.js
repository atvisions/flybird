module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': '/api/v1'  // 将 /api 重写为 /api/v1
        }
      }
    }
  }
} 