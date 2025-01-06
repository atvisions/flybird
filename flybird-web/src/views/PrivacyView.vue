<template>
  <HeadView />
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-4xl font-bold text-gray-900 mb-8 text-center">隐私政策</h1>
    <div class="bg-white rounded-lg shadow-sm p-8">
      <div class="prose prose-indigo max-w-none">
        <p class="text-lg text-gray-600 mb-8">
          飞鸟简历深知个人信息对您的重要性，我们将按照法律法规要求，采取相应的保护措施，尽力保护您的个人信息安全可控。
        </p>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">1. 信息收集</h2>
        <p class="text-gray-600 mb-4">我们收集信息的主要目的在于为您提供更好的服务。我们收集的信息类型包括：</p>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>账号信息（手机号、邮箱等）</li>
          <li>个人身份信息（姓名、性别等）</li>
          <li>简历内容</li>
          <li>使用记录</li>
          <li>设备信息</li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">2. 信息使用</h2>
        <p class="text-gray-600 mb-8">
          我们严格遵守法律法规的规定及与用户的约定，将收集的信息用于以下用途：
        </p>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>向您提供产品或服务</li>
          <li>满足您的个性化需求</li>
          <li>产品开发和服务优化</li>
          <li>安全保障</li>
          <li>向您推荐您可能感兴趣的产品或服务</li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">3. 信息保护</h2>
        <p class="text-gray-600 mb-4">
          我们采取业界先进的技术措施和数据安全措施来保护您的个人信息：
        </p>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>数据加密传输</li>
          <li>严格的数据访问权限控制</li>
          <li>定期安全评估</li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">4. 信息共享</h2>
        <p class="text-gray-600 mb-8">
          除非获得您的明确同意，我们不会与任何第三方分享您的个人信息。但以下情况除外：
        </p>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>法律法规规定必须提供</li>
          <li>获得您的明确授权</li>
          <li>维护社会公共利益</li>
        </ul>
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