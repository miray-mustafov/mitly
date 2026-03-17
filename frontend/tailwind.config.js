/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Bitly-inspired orange and dark theme
        primary: {
          light: '#ff8a50',
          DEFAULT: '#ee6123',
          dark: '#b44b1c',
        },
        secondary: '#2a2e35',
      },
    },
  },
  plugins: [],
}
