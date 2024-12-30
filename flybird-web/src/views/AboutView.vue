<template>
  <HeadView />
  <div class="max-w-6xl mx-auto px-4 py-12">
    <div class="text-center mb-16">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">关于飞鸟简历</h1>
      <p class="text-xl text-gray-600 max-w-3xl mx-auto">让每个人都能轻松制作出专业的简历，助力职业发展</p>
    </div>

    <!-- 核心价值 -->
    <div class="grid md:grid-cols-3 gap-8 mb-16">
      <div class="text-center p-6 bg-white rounded-lg shadow-sm">
        <div class="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">专业可靠</h3>
        <p class="text-gray-600">提供多样化的专业简历模板，确保您的简历始终保持最高标准</p>
      </div>

      <div class="text-center p-6 bg-white rounded-lg shadow-sm">
        <div class="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">简单高效</h3>
        <p class="text-gray-600">智能简历制作工具，让您在几分钟内完成一份专业简历</p>
      </div>

      <div class="text-center p-6 bg-white rounded-lg shadow-sm">
        <div class="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <svg class="w-8 h-8 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-900 mb-2">个性定制</h3>
        <p class="text-gray-600">丰富的个性化设置，让您的简历独具特色</p>
      </div>
    </div>

    <!-- 公司介绍 -->
    <div class="bg-white rounded-lg shadow-sm p-8 mb-16">
      <h2 class="text-3xl font-bold text-gray-900 mb-6">我们的故事</h2>
      <div class="prose prose-indigo max-w-none">
        <p class="text-lg text-gray-600 leading-relaxed">
          飞鸟简历成立于2023年，是一家专注于为求职者提供专业简历解决方案的科技公司。我们的团队由经验丰富的HR专家、UI设计师和技术工程师组成，致力于通过技术创新，帮助每一位求职者展现最好的自己。
        </p>
        <p class="text-lg text-gray-600 leading-relaxed mt-4">
          在竞争激烈的就业市场中，一份出色的简历可以让您脱颖而出。我们深知简历对求职的重要性，因此不断创新和优化我们的产品，为用户提供最好的简历制作体验。
        </p>
      </div>
    </div>

    <!-- 数据统计 -->
    <div class="grid md:grid-cols-4 gap-8 text-center">
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="text-4xl font-bold text-indigo-600 mb-2">100+</div>
        <div class="text-gray-600">精美模板</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="text-4xl font-bold text-indigo-600 mb-2">50万+</div>
        <div class="text-gray-600">注册用户</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="text-4xl font-bold text-indigo-600 mb-2">98%</div>
        <div class="text-gray-600">好评率</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm p-6">
        <div class="text-4xl font-bold text-indigo-600 mb-2">24h</div>
        <div class="text-gray-600">客服支持</div>
      </div>
    </div>
  </div>
  <FootView />
</template>

<script>
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'

export default {
  components: {
    HeadView,
    FootView
  }
}
</script>