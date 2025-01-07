<template>
  <PortfolioList
    :title="categoryConfig.title"
    :description="categoryConfig.description"
    type="photo"
    :menu-groups="menuGroups"
    :works="works"
  />
</template>

<script setup>
import PortfolioList from '@/components/portfolio/PortfolioList.vue'
import { portfolioCategories, generateMenuGroups } from '@/config/portfolioCategories'
import { usePortfolioData } from '@/composables/usePortfolioData'

const categoryConfig = portfolioCategories.photo
const menuGroups = generateMenuGroups('photo')
const { works } = usePortfolioData('photo')
</script> 