<template>
  <NuxtLayout name="default">
    <div class="space-y-6">
      <div>
        <h1 class="text-3xl font-bold">Audit Logs</h1>
        <p class="text-muted-foreground mt-2">
          Complete system audit trail and event history
        </p>
      </div>

      <!-- Filters -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Filters</UiCardTitle>
        </UiCardHeader>
        <UiCardContent>
          <div class="grid gap-4 md:grid-cols-4">
            <div class="space-y-2">
              <UiLabel>Event Type</UiLabel>
              <UiSelect v-model="filters.eventType">
                <UiSelectTrigger>
                  <UiSelectValue placeholder="All types" />
                </UiSelectTrigger>
                <UiSelectContent>
                  <UiSelectItem value="all">All types</UiSelectItem>
                  <UiSelectItem value="birth">Birth</UiSelectItem>
                  <UiSelectItem value="vaccination">Vaccination</UiSelectItem>
                  <UiSelectItem value="weighing">Weighing</UiSelectItem>
                  <UiSelectItem value="movement">Movement</UiSelectItem>
                  <UiSelectItem value="health_check">Health Check</UiSelectItem>
                  <UiSelectItem value="treatment">Treatment</UiSelectItem>
                </UiSelectContent>
              </UiSelect>
            </div>

            <div class="space-y-2">
              <UiLabel>Validity</UiLabel>
              <UiSelect v-model="filters.validity">
                <UiSelectTrigger>
                  <UiSelectValue placeholder="All events" />
                </UiSelectTrigger>
                <UiSelectContent>
                  <UiSelectItem value="all">All events</UiSelectItem>
                  <UiSelectItem value="valid">Valid only</UiSelectItem>
                  <UiSelectItem value="anomaly">Anomalies only</UiSelectItem>
                </UiSelectContent>
              </UiSelect>
            </div>

            <div class="space-y-2">
              <UiLabel>Facility</UiLabel>
              <UiSelect v-model="filters.facilityId">
                <UiSelectTrigger>
                  <UiSelectValue placeholder="All facilities" />
                </UiSelectTrigger>
                <UiSelectContent>
                  <UiSelectItem value="all">All facilities</UiSelectItem>
                  <UiSelectItem
                    v-for="facility in facilities"
                    :key="facility.id"
                    :value="facility.id.toString()"
                  >
                    {{ facility.name }}
                  </UiSelectItem>
                </UiSelectContent>
              </UiSelect>
            </div>

            <div class="flex items-end">
              <UiButton @click="loadLogs" class="w-full">
                Apply Filters
              </UiButton>
            </div>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Logs Table -->
      <UiCard>
        <UiCardHeader>
          <div class="flex items-center justify-between">
            <div>
              <UiCardTitle>Event Logs</UiCardTitle>
              <UiCardDescription>{{ total }} total events</UiCardDescription>
            </div>
            <div class="flex gap-2">
              <UiButton variant="outline" @click="exportLogs">
                Export to CSV
              </UiButton>
              <UiButton variant="outline" @click="exportLogsPDF">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
                Export to PDF
              </UiButton>
            </div>
          </div>
        </UiCardHeader>
        <UiCardContent>
          <div v-if="loading" class="flex justify-center py-12">
            <UiSpinner class="h-8 w-8" />
          </div>
          <div v-else-if="logs.length > 0" class="space-y-2">
            <div
              v-for="log in logs"
              :key="log.id"
              class="grid grid-cols-[100px_120px_100px_1fr_150px] gap-4 p-3 border rounded-lg text-sm"
              :class="!log.is_valid ? 'border-destructive/50 bg-destructive/5' : ''"
            >
              <div>
                <UiBadge>{{ log.event_type }}</UiBadge>
              </div>
              <div class="text-muted-foreground">
                Animal #{{ log.animal_id }}
              </div>
              <div class="text-muted-foreground">
                Facility #{{ log.facility_id }}
              </div>
              <div>
                <p v-if="!log.is_valid" class="text-destructive text-xs mb-1">
                  ⚠️ {{ log.anomaly_reason }}
                </p>
                <p class="text-muted-foreground">{{ log.event_metadata || 'No description' }}</p>
              </div>
              <div class="text-muted-foreground text-right">
                {{ formatDate(log.timestamp) }}
              </div>
            </div>
          </div>
          <div v-else class="py-12 text-center text-muted-foreground">
            No logs found
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Pagination -->
      <div v-if="total > limit" class="flex items-center justify-between">
        <p class="text-sm text-muted-foreground">
          Showing {{ skip + 1 }}-{{ Math.min(skip + limit, total) }} of {{ total }}
        </p>
        <div class="flex gap-2">
          <UiButton variant="outline" @click="previousPage" :disabled="skip === 0">
            Previous
          </UiButton>
          <UiButton variant="outline" @click="nextPage" :disabled="skip + limit >= total">
            Next
          </UiButton>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const api = useApi()

