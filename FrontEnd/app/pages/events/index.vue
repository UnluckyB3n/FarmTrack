<template>
  <NuxtLayout name="default">
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div class="space-y-1">
          <h1 class="text-3xl font-bold tracking-tight">Events</h1>
          <p class="text-muted-foreground">
            Track and manage all livestock traceability events across your facilities
          </p>
        </div>
        <UiButton @click="openCreateDialog" size="lg" class="shadow-sm">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            class="mr-2"
          >
            <path d="M5 12h14" />
            <path d="M12 5v14" />
          </svg>
          Record Event
        </UiButton>
      </div>

      <!-- Stats Overview -->
      <div class="grid gap-4 md:grid-cols-3">
        <UiCard>
          <UiCardContent class="pt-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-muted-foreground">Total Events</p>
                <p class="text-2xl font-bold">{{ total }}</p>
              </div>
              <div class="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-blue-600 dark:text-blue-400">
                  <path d="M8 2v4" /><path d="M16 2v4" /><rect width="18" height="18" x="3" y="4" rx="2" /><path d="M3 10h18" />
                </svg>
              </div>
            </div>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardContent class="pt-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-muted-foreground">Valid Events</p>
                <p class="text-2xl font-bold text-green-600">{{ validCount }}</p>
              </div>
              <div class="h-12 w-12 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-green-600 dark:text-green-400">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" /><path d="m9 11 3 3L22 4" />
                </svg>
              </div>
            </div>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardContent class="pt-6">
            <div class="flex items-center justify-between">
              <div>
                <p class="text-sm font-medium text-muted-foreground">Anomalies</p>
                <p class="text-2xl font-bold text-destructive">{{ anomalyCount }}</p>
              </div>
              <div class="h-12 w-12 rounded-full bg-red-100 dark:bg-red-900 flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-red-600 dark:text-red-400">
                  <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" /><path d="M12 9v4" /><path d="M12 17h.01" />
                </svg>
              </div>
            </div>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Filters -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Filter Events</UiCardTitle>
          <UiCardDescription>Narrow down events by type and validation status</UiCardDescription>
        </UiCardHeader>
        <UiCardContent>
          <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
            <div class="flex-1 space-y-2">
              <UiLabel>Event Type</UiLabel>
              <UiSelect v-model="filterType">
                <UiSelectTrigger>
                  <UiSelectValue placeholder="Select event type" />
                </UiSelectTrigger>
                <UiSelectContent>
                  <UiSelectItem value="all">
                    <div class="flex items-center gap-2">
                      <span>All Types</span>
                    </div>
                  </UiSelectItem>
                  <UiSelectItem value="birth">🐣 Birth</UiSelectItem>
                  <UiSelectItem value="vaccination">💉 Vaccination</UiSelectItem>
                  <UiSelectItem value="weighing">⚖️ Weighing</UiSelectItem>
                  <UiSelectItem value="movement">🚚 Movement</UiSelectItem>
                  <UiSelectItem value="health_check">🏥 Health Check</UiSelectItem>
                  <UiSelectItem value="treatment">💊 Treatment</UiSelectItem>
                  <UiSelectItem value="feeding">🌾 Feeding</UiSelectItem>
                </UiSelectContent>
              </UiSelect>
            </div>

            <div class="flex-1 space-y-2">
              <UiLabel>Validation Status</UiLabel>
              <UiSelect v-model="filterValid">
                <UiSelectTrigger>
                  <UiSelectValue placeholder="Select validation status" />
                </UiSelectTrigger>
                <UiSelectContent>
                  <UiSelectItem value="all">All Events</UiSelectItem>
                  <UiSelectItem value="valid">✅ Valid Only</UiSelectItem>
                  <UiSelectItem value="invalid">⚠️ Anomalies Only</UiSelectItem>
                </UiSelectContent>
              </UiSelect>
            </div>

            <UiButton @click="applyFilters" class="w-full sm:w-auto">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mr-2">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
              </svg>
              Apply Filters
            </UiButton>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Events List -->
      <UiCard>
        <UiCardHeader>
          <div class="flex items-center justify-between">
            <div>
              <UiCardTitle>Event History</UiCardTitle>
              <UiCardDescription>
                {{ events.length > 0 ? `Showing ${(currentPage - 1) * pageSize + 1}-${Math.min(currentPage * pageSize, total)} of ${total} events` : 'No events to display' }}
              </UiCardDescription>
            </div>
          </div>
        </UiCardHeader>
        <UiCardContent>
          <div v-if="loading" class="flex flex-col items-center justify-center py-12">
            <UiSpinner class="h-8 w-8 mb-4" />
            <p class="text-sm text-muted-foreground">Loading events...</p>
          </div>
          <div v-else-if="events && events.length > 0" class="space-y-3">
            <div
              v-for="event in events"
              :key="event.id"
              class="group relative flex items-start gap-4 rounded-lg border p-4 transition-all hover:border-primary hover:shadow-md"
              :class="!event.is_valid ? 'border-destructive/50 bg-destructive/5' : 'hover:bg-muted/50'"
            >
              <!-- Event Icon -->
              <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-lg"
                   :class="event.is_valid ? 'bg-primary/10' : 'bg-destructive/10'">
                {{ getEventIcon(event.event_type) }}
              </div>

              <!-- Event Content -->
              <div class="flex-1 space-y-2">
                <div class="flex flex-wrap items-center gap-2">
                  <UiBadge :variant="event.is_valid ? 'default' : 'destructive'" class="text-xs">
                    {{ formatEventType(event.event_type) }}
                  </UiBadge>
                  <span class="text-sm font-semibold">Animal #{{ event.animal_id }}</span>
                  <span v-if="!event.is_valid" class="text-xs font-medium text-destructive flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" />
                      <path d="M12 9v4" /><path d="M12 17h.01" />
                    </svg>
                    {{ event.anomaly_reason }}
                  </span>
                </div>
                
                <div class="flex flex-wrap items-center gap-3 text-xs text-muted-foreground">
                  <span class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" /><circle cx="12" cy="10" r="3" />
                    </svg>
                    Facility #{{ event.facility_id }}
                  </span>
                  <span class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" />
                    </svg>
                    {{ formatDate(event.timestamp) }}
                  </span>
                  <span v-if="event.metadata" class="flex items-center gap-1">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
                      <path d="M14 2v6h6" />
                    </svg>
                    {{ event.metadata }}
                  </span>
                </div>
              </div>

              <!-- Action Button -->
              <div class="flex shrink-0 items-center">
                <UiButton variant="ghost" size="sm" class="opacity-0 group-hover:opacity-100 transition-opacity">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mr-2">
                    <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" /><circle cx="12" cy="12" r="3" />
                  </svg>
                  View
                </UiButton>
              </div>
            </div>

            <!-- Pagination -->
            <div class="mt-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between pt-4 border-t">
              <p class="text-sm text-muted-foreground">
                Page {{ currentPage }} of {{ Math.ceil(total / pageSize) }}
              </p>
              <div class="flex gap-2">
                <UiButton
                  variant="outline"
                  size="sm"
                  :disabled="currentPage === 1"
                  @click="changePage(currentPage - 1)"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mr-1">
                    <path d="m15 18-6-6 6-6" />
                  </svg>
                  Previous
                </UiButton>
                <UiButton
                  variant="outline"
                  size="sm"
                  :disabled="currentPage * pageSize >= total"
                  @click="changePage(currentPage + 1)"
                >
                  Next
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ml-1">
                    <path d="m9 18 6-6-6-6" />
                  </svg>
                </UiButton>
              </div>
            </div>
          </div>
          <div v-else class="flex flex-col items-center justify-center py-12">
            <div class="h-16 w-16 rounded-full bg-muted flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-muted-foreground">
                <path d="M8 2v4" /><path d="M16 2v4" /><rect width="18" height="18" x="3" y="4" rx="2" /><path d="M3 10h18" />
              </svg>
            </div>
            <p class="text-lg font-medium">No events found</p>
            <p class="text-sm text-muted-foreground mt-1">Try adjusting your filters or create a new event</p>
          </div>
        </UiCardContent>
      </UiCard>
    </div>

    <!-- Create Event Dialog -->
    <UiDialog v-model:open="dialogOpen">
      <UiDialogContent class="max-w-2xl">
        <UiDialogHeader>
          <UiDialogTitle class="text-2xl">Record New Event</UiDialogTitle>
          <UiDialogDescription>
            Log a new traceability event for an animal in the system. All events are automatically validated for compliance.
          </UiDialogDescription>
        </UiDialogHeader>

        <div class="space-y-5 py-4">
          <div class="grid gap-4 sm:grid-cols-2">
            <div class="space-y-2">
              <UiLabel for="animal_id" class="text-sm font-medium">
                Animal ID *
              </UiLabel>
              <UiInput 
                id="animal_id" 
                v-model="eventForm.animal_id" 
                type="number"
                placeholder="e.g., 123"
                class="h-10"
              />
              <p class="text-xs text-muted-foreground">Enter the unique identifier for the animal</p>
            </div>

            <div class="space-y-2">
              <UiLabel for="facility_id" class="text-sm font-medium">
                Facility *
              </UiLabel>
              <UiSelect v-model="eventForm.facility_id">
                <UiSelectTrigger id="facility_id" class="h-10">
                  <UiSelectValue placeholder="Select a facility" />
                </UiSelectTrigger>
                <UiSelectContent>
                  <UiSelectItem 
                    v-for="facility in facilities" 
                    :key="facility.id" 
                    :value="facility.id.toString()"
                  >
                    <div class="flex items-center gap-2">
                      <span v-if="facility.facility_type === 'farm'">🚜</span>
                      <span v-else-if="facility.facility_type === 'processor'">🏭</span>
                      <span v-else-if="facility.facility_type === 'retailer'">🏪</span>
                      <span v-else>🏢</span>
                      <div>
                        <div class="font-medium">{{ facility.name }}</div>
                        <div class="text-xs text-muted-foreground">{{ facility.location }}</div>
                      </div>
                    </div>
                  </UiSelectItem>
                </UiSelectContent>
              </UiSelect>
              <p class="text-xs text-muted-foreground">Facility where the event occurred</p>
            </div>
          </div>

          <div class="space-y-2">
            <UiLabel for="event_type" class="text-sm font-medium">
              Event Type *
            </UiLabel>
            <UiSelect v-model="eventForm.event_type">
              <UiSelectTrigger id="event_type" class="h-10">
                <UiSelectValue placeholder="Select the type of event" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem value="birth">
                  <div class="flex items-center gap-2">
                    <span>🐣</span>
                    <div>
                      <div class="font-medium">Birth</div>
                      <div class="text-xs text-muted-foreground">Animal birth or arrival</div>
                    </div>
                  </div>
                </UiSelectItem>
                <UiSelectItem value="vaccination">
                  <div class="flex items-center gap-2">
                    <span>💉</span>
                    <div>
                      <div class="font-medium">Vaccination</div>
                      <div class="text-xs text-muted-foreground">Vaccine administration</div>
                    </div>
                  </div>
                </UiSelectItem>
                <UiSelectItem value="weighing">
                  <div class="flex items-center gap-2">
                    <span>⚖️</span>
                    <div>
                      <div class="font-medium">Weighing</div>
                      <div class="text-xs text-muted-foreground">Weight measurement</div>
                    </div>
                  </div>
                </UiSelectItem>
                <UiSelectItem value="movement">
                  <div class="flex items-center gap-2">
                    <span>🚚</span>
                    <div>
                      <div class="font-medium">Movement</div>
                      <div class="text-xs text-muted-foreground">Transfer between facilities</div>
                    </div>
                  </div>
                </UiSelectItem>
                <UiSelectItem value="health_check">
                  <div class="flex items-center gap-2">
                    <span>🏥</span>
                    <div>
                      <div class="font-medium">Health Check</div>
                      <div class="text-xs text-muted-foreground">Routine health examination</div>
                    </div>
                  </div>
                </UiSelectItem>
                <UiSelectItem value="treatment">
                  <div class="flex items-center gap-2">
                    <span>💊</span>
                    <div>
                      <div class="font-medium">Treatment</div>
                      <div class="text-xs text-muted-foreground">Medical treatment or medication</div>
                    </div>
                  </div>
                </UiSelectItem>
                <UiSelectItem value="feeding">
                  <div class="flex items-center gap-2">
                    <span>🌾</span>
                    <div>
                      <div class="font-medium">Feeding</div>
                      <div class="text-xs text-muted-foreground">Feed type or schedule change</div>
                    </div>
                  </div>
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>

          <div class="space-y-2">
            <UiLabel for="metadata" class="text-sm font-medium">
              Notes / Additional Information
              <span class="text-muted-foreground font-normal">(Optional)</span>
            </UiLabel>
            <UiTextarea 
              id="metadata" 
              v-model="eventForm.event_metadata" 
              placeholder="Add any additional details, observations, or metadata about this event..."
              rows="4"
              class="resize-none"
            />
            <p class="text-xs text-muted-foreground">This information will be included in the event record and audit trail</p>
          </div>
        </div>

        <UiDialogFooter class="gap-2">
          <UiButton variant="outline" @click="dialogOpen = false">
            Cancel
          </UiButton>
          <UiButton 
            @click="createEvent" 
            :disabled="!eventForm.animal_id || !eventForm.event_type || !eventForm.facility_id"
            class="min-w-[120px]"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="mr-2">
              <path d="M5 12h14" />
              <path d="M12 5v14" />
            </svg>
            Record Event
          </UiButton>
        </UiDialogFooter>
      </UiDialogContent>
    </UiDialog>
  </NuxtLayout>
