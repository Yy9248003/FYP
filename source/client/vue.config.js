const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  // 生产环境优化
  productionSourceMap: false, // 关闭生产环境的source map，减小打包体积
  
  // 代码分割配置
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          // 第三方库单独打包
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          // Element UI / View UI Plus 单独打包
          elementUI: {
            name: 'chunk-elementUI',
            test: /[\\/]node_modules[\\/](view-ui-plus|iview)[\\/]/,
            priority: 20,
            chunks: 'all'
          },
          // ECharts 单独打包
          echarts: {
            name: 'chunk-echarts',
            test: /[\\/]node_modules[\\/](echarts|vue-echarts)[\\/]/,
            priority: 20,
            chunks: 'all'
          },
          // 公共代码
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: 5,
            chunks: 'initial',
            reuseExistingChunk: true
          }
        }
      }
    }
  },
  
  // 开发服务器配置
  devServer: {
    port: 8080,
    open: true,
    host: '0.0.0.0',  // 允许外部访问
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true,
        secure: false,  // 如果是https接口，需要配置这个参数
        logLevel: 'debug',  // 显示代理日志
        onError: (err, req, res) => {
          console.error('代理错误:', err.message);
          console.error('请确认后端服务已启动: http://127.0.0.1:8000');
        },
        onProxyReq: (proxyReq, req, res) => {
          console.log(`[代理] ${req.method} ${req.url} -> http://127.0.0.1:8000${req.url}`);
        }
      }
    }
  },
  
  // 性能优化（简化配置，避免插件兼容性问题）
  chainWebpack: config => {
    // 生产环境优化
    if (process.env.NODE_ENV === 'production') {
      // 压缩优化
      config.optimization.minimize(true)
    }
  }
})


module.exports = defineConfig({
  transpileDependencies: true,
  
  // 生产环境优化
  productionSourceMap: false, // 关闭生产环境的source map，减小打包体积
  
  // 代码分割配置
  configureWebpack: {
    optimization: {
      splitChunks: {
        chunks: 'all',
        cacheGroups: {
          // 第三方库单独打包
          vendor: {
            name: 'chunk-vendors',
            test: /[\\/]node_modules[\\/]/,
            priority: 10,
            chunks: 'initial'
          },
          // Element UI / View UI Plus 单独打包
          elementUI: {
            name: 'chunk-elementUI',
            test: /[\\/]node_modules[\\/](view-ui-plus|iview)[\\/]/,
            priority: 20,
            chunks: 'all'
          },
          // ECharts 单独打包
          echarts: {
            name: 'chunk-echarts',
            test: /[\\/]node_modules[\\/](echarts|vue-echarts)[\\/]/,
            priority: 20,
            chunks: 'all'
          },
          // 公共代码
          common: {
            name: 'chunk-common',
            minChunks: 2,
            priority: 5,
            chunks: 'initial',
            reuseExistingChunk: true
          }
        }
      }
    }
  },
  
  // 开发服务器配置
  devServer: {
    port: 8080,
    open: true,
    host: '0.0.0.0',  // 允许外部访问
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        ws: true,
        secure: false,  // 如果是https接口，需要配置这个参数
        logLevel: 'debug',  // 显示代理日志
        onError: (err, req, res) => {
          console.error('代理错误:', err.message);
          console.error('请确认后端服务已启动: http://127.0.0.1:8000');
        },
        onProxyReq: (proxyReq, req, res) => {
          console.log(`[代理] ${req.method} ${req.url} -> http://127.0.0.1:8000${req.url}`);
        }
      }
    }
  },
  
  // 性能优化（简化配置，避免插件兼容性问题）
  chainWebpack: config => {
    // 生产环境优化
    if (process.env.NODE_ENV === 'production') {
      // 压缩优化
      config.optimization.minimize(true)
    }
  }
})
