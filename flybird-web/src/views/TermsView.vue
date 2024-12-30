<template>
  <HeadView />
  <div class="max-w-4xl mx-auto px-4 py-12">
    <h1 class="text-4xl font-bold text-gray-900 mb-8 text-center">服务条款</h1>
    <div class="bg-white rounded-lg shadow-sm p-8">
      <div class="prose prose-indigo max-w-none">
        <p class="text-lg text-gray-600 mb-8">
          欢迎使用飞鸟简历服务。请仔细阅读以下条款，使用我们的服务即表示您同意接受这些条款的约束。
        </p>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">1. 账号安全</h2>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>用户需要妥善保管账号密码，不得将账号提供给他人使用</li>
          <li>如发现账号被他人非法使用，应立即通知我们</li>
          <li>我们有权对违规账号进行警告、限制或终止使用</li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">2. 用户行为规范</h2>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>用户提交的简历内容必须真实可靠</li>
          <li>不得上传含有违法、侵权等信息的内容</li>
          <li>不得从事任何可能损害本平台的行为</li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">3. 知识产权</h2>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>平台所有内容的知识产权归我们所有</li>
          <li>用户创建的简历内容的著作权归用户所有</li>
          <li>未经授权，不得对平台内容进行复制、修改或传播</li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">4. 服务变更与终止</h2>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>我们保留随时修改或终止服务的权利</li>
          <li>服务变更会提前通知用户</li>
          <li>用户可以随时终止使用我们的服务</li>
        </ul>

        <h2 class="text-2xl font-bold text-gray-900 mb-4">5. 免责声明</h2>
        <p class="text-gray-600 mb-8">
          我们不对因下列情况导致的任何损失承担责任：
        </p>
        <ul class="list-disc pl-6 mb-8 text-gray-600">
          <li>因不可抗力导致的服务中断</li>
          <li>用户自身原因导致的信息泄露</li>
          <li>第三方造成的损失</li>
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