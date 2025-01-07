<template>
  <PortfolioList
    :title="categoryConfig.title"
    :description="categoryConfig.description"
    type="video"
    :menu-groups="menuGroups"
    :works="works"
  />
</template>

<script setup>
import PortfolioList from '@/components/portfolio/PortfolioList.vue'
import { portfolioCategories, generateMenuGroups } from '@/config/portfolioCategories'
import { usePortfolioData } from '@/composables/usePortfolioData'

const categoryConfig = portfolioCategories.video
const menuGroups = generateMenuGroups('video')
const { works } = usePortfolioData('video')
</script> 