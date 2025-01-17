<template>
  <div class="experience">
    <v-container>
      <div v-for="(exp, index) in experiences" :key="index" class="experience-item">
        <div class="d-flex align-center justify-space-between mb-2">
          <h3 class="text-h6">工作经历 {{ index + 1 }}</h3>
          <v-btn
            icon="mdi-delete"
            size="small"
            color="error"
            variant="text"
            @click="removeExperience(index)"
          ></v-btn>
        </div>
        
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="exp.company"
              label="公司"
              required
              :rules="[v => !!v || '请输入公司名称']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="exp.position"
              label="职位"
              required
              :rules="[v => !!v || '请输入职位名称']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="exp.duration"
              label="工作时间"
              placeholder="例如: 2020.07 - 至今"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="exp.location"
              label="工作地点"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="exp.description"
              label="工作内容"
              rows="3"
              @input="updateConfig"
            ></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="exp.achievements"
              label="工作成就"
              rows="3"
              @input="updateConfig"
            ></v-textarea>
          </v-col>
        </v-row>
        
        <v-divider v-if="index < experiences.length - 1" class="my-4"></v-divider>
      </div>

      <div class="text-center mt-4">
        <v-btn
          color="primary"
          variant="text"
          prepend-icon="mdi-plus"
          @click="addExperience"
        >
          添加工作经历
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
      experiences: []
    })
  }
})

const emit = defineEmits(['update:config'])

const experiences = ref(props.config.experiences || [])

// 监听配置变化
watch(() => props.config, (newConfig) => {
  experiences.value = newConfig.experiences || []
}, { deep: true })

// 添加工作经历
const addExperience = () => {
  experiences.value.push({
    company: '',
    position: '',
    duration: '',
    location: '',
    description: '',
    achievements: ''
  })
  updateConfig()
}

// 移除工作经历
const removeExperience = (index) => {
  experiences.value.splice(index, 1)
  updateConfig()
}

// 更新配置
const updateConfig = () => {
  emit('update:config', {
    ...props.config,
    experiences: experiences.value
  })
}
</script>

<style scoped>
.experience {
  padding: 16px;
}

.experience-item {
  margin-bottom: 24px;
}
</style> 