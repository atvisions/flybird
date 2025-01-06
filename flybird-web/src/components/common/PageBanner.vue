<template>
  <div class="hidden md:block mb-6">
    <div class="relative overflow-hidden rounded-2xl p-8 sm:p-10 min-h-[200px]"
      :class="[
        theme === 'rose' && 'bg-gradient-to-r from-rose-100/90 via-pink-100/80 to-rose-100/70',
        theme === 'blue' && 'bg-gradient-to-r from-blue-100/90 via-indigo-100/80 to-blue-100/70',
        theme === 'violet' && 'bg-gradient-to-r from-violet-100/90 via-purple-100/80 to-violet-100/70'
      ]"
    >
      <!-- 装饰性圆圈背景 -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-4 -right-4 w-24 h-24 rounded-full" :class="circleClasses[0]"></div>
        <div class="absolute top-1/2 -right-8 w-32 h-32 rounded-full" :class="circleClasses[1]"></div>
        <div class="absolute -bottom-8 right-1/4 w-40 h-40 rounded-full" :class="circleClasses[2]"></div>
        <div class="absolute top-1/4 -left-8 w-28 h-28 rounded-full" :class="circleClasses[1]"></div>
      </div>

      <!-- 装饰性波浪线 -->
      <div class="absolute inset-0 overflow-hidden">
        <svg class="absolute top-0 right-0" width="400" height="400" viewBox="0 0 400 400"
          :class="waveColor"
        >
          <path d="M0,100 C100,120 200,80 300,100 S400,120 500,100" fill="none" stroke="currentColor" stroke-width="2"/>
          <path d="M0,150 C100,170 200,130 300,150 S400,170 500,150" fill="none" stroke="currentColor" stroke-width="2"/>
        </svg>
      </div>

      <!-- 装饰性点阵 -->
      <div class="absolute inset-0">
        <div class="absolute top-12 right-12 grid grid-cols-3 gap-2">
          <template v-for="n in 9" :key="n">
            <div class="w-1 h-1 rounded-full" :class="dotColor"></div>
          </template>
        </div>
      </div>

      <!-- 内容区域 -->
      <div class="relative z-10">
        <slot></slot>
      </div>
      
      <!-- 右侧装饰作品 -->
      <div class="absolute right-0 top-0 bottom-0 w-1/3 hidden lg:block pointer-events-none">
        <!-- 装饰方块组 1 -->
        <div class="absolute right-24 top-8 w-40 h-32 rotate-6 transform hover:-translate-y-1 transition-transform">
          <div class="w-full h-full rounded-xl overflow-hidden shadow-lg p-4"
            :class="[
              theme === 'rose' && 'bg-gradient-to-br from-rose-400/10 to-pink-400/10',
              theme === 'blue' && 'bg-gradient-to-br from-blue-400/10 to-indigo-400/10',
              theme === 'violet' && 'bg-gradient-to-br from-violet-400/10 to-purple-400/10'
            ]"
          >
            <div class="w-full h-full rounded-lg bg-white/40 backdrop-blur-sm border border-white/60"></div>
          </div>
        </div>

        <!-- 装饰方块组 2 -->
        <div class="absolute right-40 top-16 w-36 h-28 -rotate-3 transform hover:-translate-y-1 transition-transform">
          <div class="w-full h-full rounded-xl overflow-hidden shadow-lg p-4"
            :class="[
              theme === 'rose' && 'bg-gradient-to-br from-pink-400/10 to-rose-400/10',
              theme === 'blue' && 'bg-gradient-to-br from-indigo-400/10 to-blue-400/10',
              theme === 'violet' && 'bg-gradient-to-br from-purple-400/10 to-violet-400/10'
            ]"
          >
            <div class="w-full h-full rounded-lg bg-white/40 backdrop-blur-sm border border-white/60"></div>
          </div>
        </div>

        <!-- 装饰方块组 3 -->
        <div class="absolute right-16 top-24 w-32 h-24 rotate-12 transform hover:-translate-y-1 transition-transform">
          <div class="w-full h-full rounded-xl overflow-hidden shadow-lg p-4"
            :class="[
              theme === 'rose' && 'bg-gradient-to-br from-rose-400/10 to-pink-400/10',
              theme === 'blue' && 'bg-gradient-to-br from-blue-400/10 to-indigo-400/10',
              theme === 'violet' && 'bg-gradient-to-br from-violet-400/10 to-purple-400/10'
            ]"
          >
            <div class="w-full h-full rounded-lg bg-white/40 backdrop-blur-sm border border-white/60"></div>
          </div>
        </div>

        <!-- 装饰性线条 -->
        <div class="absolute inset-0">
          <div class="absolute top-1/4 left-1/4 w-16 h-px transform rotate-45"
            :class="[
              theme === 'rose' && 'bg-gradient-to-r from-rose-300/20',
              theme === 'blue' && 'bg-gradient-to-r from-blue-300/20',
              theme === 'violet' && 'bg-gradient-to-r from-violet-300/20'
            ]"
          ></div>
          <div class="absolute top-1/3 right-1/3 w-12 h-px transform -rotate-45"
            :class="[
              theme === 'rose' && 'bg-gradient-to-l from-pink-300/20',
              theme === 'blue' && 'bg-gradient-to-l from-indigo-300/20',
              theme === 'violet' && 'bg-gradient-to-l from-purple-300/20'
            ]"
          ></div>
          <div class="absolute bottom-1/4 right-1/4 w-20 h-px transform rotate-12"
            :class="[
              theme === 'rose' && 'bg-gradient-to-l from-rose-300/20',
              theme === 'blue' && 'bg-gradient-to-l from-blue-300/20',
              theme === 'violet' && 'bg-gradient-to-l from-violet-300/20'
            ]"
          ></div>
        </div>

        <!-- 装饰性图形 -->
        <div class="absolute top-8 right-8 w-3 h-3 border-2 transform rotate-45"
          :class="[
            theme === 'rose' && 'border-rose-200/40',
            theme === 'blue' && 'border-blue-200/40',
            theme === 'violet' && 'border-violet-200/40'
          ]"
        ></div>
        <div class="absolute bottom-12 right-12 w-4 h-4 border-2 rounded-full"
          :class="[
            theme === 'rose' && 'border-pink-200/40',
            theme === 'blue' && 'border-indigo-200/40',
            theme === 'violet' && 'border-purple-200/40'
          ]"
        ></div>
        <div class="absolute top-1/2 right-1/4 w-2 h-2 transform rotate-45"
          :class="[
            theme === 'rose' && 'bg-rose-300/20',
            theme === 'blue' && 'bg-blue-300/20',
            theme === 'violet' && 'bg-violet-300/20'
          ]"
        ></div>
      </div>

      <!-- 背景装饰 -->
      <div class="absolute right-0 top-0 -mt-16 -mr-16">
        <div class="w-64 h-64 rounded-full blur-3xl" :class="bgGradientClass"></div>
      </div>
      <div class="absolute left-0 bottom-0 -mb-16 -ml-16">
        <div class="w-48 h-48 rounded-full blur-3xl" :class="bgGradientClass2"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  theme: {
    type: String,
    default: 'rose',
    validator: (value) => ['rose', 'blue', 'violet'].includes(value)
  }
})

