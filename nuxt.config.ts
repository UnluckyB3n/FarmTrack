import tailwindcss from '@tailwindcss/vite';

export default defineNuxtConfig({
  // ...
  css: ['~/assets/css/tailwind.css'],
  modules: ['shadcn-nuxt'],
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
  shadcn: {
      /**
       * Prefix for all the imported component
       */
      prefix: '',
      /**
       * Directory that the component lives in.
       * @default "./components/ui"
       */
      componentDir: './components/ui'
    }

})