<template>
  <div class="min-h-screen">
    <HeadView />
    <div class="flex-1">
      <router-view />
    </div>
    <FootView class="hidden md:block" />
  </div>
</template>

<script setup>
import HeadView from '@/components/HeadView.vue'
import FootView from '@/components/FootView.vue'
</script>

<style scoped>
.safe-area-inset-bottom {
  padding-bottom: env(safe-area-inset-bottom);
}

@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .pb-16 {
    padding-bottom: calc(4rem + env(safe-area-inset-bottom));
  }
}
</style> 