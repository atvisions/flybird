<template>
  <div class="skills">
    <v-container>
      <div v-for="(category, index) in skillCategories" :key="index" class="skill-category">
        <div class="d-flex align-center justify-space-between mb-2">
          <h3 class="text-h6">技能类别 {{ index + 1 }}</h3>
          <v-btn
            icon="mdi-delete"
            size="small"
            color="error"
            variant="text"
            @click="removeCategory(index)"
          ></v-btn>
        </div>
        
        <v-row>
          <v-col cols="12">
            <v-text-field
              v-model="category.name"
              label="类别名称"
              required
              :rules="[v => !!v || '请输入类别名称']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          
          <v-col cols="12">
            <div v-for="(skill, skillIndex) in category.skills" :key="skillIndex" class="skill-item">
              <div class="d-flex align-center gap-4">
                <v-text-field
                  v-model="skill.name"
                  label="技能名称"
                  class="flex-grow-1"
                  @input="updateConfig"
                ></v-text-field>
                
                <v-rating
                  v-model="skill.level"
                  color="warning"
                  hover
                  length="5"
                  size="small"
                  @update:modelValue="updateConfig"
                ></v-rating>
                
                <v-btn
                  icon="mdi-delete"
                  size="small"
                  color="error"
                  variant="text"
                  @click="removeSkill(index, skillIndex)"
                ></v-btn>
              </div>
            </div>
            
            <div class="text-center mt-2">
              <v-btn
                color="primary"
                variant="text"
                size="small"
                prepend-icon="mdi-plus"
                @click="addSkill(index)"
              >
                添加技能
              </v-btn>
            </div>
          </v-col>
        </v-row>
        
        <v-divider v-if="index < skillCategories.length - 1" class="my-4"></v-divider>
      </div>

      <div class="text-center mt-4">
        <v-btn
          color="primary"
          variant="text"
          prepend-icon="mdi-plus"
          @click="addCategory"
        >
          添加技能类别
        </v-btn>
      </div>
    </v-container>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      categories: []
    })
  }
})

const emit = defineEmits(['update:config'])

const skillCategories = ref(props.config.categories || [])

// 监听配置变化
watch(() => props.config, (newConfig) => {
  skillCategories.value = newConfig.categories || []
}, { deep: true })

// 添加技能类别
const addCategory = () => {
  skillCategories.value.push({
    name: '',
    skills: []
  })
  updateConfig()
}

// 移除技能类别
const removeCategory = (index) => {
  skillCategories.value.splice(index, 1)
  updateConfig()
}

// 添加技能
const addSkill = (categoryIndex) => {
  skillCategories.value[categoryIndex].skills.push({
    name: '',
    level: 3
  })
  updateConfig()
}

// 移除技能
const removeSkill = (categoryIndex, skillIndex) => {
  skillCategories.value[categoryIndex].skills.splice(skillIndex, 1)
  updateConfig()
}

// 更新配置
const updateConfig = () => {
  emit('update:config', {
    ...props.config,
    categories: skillCategories.value
  })
}
</script>

<style scoped>
.skills {
  padding: 16px;
}

.skill-category {
  margin-bottom: 24px;
}

.skill-item {
  margin-bottom: 8px;
}
</style> 