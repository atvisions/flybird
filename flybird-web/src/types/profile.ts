interface BasicInfo {
  name: string;
  name_en?: string;
  personal_summary: string;
  personal_summary_en?: string;
  // ... 其他字段
}

interface WorkExperience {
  position: string;
  position_en?: string;
  department: string;
  department_en?: string;
  description: string;
  description_en?: string;
  achievements: string;
  achievements_en?: string;
  // ... 其他字段
}

interface JobIntention {
  industries: string;
  industries_en?: string;
  expected_city: string;
  expected_city_en?: string;
  // ... 其他字段
} 