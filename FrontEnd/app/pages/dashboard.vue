<template>
  <NuxtLayout name="default">
    <div v-if="loading" class="flex justify-center items-center min-h-screen">
      <div>Loading...</div>
    </div>
    <div v-else class="space-y-6">
      <!-- Stats Grid -->
      <div v-if="overview" class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <UiCard>
          <UiCardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <UiCardTitle class="text-sm font-medium">Total Animals</UiCardTitle>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="text-muted-foreground"
            >
              <circle cx="11" cy="4" r="2" />
              <circle cx="18" cy="8" r="2" />
              <circle cx="20" cy="16" r="2" />
              <path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z" />
            </svg>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ overview.totals.animals }}</div>
            <p class="text-xs text-muted-foreground">Tracked livestock</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <UiCardTitle class="text-sm font-medium">Facilities</UiCardTitle>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="text-muted-foreground"
            >
              <path d="M6 22V4a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v18Z" />
              <path d="M6 12H4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h2" />
            </svg>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ overview.totals.facilities }}</div>
            <p class="text-xs text-muted-foreground">Active locations</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <UiCardTitle class="text-sm font-medium">Total Events</UiCardTitle>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="text-muted-foreground"
            >
              <path d="M8 2v4" />
              <path d="M16 2v4" />
              <rect width="18" height="18" x="3" y="4" rx="2" />
              <path d="M3 10h18" />
            </svg>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ overview.totals.events }}</div>
            <p class="text-xs text-muted-foreground">
              +{{ overview.recent_activity.events_last_7_days }} last 7 days
            </p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <UiCardTitle class="text-sm font-medium">Anomalies</UiCardTitle>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="text-destructive"
            >
              <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" />
              <path d="M12 9v4" />
              <path d="M12 17h.01" />
            </svg>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold text-destructive">{{ overview.anomalies.total }}</div>
            <p class="text-xs text-muted-foreground">{{ overview.anomalies.rate }}% anomaly rate</p>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Charts Row -->
      <div class="grid gap-4 md:grid-cols-2">
        <!-- Species Distribution -->
        <UiCard>
          <UiCardHeader>
            <UiCardTitle>Species Distribution</UiCardTitle>
            <UiCardDescription>Animals by species</UiCardDescription>
          </UiCardHeader>
          <UiCardContent v-if="distribution">
            <div class="space-y-3">
              <div v-for="item in distribution.distribution" :key="item.species" class="flex items-center gap-2">
                <div class="flex-1">
                  <div class="flex items-center justify-between mb-1">
                    <span class="text-sm font-medium">{{ item.species }}</span>
                    <span class="text-sm text-muted-foreground">{{ item.count }} ({{ item.percentage }}%)</span>
                  </div>
                  <UiProgress :model-value="item.percentage" class="h-2" />
                </div>
              </div>
            </div>
          </UiCardContent>
        </UiCard>

        <!-- Top Facilities -->
        <UiCard>
          <UiCardHeader>
            <UiCardTitle>Top Facilities</UiCardTitle>
            <UiCardDescription>By animal count</UiCardDescription>
          </UiCardHeader>
          <UiCardContent v-if="topFacilities">
            <div class="space-y-4">
              <div
                v-for="facility in topFacilities.facilities"
                :key="facility.id"
                class="flex items-center justify-between"
              >
                <div class="space-y-1">
                  <p class="text-sm font-medium">{{ facility.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ facility.location }} • {{ facility.facility_type }}</p>
                </div>
                <UiBadge variant="secondary">{{ facility.animal_count }} animals</UiBadge>
              </div>
            </div>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Recent Events -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Recent Events</UiCardTitle>
          <UiCardDescription>Latest traceability events</UiCardDescription>
        </UiCardHeader>
        <UiCardContent v-if="recentEvents">
          <div class="space-y-3">
            <div
              v-for="event in recentEvents.events"
              :key="event.id"
              class="flex items-center justify-between border-b pb-3 last:border-0"
            >
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <UiBadge :variant="event.is_valid ? 'default' : 'destructive'">
                    {{ event.event_type }}
                  </UiBadge>
                  <span class="text-sm font-medium">
                    {{ event.animal?.name }} ({{ event.animal?.tag_id }})
                  </span>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ event.facility?.name }} • {{ formatDate(event.timestamp) }}
                </p>
              </div>
              <UiButton variant="ghost" size="sm" @click="navigateTo(`/events`)">
                View
              </UiButton>
            </div>
          </div>
        </UiCardContent>
      </UiCard>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const api = useApi()
const loading = ref(false)

const { data: overview } = await useAsyncData('dashboard-overview', async () => {
  const result = await api.getDashboardOverview()
  return result.data
})

const { data: distribution } = await useAsyncData('species-distribution', async () => {
  const result = await api.getSpeciesDistribution()
  return result.data
})

const { data: topFacilities } = await useAsyncData('top-facilities', async () => {
  const result = await api.getTopFacilities(5)
  return result.data
})

const { data: recentEvents } = await useAsyncData('recent-events', async () => {
  const result = await api.getRecentEvents(8)
  return result.data
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}
</script>
