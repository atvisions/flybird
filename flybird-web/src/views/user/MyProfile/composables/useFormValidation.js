// src/views/user/MyProfile/composables/useFormValidation.js
import { validationRules } from '../constants/rules'

export function useFormValidation() {
  const validateForm = async (formRef, formData) => {
    if (!formRef) return { valid: false, errors: [] }
    try {
      // 只验证有值的字段
      const filledFields = {}
      Object.entries(formData).forEach(([key, value]) => {
        if (value && validationRules.basic[key]) {
          filledFields[key] = validationRules.basic[key]
        }
      })

      // 如果没有需要验证的字段，直接返回 true
      if (Object.keys(filledFields).length === 0) {
        return { valid: true, errors: [] }
      }

      // 清除之前的验证结果
      formRef.clearValidate && formRef.clearValidate()

      // 执行验证
      return new Promise((resolve) => {
        formRef.validate((valid, fields) => {
          if (valid) {
            resolve({ valid: true, errors: [] })
          } else {
            // 获取具体的错误信息
            const errors = Object.entries(fields || {}).map(([field, msgs]) => {
              const fieldName = {
                name: '姓名',
                gender: '性别',
                phone: '手机号',
                email: '邮箱',
                location: '所在地',
                birth_date: '生日',
                personal_summary: '个人简介'
              }[field]
              return `${fieldName}: ${msgs[0].message}`
            })
            resolve({ valid: false, errors })
          }
        })
      })
    } catch (error) {
      console.error('表单验证失败:', error)
      return { valid: false, errors: [error.message] }
    }
  }

  return {
    rules: validationRules.basic,
    validateForm
  }
}