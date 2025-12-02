<template>
  <div class="bg-farm-login flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10 relative">
    <!-- Overlay for better readability -->
    <div class="absolute inset-0 bg-background/40 backdrop-blur-sm"></div>
    
    <div class="flex w-full max-w-sm flex-col gap-6 relative z-10">
      <a href="#" class="flex items-center gap-2 self-center font-medium">
        <div class="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
          <GalleryVerticalEnd class="size-4" />
        </div>
        <span class="text-lg font-bold">FarmTrack</span>
      </a>
      <LoginForm />
    </div>
  </div>
</template>

<script lang="ts">
export const description = "A login page with a muted background color."
</script>

<script setup lang="ts">
import { GalleryVerticalEnd } from "lucide-vue-next"
import LoginForm from '@/components/LoginForm.vue'

// Disable layout for login page - it should be standalone
definePageMeta({
  layout: false,
})
</script>
