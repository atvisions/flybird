// src/views/user/MyProfile/constants/rules.js
export const validationRules = {
    basic: {
      name: [
        { required: false, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
      ],
      gender: [
        { required: false, message: '请选择性别', trigger: 'change' }
      ],
      phone: [
        { required: false, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      email: [
        { required: false, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      location: [
        { required: false, message: '请输入所在地', trigger: 'blur' }
      ],
      birth_date: [
        { required: false, message: '请选择生日', trigger: 'change' }
      ],
      personal_summary: [
        { required: false, message: '请输入个人简介', trigger: 'blur' },
        { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
      ]
    },
    job_intention: {
      position: [
        { required: false, message: '请输入期望职位', trigger: 'blur' },
        { max: 50, message: '职位名称不能超过50个字符', trigger: 'blur' }
      ],
      city: [
        { required: false, message: '请选择期望城市', trigger: 'change' },
        { 
          validator: (rule, value, callback) => {
            if (value && (!Array.isArray(value) || value.length < 2)) {
              callback(new Error('请选择完整的城市信息'))
            } else {
              callback()
            }
          }, 
          trigger: 'change' 
        }
      ],
      salary_min: [
        { 
          validator: (rule, value, callback) => {
            if (value && (!Number.isInteger(value) || value < 0)) {
              callback(new Error('请输入有效的最低薪资'))
            } else {
              callback()
            }
          },
          trigger: 'change'
        }
      ],
      salary_max: [
        {
          validator: (rule, value, callback, source) => {
            const minSalary = source.salary_min
            if (value && (!Number.isInteger(value) || value < 0)) {
              callback(new Error('请输入有效的最高薪资'))
            } else if (minSalary && value && value < minSalary) {
              callback(new Error('最高薪资不能低于最低薪资'))
            } else {
              callback()
            }
          },
          trigger: 'change'
        }
      ],
      availability: [
        { required: false, message: '请选择到岗时间', trigger: 'change' }
      ],
      job_type: [
        { required: false, message: '请选择工作类型', trigger: 'change' }
      ]
    }
  }