<template>
  <div class="projects">
    <v-container>
      <div v-for="(project, index) in projects" :key="index" class="project-item">
        <div class="d-flex align-center justify-space-between mb-2">
          <h3 class="text-h6">项目经历 {{ index + 1 }}</h3>
          <v-btn
            icon="mdi-delete"
            size="small"
            color="error"
            variant="text"
            @click="removeProject(index)"
          ></v-btn>
        </div>
        
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="project.name"
              label="项目名称"
              required
              :rules="[v => !!v || '请输入项目名称']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="project.role"
              label="担任角色"
              required
              :rules="[v => !!v || '请输入担任角色']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="project.duration"
              label="项目时间"
              placeholder="例如: 2021.01 - 2021.06"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="project.link"
              label="项目链接"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="project.description"
              label="项目描述"
              rows="3"
              @input="updateConfig"
            ></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="project.responsibilities"
              label="主要职责"
              rows="3"
              @input="updateConfig"
            ></v-textarea>
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="project.achievements"
              label="项目成果"
              rows="3"
              @input="updateConfig"
            ></v-textarea>
          </v-col>
          
          <!-- 技术栈 -->
          <v-col cols="12">
            <div class="d-flex align-center mb-2">
              <span class="text-subtitle-1">使用技术</span>
              <v-spacer></v-spacer>
              <v-btn
                color="primary"
                variant="text"
                size="small"
                prepend-icon="mdi-plus"
                @click="addTechnology(index)"
              >
                添加技术
              </v-btn>
            </div>
            
            <div class="tech-stack">
              <v-chip
                v-for="(tech, techIndex) in project.technologies"
                :key="techIndex"
                class="ma-1"
                closable
                @click:close="removeTechnology(index, techIndex)"
              >
                {{ tech }}
              </v-chip>
            </div>
            
            <v-dialog v-model="showTechDialog" max-width="400px">
              <v-card>
                <v-card-title>添加技术</v-card-title>
                <v-card-text>
                  <v-text-field
                    v-model="newTechnology"
                    label="技术名称"
                    @keyup.enter="confirmAddTechnology"
                  ></v-text-field>
                </v-card-text>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn color="primary" variant="text" @click="confirmAddTechnology">
                    确定
                  </v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-col>
        </v-row>
        
        <v-divider v-if="index < projects.length - 1" class="my-4"></v-divider>
      </div>

      <div class="text-center mt-4">
        <v-btn
          color="primary"
          variant="text"
          prepend-icon="mdi-plus"
          @click="addProject"
        >
          添加项目经历
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
      projects: []
    })
  }
})

const emit = defineEmits(['update:config'])

const projects = ref(props.config.projects || [])
const showTechDialog = ref(false)
const newTechnology = ref('')
const currentProjectIndex = ref(0)

// 监听配置变化
watch(() => props.config, (newConfig) => {
  projects.value = newConfig.projects || []
}, { deep: true })

// 添加项目
const addProject = () => {
  projects.value.push({
    name: '',
    role: '',
    duration: '',
    link: '',
    description: '',
    responsibilities: '',
    achievements: '',
    technologies: []
  })
  updateConfig()
}

// 移除项目
const removeProject = (index) => {
  projects.value.splice(index, 1)
  updateConfig()
}

// 添加技术
const addTechnology = (projectIndex) => {
  currentProjectIndex.value = projectIndex
  newTechnology.value = ''
  showTechDialog.value = true
}

// 确认添加技术
const confirmAddTechnology = () => {
  if (newTechnology.value.trim()) {
    if (!projects.value[currentProjectIndex.value].technologies) {
      projects.value[currentProjectIndex.value].technologies = []
    }
    projects.value[currentProjectIndex.value].technologies.push(newTechnology.value.trim())
    updateConfig()
  }
  showTechDialog.value = false
}

// 移除技术
const removeTechnology = (projectIndex, techIndex) => {
  projects.value[projectIndex].technologies.splice(techIndex, 1)
  updateConfig()
}

// 更新配置
const updateConfig = () => {
  emit('update:config', {
    ...props.config,
    projects: projects.value
  })
}
</script>

<style scoped>
.projects {
  padding: 16px;
}

.project-item {
  margin-bottom: 24px;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  min-height: 40px;
  padding: 8px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 4px;
}
</style> 