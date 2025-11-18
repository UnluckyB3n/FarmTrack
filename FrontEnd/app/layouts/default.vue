<template>
  <div class="min-h-screen bg-background">
    <!-- Sidebar -->
    <aside
      class="fixed left-0 top-0 z-40 h-screen w-64 border-r bg-card transition-transform"
    >
      <div class="flex h-full flex-col">
        <!-- Logo -->
        <div class="flex h-16 items-center border-b px-6">
          <h1 class="text-2xl font-bold text-primary">🚜 FarmTrack</h1>
        </div>

        <!-- Navigation -->
        <nav class="flex-1 space-y-1 p-4">
          <NuxtLink
            v-for="item in filteredNavItems"
            :key="item.id"
            :to="item.to"
            class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground"
            active-class="bg-accent text-accent-foreground"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              v-html="item.icon"
            />
            {{ item.label }}
          </NuxtLink>
        </nav>

        <!-- User Section -->
        <div class="border-t p-4">
          <UiDropdownMenu>
            <UiDropdownMenuTrigger as-child>
              <button class="flex w-full items-center gap-3 rounded-lg px-2 py-2 transition-colors hover:bg-accent">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground font-semibold">
                  {{ userInitials }}
                </div>
                <div class="flex-1 text-left">
                  <p class="text-sm font-medium">{{ displayName }}</p>
                  <p class="text-xs text-muted-foreground">{{ userRole }}</p>
                </div>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="m6 9 6 6 6-6" />
                </svg>
              </button>
            </UiDropdownMenuTrigger>
            <UiDropdownMenuContent class="w-56" align="end">
              <UiDropdownMenuLabel>
                <div class="flex flex-col space-y-1">
                  <p class="text-sm font-medium">{{ displayName }}</p>
                  <p class="text-xs text-muted-foreground">{{ userRole }}</p>
                </div>
              </UiDropdownMenuLabel>
              <UiDropdownMenuSeparator />
              <UiDropdownMenuItem @click="navigateTo('/settings')">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="mr-2"
                >
                  <path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" />
                  <circle cx="12" cy="12" r="3" />
                </svg>
                Settings
              </UiDropdownMenuItem>
              <UiDropdownMenuSeparator />
              <UiDropdownMenuItem @click="handleSignOut" class="text-destructive focus:text-destructive">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  class="mr-2"
                >
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                  <polyline points="16 17 21 12 16 7" />
                  <line x1="21" x2="9" y1="12" y2="12" />
                </svg>
                Sign Out
              </UiDropdownMenuItem>
            </UiDropdownMenuContent>
          </UiDropdownMenu>
        </div>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="ml-64">
      <!-- Page Content -->
      <main class="p-6">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const auth = useAuthManagement()

// Define all available navigation items
const allNavItems = [
  {
    id: 'dashboard',
    to: '/dashboard',
    label: 'Dashboard',
    icon: '<rect width="7" height="9" x="3" y="3" rx="1" /><rect width="7" height="5" x="14" y="3" rx="1" /><rect width="7" height="9" x="14" y="12" rx="1" /><rect width="7" height="5" x="3" y="16" rx="1" />'
  },
  {
    id: 'animals',
    to: '/animals',
    label: 'Animals',
    icon: '<circle cx="11" cy="4" r="2" /><circle cx="18" cy="8" r="2" /><circle cx="20" cy="16" r="2" /><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z" />'
  },
  {
    id: 'facilities',
    to: '/facilities',
    label: 'Facilities',
    icon: '<path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z" /><path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2" /><path d="M18 9h2a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2h-2" /><path d="M10 6h4" /><path d="M10 10h4" /><path d="M10 14h4" /><path d="M10 18h4" />'
  },
  {
    id: 'events',
    to: '/events',
    label: 'Events',
    icon: '<path d="M8 2v4" /><path d="M16 2v4" /><rect width="18" height="18" x="3" y="4" rx="2" /><path d="M3 10h18" />'
  },
  {
    id: 'reports',
    to: '/anomalies',
    label: 'Reports',
    icon: '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" /><path d="M12 9v4" /><path d="M12 17h.01" />'
  },
  {
    id: 'api-docs',
    to: '/api-docs',
    label: 'API Docs',
    icon: '<path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1H6.5a1 1 0 0 1 0-5H20" /><path d="m8 13 4-7 4 7" /><path d="M9.1 11h5.7" />'
  },
  {
    id: 'settings',
    to: '/settings',
    label: 'Settings',
    icon: '<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z" /><circle cx="12" cy="12" r="3" />'
  }
]

// Load visible nav items from localStorage
const visibleNavItems = ref<string[]>([])

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/dashboard': 'Dashboard',
    '/animals': 'Animals',
    '/facilities': 'Facilities',
    '/api-docs': 'API Documentation',
    '/events': 'Events',
    '/anomalies': 'Anomalies',
    '/settings': 'Settings',
  }
  
  // Check if current path starts with any title path
  const matchedKey = Object.keys(titles).find(key => route.path.startsWith(key))
  return matchedKey ? titles[matchedKey] : 'FarmTrack'
})

// Filter nav items based on display settings
const filteredNavItems = computed(() => {
  if (visibleNavItems.value.length === 0) {
    return allNavItems // Show all if no preferences saved
  }
  return allNavItems.filter(item => visibleNavItems.value.includes(item.id))
})

const displayName = ref('User')
const userRole = ref('Farmer')
const userInitials = ref('U')

onMounted(() => {
  // Load display settings from localStorage
  const saved = localStorage.getItem('sidebar-display-items')
  if (saved) {
    try {
      visibleNavItems.value = JSON.parse(saved)
    } catch (e) {
      console.error('Error parsing display settings:', e)
      visibleNavItems.value = []
    }
  }
  
  const username = auth.getUsername()
  if (username) {
    displayName.value = username
    // Generate initials from username
    const parts = username.split('_')
    if (parts.length > 1) {
      userInitials.value = parts.map((p: string) => p?.[0]?.toUpperCase() || '').join('')
    } else {
      userInitials.value = username.substring(0, 2).toUpperCase()
    }
  }
})

const handleSignOut = async () => {
  console.log('Sign out button clicked')
  await auth.signOut()
}
</script>
