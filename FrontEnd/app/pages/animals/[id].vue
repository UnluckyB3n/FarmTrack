<template>
  <NuxtLayout name="default">
    <div v-if="loading" class="flex justify-center items-center min-h-[400px]">
      <UiSpinner class="h-8 w-8" />
    </div>
    <div v-else-if="animal" class="space-y-6">
      <!-- Header -->
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-3xl font-bold">{{ animal.name }}</h1>
          <p class="text-muted-foreground mt-1">Tag ID: {{ animal.tag_id }}</p>
        </div>
        <div class="flex gap-2">
          <UiButton variant="outline" @click="router.push('/animals')">
            Back to Animals
          </UiButton>
          <UiButton>Edit Animal</UiButton>
        </div>
      </div>

      <!-- Info Cards -->
      <div class="grid gap-4 md:grid-cols-3">
        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Species</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ animal.species }}</div>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Breed</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ animal.breed?.name || 'N/A' }}</div>
            <p v-if="animal.breed?.code" class="text-xs text-muted-foreground">{{ animal.breed.code }}</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Status</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <UiBadge :variant="animal.date_of_death ? 'destructive' : 'default'">
              {{ animal.date_of_death ? 'Deceased' : 'Active' }}
            </UiBadge>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Details -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Details</UiCardTitle>
        </UiCardHeader>
        <UiCardContent class="space-y-3">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-medium">Date of Birth</p>
              <p class="text-sm text-muted-foreground">
                {{ formatDate(animal.date_of_birth) }}
              </p>
            </div>
            <div v-if="animal.date_of_death">
              <p class="text-sm font-medium">Date of Death</p>
              <p class="text-sm text-muted-foreground">
                {{ formatDate(animal.date_of_death) }}
              </p>
            </div>
            <div v-if="animal.facility">
              <p class="text-sm font-medium">Current Facility</p>
              <p class="text-sm text-muted-foreground">
                {{ animal.facility.name }} ({{ animal.facility.facility_type }})
              </p>
            </div>
            <div v-if="animal.owner">
              <p class="text-sm font-medium">Owner</p>
              <p class="text-sm text-muted-foreground">
                {{ animal.owner.username }}
              </p>
            </div>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Event Timeline -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Event Timeline</UiCardTitle>
          <UiCardDescription>Complete history of events for this animal</UiCardDescription>
        </UiCardHeader>
        <UiCardContent>
          <div v-if="loadingEvents" class="flex justify-center py-8">
            <UiSpinner />
          </div>
          <div v-else-if="events && events.length > 0" class="space-y-4">
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
                <p class="text-sm font-medium mt-2">
                  {{ formatDate(event.timestamp) }}
                </p>
                <p v-if="event.facility" class="text-sm text-muted-foreground">
                  at {{ event.facility.name }}
                </p>
                <p v-if="!event.is_valid && event.anomaly_reason" class="text-sm text-destructive mt-1">
                  ⚠️ {{ event.anomaly_reason }}
                </p>
                <p v-if="event.metadata" class="text-xs text-muted-foreground mt-1">
                  {{ event.metadata }}
                </p>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-muted-foreground">
            No events recorded yet
          </div>
        </UiCardContent>
      </UiCard>
    </div>
    <div v-else class="text-center py-12">
      <p class="text-muted-foreground">Animal not found</p>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const api = useApi()

const animalId = computed(() => parseInt(route.params.id as string))

const animal = ref<any>(null)
const events = ref<any[]>([])
const loading = ref(true)
const loadingEvents = ref(true)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const loadAnimal = async () => {
  loading.value = true
  const result = await api.getAnimal(animalId.value)
  if (result.data) {
    animal.value = result.data
  }
  loading.value = false
}

const loadEvents = async () => {
  loadingEvents.value = true
  const result = await api.getAnimalEvents(animalId.value)
  if (result.data) {
    events.value = result.data.sort((a: any, b: any) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    )
  }
  loadingEvents.value = false
}

onMounted(() => {
  loadAnimal()
  loadEvents()
})
</script>