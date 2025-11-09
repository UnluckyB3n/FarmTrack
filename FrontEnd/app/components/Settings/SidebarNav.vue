<script setup lang="ts">
import { cn } from '@/lib/utils'
import { Button } from '~/components/ui/button'

interface Item {
  title: string
  href: string
}

const $route = useRoute()

const sidebarNavItems: Item[] = [
  {
    title: 'Profile',
    href: '/settings',
  },
  {
    title: 'Account',
    href: '/settings/Account',
  },
  {
    title: 'Appearance',
    href: '/settings/Appearance',
  },
  {
    title: 'Notifications',
    href: '/settings/Notifications',
  },
  {
    title: 'Display',
    href: '/settings/Display',
  },
]
</script>

<template>
  <nav class="flex space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1">
    <NuxtLink
      v-for="item in sidebarNavItems"
      :key="item.title"
      :to="item.href"
    >
      <Button
        variant="ghost"
        :class="cn(
          'w-full text-left justify-start',
          $route.path === item.href && 'bg-muted hover:bg-muted',
        )"
      >
        {{ item.title }}
      </Button>
    </NuxtLink>
  </nav>
</template>