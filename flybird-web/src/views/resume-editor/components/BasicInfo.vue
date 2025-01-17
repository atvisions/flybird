<template>
  <div class="basic-info">
    <v-form v-model="valid">
      <v-container>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.name"
              label="姓名"
              required
              :rules="[v => !!v || '请输入姓名']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.title"
              label="职位"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.email"
              label="邮箱"
              type="email"
              :rules="[v => !v || /.+@.+\..+/.test(v) || '请输入有效的邮箱']"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field
              v-model="formData.phone"
              label="电话"
              @input="updateConfig"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-textarea
              v-model="formData.summary"
              label="个人简介"
              rows="3"
              @input="updateConfig"
            ></v-textarea>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  config: {
    type: Object,
    default: () => ({
      name: '',
      title: '',
      email: '',
      phone: '',
      summary: ''
    })
  }
})

const emit = defineEmits(['update:config'])

const valid = ref(false)
const formData = ref({ ...props.config })

// 监听配置变化
watch(() => props.config, (newConfig) => {
  formData.value = { ...newConfig }
}, { deep: true })

// 更新配置
const updateConfig = () => {
  emit('update:config', { ...formData.value })
}
</script>

<style scoped>
.basic-info {
  padding: 16px;
}
</style> 