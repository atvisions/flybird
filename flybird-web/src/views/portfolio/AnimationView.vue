<template>
  <PortfolioList
    :title="categoryConfig.title"
    :description="categoryConfig.description"
    type="animation"
    :menu-groups="menuGroups"
    :works="works"
  />
</template>

<script setup>
import PortfolioList from '@/components/portfolio/PortfolioList.vue'
import { portfolioCategories, generateMenuGroups } from '@/config/portfolioCategories'
import { usePortfolioData } from '@/composables/usePortfolioData'

const categoryConfig = portfolioCategories.animation
const menuGroups = generateMenuGroups('animation')
const { works } = usePortfolioData('animation')
</script> 