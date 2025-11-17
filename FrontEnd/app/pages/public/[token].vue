<template>
  <div class="min-h-screen bg-gradient-to-br from-primary/10 to-background">
    <!-- Header -->
    <div class="bg-white border-b">
      <div class="container mx-auto px-4 py-6">
        <div class="flex items-center gap-3">
          <svg class="h-8 w-8 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h1 class="text-2xl font-bold">FarmTrack</h1>
            <p class="text-sm text-muted-foreground">Livestock Traceability</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-4 py-12">
      <div class="flex flex-col items-center justify-center space-y-4">
        <UiSpinner class="h-12 w-12" />
        <p class="text-muted-foreground">Loading animal information...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="container mx-auto px-4 py-12">
      <UiCard class="max-w-2xl mx-auto">
        <UiCardContent class="pt-6">
          <div class="text-center space-y-4">
            <div class="flex justify-center">
              <svg class="h-16 w-16 text-destructive" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 class="text-2xl font-bold">Animal Not Found</h2>
            <p class="text-muted-foreground">{{ error }}</p>
          </div>
        </UiCardContent>
      </UiCard>
    </div>

    <!-- Animal Details -->
    <div v-else-if="animal" class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto space-y-6">
        <!-- Animal Info Card -->
        <UiCard>
          <UiCardHeader>
            <div class="flex items-start justify-between">
              <div>
                <UiCardTitle class="text-3xl">{{ animal.name }}</UiCardTitle>
                <UiCardDescription class="text-lg mt-2">
                  {{ animal.species }}
                  <span v-if="animal.breed"> • {{ animal.breed.name }}</span>
                </UiCardDescription>
              </div>
              <UiBadge variant="default" class="text-lg px-4 py-2">
                Verified
              </UiBadge>
            </div>
          </UiCardHeader>
          <UiCardContent class="space-y-6">
            <!-- Key Details Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-1">
                <p class="text-sm font-medium text-muted-foreground">Tag ID</p>
                <p class="text-lg font-semibold">{{ animal.tag_id || 'N/A' }}</p>
              </div>
              
              <div class="space-y-1" v-if="animal.date_added">
                <p class="text-sm font-medium text-muted-foreground">Date Registered</p>
                <p class="text-lg font-semibold">{{ formatDate(animal.date_added) }}</p>
              </div>

              <div class="space-y-1" v-if="animal.breed">
                <p class="text-sm font-medium text-muted-foreground">Breed</p>
                <p class="text-lg font-semibold">{{ animal.breed.name }}</p>
                <p class="text-xs text-muted-foreground" v-if="animal.breed.country">
                  Origin: {{ animal.breed.country }}
                </p>
              </div>

              <div class="space-y-1" v-if="animal.facility">
                <p class="text-sm font-medium text-muted-foreground">Current Location</p>
                <p class="text-lg font-semibold">{{ animal.facility.name }}</p>
                <p class="text-xs text-muted-foreground">
                  {{ animal.facility.facility_type }} • {{ animal.facility.location }}
                </p>
              </div>
            </div>

            <!-- Breed Description -->
            <div v-if="animal.breed?.description" class="pt-4 border-t">
              <p class="text-sm font-medium text-muted-foreground mb-2">About the Breed</p>
              <p class="text-sm">{{ animal.breed.description }}</p>
            </div>
          </UiCardContent>
        </UiCard>

        <!-- Event Timeline -->
        <UiCard>
          <UiCardHeader>
            <UiCardTitle>Traceability Timeline</UiCardTitle>
            <UiCardDescription>Complete history of events for this animal</UiCardDescription>
          </UiCardHeader>
          <UiCardContent>
            <div v-if="loadingEvents" class="flex justify-center py-8">
              <UiSpinner />
            </div>
            <div v-else-if="events && events.length > 0" class="space-y-4">
              <div
                v-for="(event, index) in events"
                :key="event.id"
                class="flex gap-4 pb-4"
                :class="{ 'border-b': index < events.length - 1 }"
              >
                <div class="flex flex-col items-center">
                  <div 
                    class="w-3 h-3 rounded-full"
                    :class="event.is_valid ? 'bg-primary' : 'bg-destructive'"
                  ></div>
                  <div 
                    v-if="index < events.length - 1"
                    class="w-px flex-1 mt-2"
                    :class="event.is_valid ? 'bg-primary/30' : 'bg-destructive/30'"
                  ></div>
                </div>
                <div class="flex-1 pb-4">
                  <div class="flex items-center gap-2 mb-1">
                    <UiBadge>{{ event.event_type }}</UiBadge>
                    <UiBadge v-if="!event.is_valid" variant="destructive">Anomaly</UiBadge>
                  </div>
                  <p class="text-sm font-medium">
                    {{ formatDateTime(event.timestamp) }}
                  </p>
                  <p v-if="event.facility" class="text-sm text-muted-foreground mt-1">
                    Location: {{ event.facility.name }}
                  </p>
                  <p v-if="!event.is_valid && event.anomaly_reason" class="text-sm text-destructive mt-2">
                    ⚠️ {{ event.anomaly_reason }}
                  </p>
                  <p v-if="event.metadata" class="text-xs text-muted-foreground mt-1">
                    {{ event.metadata }}
                  </p>
                </div>
              </div>
            </div>
            <div v-else class="py-8 text-center text-muted-foreground">
              <svg class="h-12 w-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <p>No events recorded yet</p>
            </div>
          </UiCardContent>
        </UiCard>

        <!-- Trust Badge -->
        <div class="text-center py-6">
          <div class="inline-flex items-center gap-2 text-sm text-muted-foreground">
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span>Verified by FarmTrack Traceability System</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false // No authenticated layout for public page
})

const route = useRoute()
const api = useApi()

const animalId = computed(() => route.params.token as string)

const animal = ref<any>(null)
const events = ref<any[]>([])
const loading = ref(true)
const loadingEvents = ref(false)
const error = ref('')

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatDateTime = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadAnimal = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const result = await api.getAnimal(parseInt(animalId.value))
    
    if (result.error) {
      error.value = result.error
    } else if (result.data) {
      animal.value = result.data
      loadEvents()
    } else {
      error.value = 'Animal not found in our system'
    }
  } catch (err) {
    error.value = 'Unable to load animal information. Please try again.'
  } finally {
    loading.value = false
  }
}

const loadEvents = async () => {
  loadingEvents.value = true
  
  try {
    const result = await api.getAnimalEvents(parseInt(animalId.value))
    
    if (result.data?.events) {
      events.value = result.data.events
    }
  } catch (err) {
    console.error('Error loading events:', err)
  } finally {
    loadingEvents.value = false
  }
}

onMounted(() => {
  loadAnimal()
})
</script>