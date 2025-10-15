<template>
  <SidebarProvider>
    <Sidebar />
    <main>
      <SidebarTrigger />
      <NuxtPage />
    </main>
  </SidebarProvider>
</template>

<script setup lang="ts">
import Sidebar from '~/components/ui/sidebar/Sidebar.vue';
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
</script>