<template>
  <NuxtLayout name="default">
    <div class="space-y-4">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium">Events</h3>
          <p class="text-sm text-muted-foreground">Track all livestock traceability events</p>
        </div>
        <UiButton>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
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

      <!-- Filters -->
      <UiCard>
        <UiCardContent class="pt-6">
          <div class="flex gap-4">
            <UiSelect v-model="filterType">
              <UiSelectTrigger class="w-[180px]">
                <UiSelectValue placeholder="Event Type" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem value="all">All Types</UiSelectItem>
                <UiSelectItem value="birth">Birth</UiSelectItem>
                <UiSelectItem value="vaccination">Vaccination</UiSelectItem>
                <UiSelectItem value="weighing">Weighing</UiSelectItem>
                <UiSelectItem value="movement">Movement</UiSelectItem>
                <UiSelectItem value="health_check">Health Check</UiSelectItem>
              </UiSelectContent>
            </UiSelect>

            <UiSelect v-model="filterValid">
              <UiSelectTrigger class="w-[180px]">
                <UiSelectValue placeholder="Validation" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem value="all">All Events</UiSelectItem>
                <UiSelectItem value="valid">Valid Only</UiSelectItem>
                <UiSelectItem value="invalid">Anomalies Only</UiSelectItem>
              </UiSelectContent>
            </UiSelect>

            <UiButton variant="outline" @click="applyFilters">Apply</UiButton>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Events List -->
      <UiCard>
        <UiCardContent class="pt-6">
          <div v-if="loading" class="flex justify-center py-8">
            <UiSpinner />
          </div>
          <div v-else-if="events && events.length > 0" class="space-y-4">
            <div
              v-for="event in events"
              :key="event.id"
              class="flex items-center justify-between border-b pb-4 last:border-0"
            >
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <UiBadge :variant="event.is_valid ? 'default' : 'destructive'">
                    {{ event.event_type }}
                  </UiBadge>
                  <span class="text-sm font-medium">Animal ID: {{ event.animal_id }}</span>
                  <span v-if="!event.is_valid" class="text-xs text-destructive">
                    • {{ event.anomaly_reason }}
                  </span>
                </div>
                <p class="text-xs text-muted-foreground">
                  Facility #{{ event.facility_id }} • {{ formatDate(event.timestamp) }}
                </p>
              </div>
              <div class="flex items-center gap-2">
                <UiButton variant="ghost" size="sm">View Details</UiButton>
              </div>
            </div>

            <!-- Pagination -->
            <div class="mt-4 flex items-center justify-between pt-4 border-t">
              <p class="text-sm text-muted-foreground">
                Showing {{ events.length }} of {{ total }} events
              </p>
              <div class="flex gap-2">
                <UiButton
                  variant="outline"
                  size="sm"
                  :disabled="currentPage === 1"
                  @click="changePage(currentPage - 1)"
                >
                  Previous
                </UiButton>
                <UiButton
                  variant="outline"
                  size="sm"
                  :disabled="currentPage * pageSize >= total"
                  @click="changePage(currentPage + 1)"
                >
                  Next
                </UiButton>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-muted-foreground">
            No events found
          </div>
        </UiCardContent>
      </UiCard>
    </div>
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

onMounted(() => {
  loadEvents()
})
</script>