const filters = ref({
  eventType: 'all',
  validity: 'all',
  facilityId: 'all'
})

const logs = ref<any[]>([])
const facilities = ref<any[]>([])
const loading = ref(true)
const total = ref(0)
const skip = ref(0)
const limit = ref(20)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadLogs = async () => {
  loading.value = true
  
  const params: any = {
    skip: skip.value,
    limit: limit.value
  }
  
  if (filters.value.eventType !== 'all') {
    params.event_type = filters.value.eventType
  }
  
  if (filters.value.validity === 'valid') {
    params.is_valid = true
  } else if (filters.value.validity === 'anomaly') {
    params.is_valid = false
  }
  
  if (filters.value.facilityId !== 'all') {
    params.facility_id = filters.value.facilityId
  }
  
  const result = await api.getEvents(params)
  
  if (result.data?.events) {
    logs.value = result.data.events
    total.value = result.data.total || logs.value.length
  }
  
  loading.value = false
}

const loadFacilities = async () => {
  const result = await api.getFacilities()
  if (result.data?.facilities) {
    facilities.value = result.data.facilities
  }
}

const previousPage = () => {
  if (skip.value >= limit.value) {
    skip.value -= limit.value
    loadLogs()
  }
}

const nextPage = () => {
  if (skip.value + limit.value < total.value) {
    skip.value += limit.value
    loadLogs()
  }
}

const exportLogs = () => {
  // Create CSV content
  const headers = ['ID', 'Type', 'Animal ID', 'Facility ID', 'Valid', 'Timestamp', 'Metadata', 'Anomaly Reason']
  const rows = logs.value.map(log => [
    log.id,
    log.event_type,
    log.animal_id,
    log.facility_id,
    log.is_valid ? 'Yes' : 'No',
    log.timestamp,
    log.event_metadata || '',
    log.anomaly_reason || ''
  ])
  
  const csv = [headers, ...rows].map(row => row.join(',')).join('\n')
  
  // Download file
  const blob = new Blob([csv], { type: 'text/csv' })
  const url = window.URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `audit-logs-${new Date().toISOString().split('T')[0]}.csv`
  a.click()
  window.URL.revokeObjectURL(url)
}

const exportLogsPDF = () => {
  const token = localStorage.getItem('token')
  
  // Build query params from filters
  const params: any = {}
  if (filters.value.eventType !== 'all') {
    params.event_type = filters.value.eventType
  }
  if (filters.value.validity !== 'all') {
    params.validity = filters.value.validity
  }
  if (filters.value.facilityId !== 'all') {
    params.facility_id = filters.value.facilityId
  }
  
  const url = api.downloadAuditLogsPDF(params)
  
  // Create a temporary link and trigger download
  const link = document.createElement('a')
  link.href = url + `&token=${token}`
  link.download = `audit_logs_${new Date().toISOString().split('T')[0]}.pdf`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  loadFacilities()
  loadLogs()
})
</script>