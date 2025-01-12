<template>
  <footer class="bg-white">
    <!-- 主分割线 -->
    <div class="border-t border-gray-100">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 md:grid-cols-6 gap-8">
          <!-- Logo 和简介 -->
          <div class="col-span-2">
            <div class="flex items-center space-x-2 mb-4">
              <img src="@/assets/images/logo.png" alt="FlyBird" class="h-8 w-auto">
              <span class="text-lg font-bold text-gray-900">飞鸟简历</span>
            </div>
            <p class="text-sm text-gray-500 leading-relaxed">
              专业的简历制作和作品集展示平台
            </p>
          </div>

          <!-- 产品 -->
          <div class="col-span-1">
            <h3 class="text-sm font-medium text-gray-900 mb-4">产品</h3>
            <ul class="space-y-3">
              <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">简历模板</a></li>
              <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">作品集展示</a></li>
              <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">社区交流</a></li>
            </ul>
          </div>

          <!-- 支持 -->
          <div class="col-span-1">
            <h3 class="text-sm font-medium text-gray-900 mb-4">支持</h3>
            <ul class="space-y-3">
              <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">使用指南</a></li>
              <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">常见问题</a></li>
              <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">意见反馈</a></li>
            </ul>
          </div>

          <!-- 法律和二维码并排 -->
          <div class="col-span-2 grid grid-cols-2 gap-4">
            <!-- 法律 -->
            <div>
              <h3 class="text-sm font-medium text-gray-900 mb-4">法律</h3>
              <ul class="space-y-3">
                <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">服务条款</a></li>
                <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">隐私政策</a></li>
                <li><a href="#" class="text-sm text-gray-500 hover:text-blue-600 transition-colors">Cookie 政策</a></li>
              </ul>
            </div>

            <!-- 微信二维码 -->
            <div class="flex flex-col items-center">
              <h3 class="text-sm font-medium text-gray-900 mb-4">关注我们</h3>
              <div class="flex flex-col items-center">
                <img 
                  src="@/assets/images/qrcode.jpg" 
                  alt="微信公众号" 
                  class="w-20 h-20 bg-white rounded-lg shadow-sm border border-gray-100 mb-2"
                >
                <p class="text-xs text-gray-500">扫码关注获取最新资讯</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 版权信息 -->
    <div class="border-t border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between text-sm text-gray-500">
          <span>&copy; 2024 FlyBirdX. All rights reserved.</span>
          <a 
            href="https://beian.miit.gov.cn" 
            target="_blank" 
            class="mt-2 md:mt-0 hover:text-blue-600 transition-colors"
          >
            沪ICP备2024102744号-1
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
</script>