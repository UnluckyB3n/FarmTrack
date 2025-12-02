<template>
  <NuxtLayout name="default">
    <div class="space-y-6">
      <div>
        <h1 class="text-3xl font-bold">Animal Traceability</h1>
        <p class="text-muted-foreground mt-2">
          Track complete lifecycle and movement history of any animal
        </p>
      </div>

      <!-- Search -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Search Animal</UiCardTitle>
          <UiCardDescription>Enter animal ID or tag ID to trace</UiCardDescription>
        </UiCardHeader>
        <UiCardContent>
          <div class="flex gap-2">
            <UiInput
              v-model="searchQuery"
              placeholder="Enter animal ID or tag ID..."
              @keyup.enter="searchAnimal"
              class="flex-1"
            />
            <UiButton @click="searchAnimal" :disabled="!searchQuery || searching">
              <UiSpinner v-if="searching" class="mr-2 h-4 w-4" />
              Search
            </UiButton>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Results -->
      <div v-if="animal" class="space-y-6">
        <!-- Animal Info -->
        <UiCard>
          <UiCardHeader>
            <UiCardTitle>Animal Information</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="grid gap-4 md:grid-cols-3">
              <div>
                <p class="text-sm font-medium">Name</p>
                <p class="text-sm text-muted-foreground">{{ animal.name }}</p>
              </div>
              <div>
                <p class="text-sm font-medium">Species</p>
                <p class="text-sm text-muted-foreground">{{ animal.species }}</p>
              </div>
              <div>
                <p class="text-sm font-medium">Tag ID</p>
                <p class="text-sm text-muted-foreground">{{ animal.tag_id }}</p>
              </div>
              <div>
                <p class="text-sm font-medium">Breed</p>
                <p class="text-sm text-muted-foreground">{{ animal.breed?.name || 'N/A' }}</p>
              </div>
              <div>
                <p class="text-sm font-medium">Current Facility</p>
                <p class="text-sm text-muted-foreground">{{ animal.facility?.name || 'Unknown' }}</p>
              </div>
              <div>
                <p class="text-sm font-medium">Owner</p>
                <p class="text-sm text-muted-foreground">{{ animal.owner?.username || 'Unknown' }}</p>
              </div>
            </div>
          </UiCardContent>
        </UiCard>

        <!-- Movement History -->
        <UiCard>
          <UiCardHeader>
            <UiCardTitle>Movement History</UiCardTitle>
            <UiCardDescription>Complete transfer chain across facilities</UiCardDescription>
          </UiCardHeader>
          <UiCardContent>
            <div v-if="loadingMovements" class="flex justify-center py-8">
              <UiSpinner />
            </div>
            <div v-else-if="movements.length > 0" class="space-y-3">
              <div
                v-for="(movement, index) in movements"
                :key="movement.id"
                class="flex items-start gap-4 p-3 border rounded-lg"
              >
                <div class="flex-shrink-0 w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-medium">
                  {{ movements.length - index }}
                </div>
                <div class="flex-1">
                  <p class="font-medium text-sm">{{ movement.facility_name }}</p>
                  <p class="text-xs text-muted-foreground">{{ movement.facility_type }} • {{ movement.facility_location }}</p>
                  <p class="text-xs text-muted-foreground mt-1">{{ formatDate(movement.timestamp) }}</p>
                  <p v-if="movement.metadata" class="text-xs mt-1">{{ movement.metadata }}</p>
                </div>
              </div>
            </div>
            <div v-else class="py-8 text-center text-muted-foreground text-sm">
              No movement history available
            </div>
          </UiCardContent>
        </UiCard>

        <!-- Event Timeline -->
        <UiCard>
          <UiCardHeader>
            <UiCardTitle>Event Timeline</UiCardTitle>
            <UiCardDescription>Complete lifecycle events</UiCardDescription>
          </UiCardHeader>
          <UiCardContent>
            <div v-if="loadingEvents" class="flex justify-center py-8">
              <UiSpinner />
            </div>
            <div v-else-if="events.length > 0" class="space-y-3">
              <div
                v-for="event in events"
                :key="event.id"
                class="flex gap-4 border-l-2 pl-4 pb-4"
                :class="event.is_valid ? 'border-primary' : 'border-destructive'"
              >
                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <UiBadge>{{ event.event_type }}</UiBadge>
                    <UiBadge v-if="!event.is_valid" variant="destructive">Anomaly</UiBadge>
                  </div>
                  <p class="text-sm font-medium mt-2">{{ formatDate(event.timestamp) }}</p>
                  <p v-if="event.metadata" class="text-xs text-muted-foreground mt-1">{{ event.metadata }}</p>
                  <p v-if="!event.is_valid && event.anomaly_reason" class="text-sm text-destructive mt-1">
                    ⚠️ {{ event.anomaly_reason }}
                  </p>
                </div>
              </div>
            </div>
            <div v-else class="py-8 text-center text-muted-foreground text-sm">
              No events recorded
            </div>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- No Results -->
      <UiAlert v-else-if="searched && !animal">
        <p>No animal found with ID or tag "{{ searchQuery }}"</p>
      </UiAlert>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const api = useApi()

const searchQuery = ref('')
const searching = ref(false)
const searched = ref(false)
const animal = ref<any>(null)
const movements = ref<any[]>([])
const loadingMovements = ref(false)
const events = ref<any[]>([])
const loadingEvents = ref(false)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const searchAnimal = async () => {
  if (!searchQuery.value) return
  
  searching.value = true
  searched.value = true
  animal.value = null
  movements.value = []
  events.value = []
  
  // Try to parse as ID first
  const animalId = parseInt(searchQuery.value)
  
  if (!isNaN(animalId)) {
    // Search by ID
    const result = await api.getAnimal(animalId)
    if (result.data) {
      animal.value = result.data
      await loadMovementHistory(animalId)
      await loadEvents(animalId)
    }
  } else {
    // Search by tag ID
    const result = await api.getAnimals({ tag_id: searchQuery.value })
    if (result.data?.animals && result.data.animals.length > 0) {
      animal.value = result.data.animals[0]
      await loadMovementHistory(animal.value.id)
      await loadEvents(animal.value.id)
    }
  }
  
  searching.value = false
}

const loadMovementHistory = async (animalId: number) => {
  loadingMovements.value = true
  const result = await api.getMovementHistory(animalId)
  if (result.data?.movement_history) {
    movements.value = result.data.movement_history
  }
  loadingMovements.value = false
}

const loadEvents = async (animalId: number) => {
  loadingEvents.value = true
  const result = await api.getAnimalEvents(animalId)
  if (result.data?.events) {
    events.value = result.data.events.sort((a: any, b: any) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    )
  }
  loadingEvents.value = false
}
</script>