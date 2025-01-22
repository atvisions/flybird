import ResumeField from './ResumeField.vue'
import BasicInfo from './BasicInfo.vue'

export {
  ResumeField,
  BasicInfo
}

// 注册所有组件
export default {
  install(app) {
    app.component('ResumeField', ResumeField)
    app.component('ResumeBasicInfo', BasicInfo)
  }
} 