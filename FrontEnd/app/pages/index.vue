<template>
  <div class="flex min-h-screen items-center justify-center">
    <div class="text-center">
      <h1 class="text-2xl font-bold mb-2">FarmTrack</h1>
      <p class="text-muted-foreground">Redirecting...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false,
})

// Redirect to login or dashboard based on auth status
onMounted(() => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    navigateTo('/dashboard')
  } else {
    navigateTo('/login')
  }
})
</script>
