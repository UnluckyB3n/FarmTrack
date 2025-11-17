<template>
  <div class="bg-muted flex min-h-svh flex-col items-center justify-center gap-6 p-6 md:p-10">
    <div class="flex w-full max-w-sm flex-col gap-6">
      <a href="#" class="flex items-center gap-2 self-center font-medium">
        <div class="bg-primary text-primary-foreground flex size-6 items-center justify-center rounded-md">
          <GalleryVerticalEnd class="size-4" />
        </div>
        FarmTrack
      </a>
      <RegisterForm />
    </div>
  </div>
</template>

<script lang="ts">
export const description = "A registration page with a muted background color."
</script>

<script setup lang="ts">
import { GalleryVerticalEnd } from "lucide-vue-next"
import RegisterForm from '@/components/RegisterForm.vue'

// Disable layout for register page - it should be standalone
definePageMeta({
  layout: false,
})
</script>