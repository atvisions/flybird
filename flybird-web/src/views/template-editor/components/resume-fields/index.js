import ResumeField from './ResumeField.vue'
import BasicInfo from './BasicInfo.vue'
import JobIntention from './JobIntention.vue'

export {
  ResumeField,
  BasicInfo,
  JobIntention
}

// 注册所有组件
export default {
  install(app) {
    app.component('ResumeField', ResumeField)
    app.component('ResumeBasicInfo', BasicInfo)
    app.component('JobIntention', JobIntention)
  }
} 