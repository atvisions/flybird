<template>
  <div class="education">
    <v-container>
      <div v-for="(edu, index) in educations" :key="index" class="education-item">
        <div class="d-flex align-center justify-space-between mb-2">
          <h3 class="text-h6">教育经历 {{ index + 1 }}</h3>
          <v-btn
            icon="mdi-delete"
            size="small"
            color="error"
            variant="text"
            @click="removeEducation(index)"
          ></v-btn>
        </div>
        
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="edu.school"
              label="学校"
              required
              :rules="[v => !!v || '请输入学校名称']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="edu.major"
              label="专业"
              required
              :rules="[v => !!v || '请输入专业名称']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="edu.degree"
              label="学位"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="edu.duration"
              label="就读时间"
              placeholder="例如: 2018.09 - 2022.06"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="edu.description"
              label="在校经历"
              rows="3"
              @input="updateConfig"
            ></v-textarea>
          </v-col>
        </v-row>
        
        <v-divider v-if="index < educations.length - 1" class="my-4"></v-divider>
      </div>

      <div class="text-center mt-4">
        <v-btn
          color="primary"
          variant="text"
          prepend-icon="mdi-plus"
          @click="addEducation"
        >
          添加教育经历
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
      educations: []
    })
  }
})

const emit = defineEmits(['update:config'])

const educations = ref(props.config.educations || [])

// 监听配置变化
watch(() => props.config, (newConfig) => {
  educations.value = newConfig.educations || []
}, { deep: true })

// 添加教育经历
const addEducation = () => {
  educations.value.push({
    school: '',
    major: '',
    degree: '',
    duration: '',
    description: ''
  })
  updateConfig()
}

// 移除教育经历
const removeEducation = (index) => {
  educations.value.splice(index, 1)
  updateConfig()
}

// 更新配置
const updateConfig = () => {
  emit('update:config', {
    ...props.config,
    educations: educations.value
  })
}
</script>

<style scoped>
.education {
  padding: 16px;
}

.education-item {
  margin-bottom: 24px;
}
</style> 