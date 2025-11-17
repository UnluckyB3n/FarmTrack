<template>
  <NuxtLayout name="default">
    <div class="space-y-6">
      <!-- Header -->
      <div>
        <h1 class="text-3xl font-bold">Regulator Dashboard</h1>
        <p class="text-muted-foreground mt-2">
          Compliance monitoring, anomaly detection, and audit trails
        </p>
      </div>

      <!-- Stats Overview -->
      <div class="grid gap-4 md:grid-cols-4">
        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Total Animals</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ stats.totalAnimals }}</div>
            <p class="text-xs text-muted-foreground">Across all facilities</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Total Events</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ stats.totalEvents }}</div>
            <p class="text-xs text-muted-foreground">Recorded activities</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium text-destructive">Anomalies</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold text-destructive">{{ stats.anomalies }}</div>
            <p class="text-xs text-muted-foreground">Require attention</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Facilities</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ stats.totalFacilities }}</div>
            <p class="text-xs text-muted-foreground">Registered locations</p>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Anomalies & Compliance -->
      <div class="grid gap-6 md:grid-cols-2">
        <!-- Recent Anomalies -->
        <UiCard>
          <UiCardHeader>
            <div class="flex items-center justify-between">
              <UiCardTitle>Recent Anomalies</UiCardTitle>
              <UiButton variant="ghost" size="sm" @click="router.push('/events?filter=anomalies')">
                View All
              </UiButton>
            </div>
            <UiCardDescription>Events flagged by plausibility validation</UiCardDescription>
          </UiCardHeader>
          <UiCardContent>
            <div v-if="loadingAnomalies" class="flex justify-center py-8">
              <UiSpinner />
            </div>
            <div v-else-if="anomalies.length > 0" class="space-y-3">
              <div
                v-for="anomaly in anomalies"
                :key="anomaly.id"
                class="flex items-start gap-3 p-3 border rounded-lg border-destructive/50 bg-destructive/5"
              >
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <UiBadge variant="destructive">{{ anomaly.event_type }}</UiBadge>
                    <span class="text-xs text-muted-foreground">
                      Animal #{{ anomaly.animal_id }}
                    </span>
                  </div>
                  <p class="text-sm font-medium">{{ anomaly.anomaly_reason }}</p>
                  <p class="text-xs text-muted-foreground mt-1">
                    {{ formatDate(anomaly.timestamp) }}
                  </p>
                </div>
              </div>
            </div>
            <div v-else class="py-8 text-center text-muted-foreground text-sm">
              No anomalies detected
            </div>
          </UiCardContent>
        </UiCard>

        <!-- Facility Compliance -->
        <UiCard>
          <UiCardHeader>
            <UiCardTitle>Facility Compliance</UiCardTitle>
            <UiCardDescription>Recent activity by facility type</UiCardDescription>
          </UiCardHeader>
          <UiCardContent>
            <div v-if="loadingFacilities" class="flex justify-center py-8">
              <UiSpinner />
            </div>
            <div v-else class="space-y-4">
              <div
                v-for="facility in topFacilities"
                :key="facility.id"
                class="flex items-center justify-between p-3 border rounded-lg"
              >
                <div>
                  <p class="font-medium text-sm">{{ facility.name }}</p>
                  <p class="text-xs text-muted-foreground">{{ facility.facility_type }}</p>
                </div>
                <div class="text-right">
                  <p class="font-semibold">{{ facility.animal_count || 0 }}</p>
                  <p class="text-xs text-muted-foreground">animals</p>
                </div>
              </div>
            </div>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Recent Events Timeline -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Recent Activity</UiCardTitle>
          <UiCardDescription>Latest events across all facilities</UiCardDescription>
        </UiCardHeader>
        <UiCardContent>
          <div v-if="loadingEvents" class="flex justify-center py-8">
            <UiSpinner />
          </div>
          <div v-else-if="recentEvents.length > 0" class="space-y-3">
            <div
              v-for="event in recentEvents"
              :key="event.id"
              class="flex items-start gap-4 p-3 border rounded-lg"
              :class="!event.is_valid ? 'border-destructive/50 bg-destructive/5' : ''"
            >
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <UiBadge>{{ event.event_type }}</UiBadge>
                  <UiBadge v-if="!event.is_valid" variant="destructive">Anomaly</UiBadge>
                  <span class="text-xs text-muted-foreground">
                    Animal #{{ event.animal_id }}
                  </span>
                </div>
                <p class="text-sm">{{ event.event_metadata || 'No description' }}</p>
                <p class="text-xs text-muted-foreground mt-1">
                  {{ formatDate(event.timestamp) }} • Facility #{{ event.facility_id }}
                </p>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-muted-foreground text-sm">
            No recent events
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Audit Tools -->
      <div class="grid gap-4 md:grid-cols-3">
        <UiCard class="hover:bg-muted/50 cursor-pointer" @click="router.push('/regulator/trace')">
          <UiCardHeader>
            <UiCardTitle class="text-base">Trace Animal</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <p class="text-sm text-muted-foreground">
              Track complete lifecycle and movement history
            </p>
          </UiCardContent>
        </UiCard>

        <UiCard class="hover:bg-muted/50 cursor-pointer" @click="router.push('/regulator/logs')">
          <UiCardHeader>
            <UiCardTitle class="text-base">Audit Logs</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <p class="text-sm text-muted-foreground">
              View complete system audit trail
            </p>
          </UiCardContent>
        </UiCard>

        <UiCard class="hover:bg-muted/50 cursor-pointer" @click="exportReport">
          <UiCardHeader>
            <UiCardTitle class="text-base">Export Report</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <p class="text-sm text-muted-foreground">
              Generate compliance report (PDF)
            </p>
          </UiCardContent>
        </UiCard>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const router = useRouter()
