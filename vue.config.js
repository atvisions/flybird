module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://192.168.3.16:8000',
        changeOrigin: true
      }
    }
  }
} 