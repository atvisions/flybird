// ... existing code ...
// 处理工作经历字段
if (label === '公司名称' || label === '职位名称' || 
    label === '所在部门' || label === '工作时间' || 
    label === '工作描述' || label === '工作成就' ||
    label === '技术栈') {
  console.log('【LoadingScreen】处理工作经历字段:', {
    label,
    key,
    fieldType,
    dataPath: `work_experience[0].${key}`
  })
  
  // 根据字段类型设置合适的类型
  if (label === '工作描述' || label === '工作成就' || label === '技术栈') {
    fieldType = 'textarea'
  }
  
  return {
    key,
    label,
    type: fieldType,
    dataPath: `work_experience[0].${key}`
  }
}
// ... existing code ... 