</template>

<script setup lang="ts">
const api = useApi()

const filterType = ref('all')
const filterValid = ref('all')
const currentPage = ref(1)
const pageSize = ref(20)
const loading = ref(false)

const events = ref<any[]>([])
const total = ref(0)
const facilities = ref<any[]>([])

// Dialog state
const dialogOpen = ref(false)
const eventForm = ref({
  animal_id: '',
  event_type: '',
  facility_id: '',
  event_metadata: ''
})

// Computed stats
const validCount = computed(() => {
  return events.value.filter(e => e.is_valid).length
})

const anomalyCount = computed(() => {
  return events.value.filter(e => !e.is_valid).length
})

// Helper functions
const getEventIcon = (eventType: string) => {
  const icons: Record<string, string> = {
    birth: '🐣',
    vaccination: '💉',
    weighing: '⚖️',
    movement: '🚚',
    health_check: '🏥',
    treatment: '💊',
    feeding: '🌾'
  }
  return icons[eventType] || '📋'
}

const formatEventType = (eventType: string) => {
  return eventType
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const loadEvents = async () => {
  loading.value = true
  const params: any = {
    skip: (currentPage.value - 1) * pageSize.value,
    limit: pageSize.value,
  }

  if (filterType.value && filterType.value !== 'all') {
    params.event_type = filterType.value
  }

  if (filterValid.value === 'valid') {
    params.is_valid = true
  } else if (filterValid.value === 'invalid') {
    params.is_valid = false
  }

  const result = await api.getEvents(params)
  if (result.data) {
    events.value = result.data.events
    total.value = result.data.total
  }
  loading.value = false
}

const applyFilters = () => {
  currentPage.value = 1
  loadEvents()
}

const changePage = (page: number) => {
  currentPage.value = page
  loadEvents()
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

const openCreateDialog = () => {
  eventForm.value = {
    animal_id: '',
    event_type: '',
    facility_id: '',
    event_metadata: ''
  }
  dialogOpen.value = true
}

const loadFacilities = async () => {
  const result = await api.getFacilities({ limit: 100 })
  if (result.data?.facilities) {
    facilities.value = result.data.facilities
  }
}

const createEvent = async () => {
  if (!eventForm.value.animal_id || !eventForm.value.event_type || !eventForm.value.facility_id) {
    return
  }

  const payload = {
    animal_id: parseInt(eventForm.value.animal_id),
    event_type: eventForm.value.event_type,
    facility_id: parseInt(eventForm.value.facility_id),
    metadata: eventForm.value.event_metadata || ""
  }

  const result = await api.createEvent(payload)

  if (result.data) {
    dialogOpen.value = false
    loadEvents()
  }
}

onMounted(() => {
  loadEvents()
  loadFacilities()
})
</script>