const api = useApi()

const stats = ref({
  totalAnimals: 0,
  totalEvents: 0,
  anomalies: 0,
  totalFacilities: 0
})

const anomalies = ref<any[]>([])
const loadingAnomalies = ref(true)

const topFacilities = ref<any[]>([])
const loadingFacilities = ref(true)

const recentEvents = ref<any[]>([])
const loadingEvents = ref(true)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadStats = async () => {
  const animalStats = await api.getAnimalStats()
  const eventStats = await api.getEventStats()
  const facilities = await api.getFacilities()
  const anomaliesResult = await api.getAnomalies({ limit: 10 })

  if (animalStats.data?.total) {
    stats.value.totalAnimals = animalStats.data.total
  }

  if (eventStats.data?.total) {
    stats.value.totalEvents = eventStats.data.total
  }

  if (eventStats.data?.anomalies) {
    stats.value.anomalies = eventStats.data.anomalies
  }

  if (facilities.data?.facilities) {
    stats.value.totalFacilities = facilities.data.facilities.length
  }
}

const loadAnomalies = async () => {
  loadingAnomalies.value = true
  const result = await api.getAnomalies({ limit: 5 })
  if (result.data?.anomalies) {
    anomalies.value = result.data.anomalies
  }
  loadingAnomalies.value = false
}

const loadFacilities = async () => {
  loadingFacilities.value = true
  const result = await api.getFacilities({ limit: 5 })
  if (result.data?.facilities) {
    topFacilities.value = result.data.facilities
  }
  loadingFacilities.value = false
}

const loadRecentEvents = async () => {
  loadingEvents.value = true
  const result = await api.getRecentEvents(10)
  if (result.data?.events) {
    recentEvents.value = result.data.events
  }
  loadingEvents.value = false
}

const exportReport = () => {
  const token = localStorage.getItem('token')
  const url = api.downloadCompliancePDF()
  
  // Create a temporary link and trigger download
  const link = document.createElement('a')
  link.href = url + `?token=${token}`
  link.download = `compliance_report_${new Date().toISOString().split('T')[0]}.pdf`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  loadStats()
  loadAnomalies()
  loadFacilities()
  loadRecentEvents()
})
</script>