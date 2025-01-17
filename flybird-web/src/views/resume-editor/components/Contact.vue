<template>
  <div class="contact">
    <v-container>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.phone"
            label="手机号码"
            :rules="[v => !v || /^1[3-9]\d{9}$/.test(v) || '请输入有效的手机号码']"
            @input="updateConfig"
          ></v-text-field>
        </v-col>
        
        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.email"
            label="电子邮箱"
            type="email"
            :rules="[v => !v || /.+@.+\..+/.test(v) || '请输入有效的邮箱地址']"
            @input="updateConfig"
          ></v-text-field>
        </v-col>
        
        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.wechat"
            label="微信号"
            @input="updateConfig"
          ></v-text-field>
        </v-col>
        
        <v-col cols="12" md="6">
          <v-text-field
            v-model="formData.location"
            label="所在地"
            @input="updateConfig"
          ></v-text-field>
        </v-col>
      </v-row>

      <!-- 社交账号 -->
      <div class="mt-4">
        <div class="d-flex align-center mb-4">
          <h3 class="text-h6">社交账号</h3>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            variant="text"
            prepend-icon="mdi-plus"
            @click="addSocialLink"
          >
            添加账号
          </v-btn>
        </div>

        <div v-for="(social, index) in formData.socials" :key="index" class="social-item">
          <v-row align="center">
            <v-col cols="12" md="4">
              <v-select
                v-model="social.platform"
                :items="socialPlatforms"
                label="平台"
                @update:modelValue="updateConfig"
              ></v-select>
            </v-col>
            
            <v-col cols="12" md="7">
              <v-text-field
                v-model="social.link"
                :label="social.platform ? `${social.platform}链接` : '链接'"
                @input="updateConfig"
              ></v-text-field>
            </v-col>
            
            <v-col cols="12" md="1" class="d-flex justify-end">
              <v-btn
                icon="mdi-delete"
                size="small"
                color="error"
                variant="text"
                @click="removeSocialLink(index)"
              ></v-btn>
            </v-col>
          </v-row>
        </div>
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
      phone: '',
      email: '',
      wechat: '',
      location: '',
      socials: []
    })
  }
})

const emit = defineEmits(['update:config'])

const formData = ref({ ...props.config })

const socialPlatforms = [
  'GitHub',
  '领英',
  '知乎',
  '掘金',
  'CSDN',
  '个人网站',
  '其他'
]

// 监听配置变化
watch(() => props.config, (newConfig) => {
  formData.value = { ...newConfig }
}, { deep: true })

// 添加社交账号
const addSocialLink = () => {
  if (!formData.value.socials) {
    formData.value.socials = []
  }
  formData.value.socials.push({
    platform: '',
    link: ''
  })
  updateConfig()
}

// 移除社交账号
const removeSocialLink = (index) => {
  formData.value.socials.splice(index, 1)
  updateConfig()
}

// 更新配置
const updateConfig = () => {
  emit('update:config', { ...formData.value })
}
</script>

<style scoped>
.contact {
  padding: 16px;
}

.social-item {
  margin-bottom: 16px;
  padding: 16px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 4px;
}
</style> 