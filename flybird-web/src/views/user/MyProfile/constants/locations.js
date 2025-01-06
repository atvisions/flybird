// src/constants/locations.js
export const locationOptions = [
    {
      value: '北京',
      label: '北京',
      children: [
        {
          value: '北京市',
          label: '北京市',
          children: [
            { value: '朝阳区', label: '朝阳区' },
            { value: '海淀区', label: '海淀区' },
            { value: '西城区', label: '西城区' },
            { value: '东城区', label: '东城区' },
            // ... 其他区
          ]
        }
      ]
    },
    {
      value: '上海',
      label: '上海',
      children: [
        {
          value: '上海市',
          label: '上海市',
          children: [
            { value: '浦东新区', label: '浦东新区' },
            { value: '徐汇区', label: '徐汇区' },
            { value: '黄浦区', label: '黄浦区' },
            // ... 其他区
          ]
        }
      ]
    },
    // ... 其他省市
  ]