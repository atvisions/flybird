<template>
  <footer class="bg-gray-900 text-gray-300">
    <!-- 主要内容区 -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
        <!-- 公司简介 -->
        <div class="space-y-4">
          <div class="flex items-center space-x-2">
            <img src="@/assets/images/logo.png" alt="FlyBird" class="h-8 w-auto">
            <span class="text-xl font-bold text-white">飞鸟简历</span>
          </div>
          <p class="text-sm text-gray-400 leading-relaxed">
            飞鸟简历是一个专业的简历制作和作品集展示平台，致力于帮助用户打造专业的个人品牌形象，连接全球职业发展机会。
          </p>
        </div>

        <!-- 产品服务 -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-4">产品服务</h3>
          <ul class="space-y-3">
            <li><a href="#" class="hover:text-white transition-colors">简历模板</a></li>
            <li><a href="#" class="hover:text-white transition-colors">作品集展示</a></li>
            <li><a href="#" class="hover:text-white transition-colors">社区交流</a></li>
            <li><a href="#" class="hover:text-white transition-colors">职业发展</a></li>
            <li><a href="#" class="hover:text-white transition-colors">企业服务</a></li>
          </ul>
        </div>

        <!-- 帮助支持 -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-4">帮助支持</h3>
          <ul class="space-y-3">
            <li><a href="#" class="hover:text-white transition-colors">使用指南</a></li>
            <li><a href="#" class="hover:text-white transition-colors">常见问题</a></li>
            <li><a href="#" class="hover:text-white transition-colors">意见反馈</a></li>
            <li><a href="#" class="hover:text-white transition-colors">联系我们</a></li>
            <li><a href="#" class="hover:text-white transition-colors">隐私政策</a></li>
          </ul>
        </div>

        <!-- 联系方式 -->
        <div>
          <h3 class="text-lg font-semibold text-white mb-4">联系我们</h3>
          <ul class="space-y-3">
            <li class="flex items-center space-x-3">
              <PhoneIcon class="h-5 w-5 text-gray-400" />
              <span>400-888-8888</span>
            </li>
            <li class="flex items-center space-x-3">
              <EnvelopeIcon class="h-5 w-5 text-gray-400" />
              <span>support@flybirdx.com</span>
            </li>
            <li class="flex items-center space-x-3">
              <MapPinIcon class="h-5 w-5 text-gray-400" />
              <span>上海市青浦区沪青平公路3398号</span>
            </li>
          </ul>
          <!-- 微信公众号 -->
          <div class="mt-6">
            <span class="block text-sm font-medium mb-2">关注公众号</span>
            <img src="@/assets/images/qrcode.jpg" alt="微信公众号" class="h-24 w-24 bg-white p-1 rounded">
          </div>
        </div>
      </div>
    </div>

    <!-- 底部版权信息 -->
    <div class="border-t border-gray-800">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="md:flex md:items-center md:justify-between">
          <div class="text-sm">
            <p>&copy; 2024 FlyBirdX. All rights reserved.</p>
          </div>
          <div class="mt-4 md:mt-0">
            <div class="flex space-x-6 text-sm">
              <a href="#" class="hover:text-white transition-colors">服务条款</a>
              <a href="#" class="hover:text-white transition-colors">隐私政策</a>
              <a href="#" class="hover:text-white transition-colors">Cookie 政策</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { PhoneIcon, EnvelopeIcon, MapPinIcon } from '@heroicons/vue/24/outline'
</script>