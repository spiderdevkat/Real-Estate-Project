/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['Georgia', 'serif'],
        body: ['DM Sans', 'sans-serif'],
        mono: ['DM Mono', 'monospace'],
      },
      colors: {
        teal: {
          50: '#E1F5EE', 100: '#9FE1CB', 200: '#5DCAA5',
          400: '#1D9E75', 600: '#0F6E56', 800: '#085041', 900: '#04342C',
        },
        coral: {
          50: '#FAECE7', 100: '#F5C4B3', 400: '#D85A30',
          600: '#993C1D', 800: '#712B13',
        },
        ink: {
          50: '#F7F6F3', 100: '#EDEBE4', 200: '#D3D1C7',
          400: '#888780', 600: '#5F5E5A', 800: '#2C2C2A', 900: '#1A1A18',
        },
      },
    },
  },
  plugins: [],
}
