/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js,vue}",
    "./node_modules/flowbite/**/*.js",
    './node_modules/@headlessui/vue/dist/components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#F5F8FF',
          100: '#E8EFFF',
          200: '#C7D9FF',
          300: '#96B9FF',
          400: '#4585FF',
          500: '#1A56DB',
          600: '#1142B0',
          700: '#0B3285',
          800: '#072159',
          900: '#041333',
          950: '#020A1F',
        }
      }
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('@tailwindcss/forms'),
  ],
}