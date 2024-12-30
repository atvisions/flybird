// 这里是简化版的示例，实际数据需要完整的中国省市区数据
export const areaData = [
    {
      code: '110000',
      name: '北京市',
      children: [
        {
          code: '110100',
          name: '北京市',
          children: [
            {
              code: '110101',
              name: '东城区'
            },
            // ... 其他区县
          ]
        }
      ]
    },
    // ... 其他省份
  ]