// 根据主题计算各种颜色类
const circleClasses = computed(() => {
  const themeColors = {
    rose: ['bg-rose-200/30', 'bg-pink-200/20', 'bg-rose-200/10'],
    blue: ['bg-blue-200/30', 'bg-indigo-200/20', 'bg-blue-200/10'],
    violet: ['bg-violet-200/30', 'bg-purple-200/20', 'bg-violet-200/10']
  }
  return themeColors[props.theme]
})

const waveColor = computed(() => ({
  rose: 'text-rose-200/20',
  blue: 'text-blue-200/20',
  violet: 'text-violet-200/20'
}[props.theme]))

const dotColor = computed(() => ({
  rose: 'bg-rose-300/30',
  blue: 'bg-blue-300/30',
  violet: 'bg-violet-300/30'
}[props.theme]))

const lineColor = computed(() => ({
  rose: 'bg-gradient-to-r from-rose-300/20',
  blue: 'bg-gradient-to-r from-blue-300/20',
  violet: 'bg-gradient-to-r from-violet-300/20'
}[props.theme]))

const shapeColor = computed(() => ({
  rose: 'border-rose-200/40',
  blue: 'border-blue-200/40',
  violet: 'border-violet-200/40'
}[props.theme]))

const bgGradientClass = computed(() => ({
  rose: 'bg-gradient-to-r from-rose-200/40 to-pink-200/40',
  blue: 'bg-gradient-to-r from-blue-200/40 to-indigo-200/40',
  violet: 'bg-gradient-to-r from-violet-200/40 to-purple-200/40'
}[props.theme]))

const bgGradientClass2 = computed(() => ({
  rose: 'bg-gradient-to-r from-pink-200/40 to-rose-200/40',
  blue: 'bg-gradient-to-r from-indigo-200/40 to-blue-200/40',
  violet: 'bg-gradient-to-r from-purple-200/40 to-violet-200/40'
}[props.theme]))

// 装饰性方块配置
const decorativeBlocks = [
  {
    containerClass: 'absolute right-24 top-8 w-40 h-32 rotate-6 transform hover:-translate-y-1 transition-transform',
    gradientClass: computed(() => ({
      rose: 'bg-gradient-to-br from-rose-400/10 to-pink-400/10',
      blue: 'bg-gradient-to-br from-blue-400/10 to-indigo-400/10',
      violet: 'bg-gradient-to-br from-violet-400/10 to-purple-400/10'
    }[props.theme]))
  },
  // ... 其他方块配置
]

// 装饰性线条配置
const decorativeLines = [
  {
    class: 'absolute top-1/4 left-1/4 w-16 h-px transform rotate-45'
  },
  // ... 其他线条配置
]

// 装饰性图形配置
const decorativeShapes = [
  {
    class: 'absolute top-8 right-8 w-3 h-3 border-2 transform rotate-45'
  },
  // ... 其他图形配置
]
</script> 