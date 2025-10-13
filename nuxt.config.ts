// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    'shadcn-nuxt',
    '@nuxtjs/color-mode',
    'nuxt-icon',
    '@pinia/nuxt',
    '@sidebase/nuxt-auth'
  ],
  auth: {
    baseURL: '/api/auth',
    provider: {
      type: 'authjs',
      origin: process.env.NUXT_NEXTAUTH_URL || 'http://localhost:3000',
      trustHost: false,
      defaultProvider: 'google',
      addDefaultCallbackUrl: true
    },
    sessionRefresh: {
      enablePeriodically: true,
      enableOnWindowFocus: true,
    },
    globalAppMiddleware: false
  },
  pinia: {
    storesDirs: ['./stores/**', './custom-folder/stores/**'],
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
    },
  colorMode: {
    classSuffix: ''
  },
   runtimeConfig: {
    // PRIVATE (SERVER-ONLY) KEYS: Secrets, IDs, and API keys must go here.
    private: {
      GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID,
      GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET,
      NEXTAUTH_SECRET: process.env.NEXTAUTH_SECRET,
    },
    // PUBLIC (CLIENT & SERVER) KEYS: The URL needed for the OAuth redirect fix MUST go here.
    public: {
      // CRITICAL FIX: The full URL (e.g., 'http://localhost:3000') must be public.
      NUXT_NEXTAUTH_URL: process.env.NUXT_NEXTAUTH_URL || 'http://localhost:3000',
      NEXTAUTH_URL: process.env.NEXTAUTH_URL || 'http://localhost:3000'
    }
  }
})
