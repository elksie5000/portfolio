/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-base': '#F0F4EF',   // Pale mint-cream
        'text-main': '#1B3A2B', // Deep forest green
        'brand-sage': '#4A7C59', // Borders, secondary text
        'brand-lime': '#D8F1A0', // Buttons, accents
      },
      fontFamily: {
        sans: ['Inter', 'DM Sans', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
