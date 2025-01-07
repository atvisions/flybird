<template>
  <PortfolioList
    :title="categoryConfig.title"
    :description="categoryConfig.description"
    type="design"
    :menu-groups="menuGroups"
    :works="works"
  />
</template>

<script setup>
import PortfolioList from '@/components/portfolio/PortfolioList.vue'
import { portfolioCategories, generateMenuGroups } from '@/config/portfolioCategories'
import { usePortfolioData } from '@/composables/usePortfolioData'

const categoryConfig = portfolioCategories.design
const menuGroups = generateMenuGroups('design')
const { works } = usePortfolioData('design')
</script> 