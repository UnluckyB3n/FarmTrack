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
          <UiButton @click="openEditDialog">Edit Animal</UiButton>
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
              <p class="text-sm font-medium">Date Added</p>
              <p class="text-sm text-muted-foreground">
                {{ formatDate(animal.date_added) }}
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

    <!-- Edit Animal Dialog -->
    <UiDialog v-model:open="editDialogOpen">
      <UiDialogContent class="max-w-2xl max-h-[90vh] overflow-y-auto">
        <UiDialogHeader>
          <UiDialogTitle>Edit Animal</UiDialogTitle>
          <UiDialogDescription>
            Update the animal's information
          </UiDialogDescription>
        </UiDialogHeader>

        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <UiLabel for="edit-name">Name *</UiLabel>
            <UiInput id="edit-name" v-model="editAnimal.name" placeholder="e.g., Bessie" />
          </div>

          <div class="space-y-2">
            <UiLabel for="edit-species">Species *</UiLabel>
            <UiSelect v-model="editAnimal.species" @update:model-value="onSpeciesChange">
              <UiSelectTrigger id="edit-species">
                <UiSelectValue placeholder="Select species" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem v-for="sp in breedSpecies" :key="sp" :value="sp">
                  {{ sp }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>

          <div v-if="editAnimal.species && breedCountries.length > 0" class="space-y-2">
            <UiLabel for="edit-country">Country (Optional)</UiLabel>
            <UiSelect v-model="editAnimal.country" @update:model-value="onCountryChange">
              <UiSelectTrigger id="edit-country">
                <UiSelectValue placeholder="Select country to filter breeds" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem value="all">All countries</UiSelectItem>
                <UiSelectItem v-for="country in breedCountries" :key="country.country" :value="country.country">
                  {{ country.country }} ({{ country.breed_count }} breeds)
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>

          <div v-if="editAnimal.species" class="space-y-2">
            <UiLabel for="edit-breed">Breed (Optional)</UiLabel>
            <UiSelect v-model="editAnimal.breed_id" :disabled="loadingBreeds">
              <UiSelectTrigger id="edit-breed">
                <UiSelectValue :placeholder="loadingBreeds ? 'Loading breeds...' : 'Select breed'" />
              </UiSelectTrigger>
              <UiSelectContent>
                <div v-if="availableBreeds.length === 0" class="px-3 py-2 text-sm text-muted-foreground">
                  No breeds available for this selection
                </div>
                <UiSelectItem v-for="breed in availableBreeds" :key="breed.id" :value="String(breed.id)">
                  {{ breed.breed_name }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
            <p v-if="availableBreeds.length > 0" class="text-xs text-muted-foreground">
              {{ availableBreeds.length }} breeds available
            </p>
          </div>

          <div class="space-y-2">
            <UiLabel for="edit-tag">Tag ID</UiLabel>
            <UiInput id="edit-tag" v-model="editAnimal.tag_id" placeholder="e.g., TAG-001" />
          </div>

          <div class="space-y-2">
            <UiLabel for="edit-facility">Facility</UiLabel>
            <UiInput id="edit-facility" v-model="editAnimal.facility_id" type="number" placeholder="Facility ID" />
          </div>

          <div class="space-y-2">
            <UiLabel for="edit-date">Date Added</UiLabel>
            <UiInput id="edit-date" v-model="editAnimal.date_added" type="date" />
          </div>
        </div>

        <UiDialogFooter>
          <UiButton variant="outline" @click="editDialogOpen = false">Cancel</UiButton>
          <UiButton @click="updateAnimal" :disabled="!editAnimal.name || !editAnimal.species">
            Update Animal
          </UiButton>
        </UiDialogFooter>
      </UiDialogContent>
    </UiDialog>
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
const editDialogOpen = ref(false)
const editAnimal = ref({
  name: '',
  species: '',
  breed_id: '',
  country: '',
  tag_id: '',
  facility_id: '',
  date_added: ''
})

// Breed filter state for edit dialog
const breedSpecies = ref<string[]>([])
const breedCountries = ref<any[]>([])
const availableBreeds = ref<any[]>([])
const loadingBreeds = ref(false)

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
    console.log('Loaded animal:', animal.value)
  }
  loading.value = false
}

const loadEvents = async () => {
  loadingEvents.value = true
  const result = await api.getAnimalEvents(animalId.value)
  if (result.data && result.data.events) {
    events.value = result.data.events.sort((a: any, b: any) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    )
  }
  loadingEvents.value = false
}

const openEditDialog = async () => {
  // Populate edit form with current animal data
  editAnimal.value = {
    name: animal.value.name,
    species: animal.value.species,
    breed_id: animal.value.breed_id || '',
    country: animal.value.breed?.country || '',
    tag_id: animal.value.tag_id,
    facility_id: animal.value.facility_id,
    date_added: animal.value.date_added ? animal.value.date_added.split('T')[0] : ''
  }
  
  // Load breed data for the edit dialog
  await loadBreedSpecies()
  if (editAnimal.value.species) {
    await onSpeciesChange()
  }
  
  editDialogOpen.value = true
}

const loadBreedSpecies = async () => {
  const result = await api.getBreedSpecies()
  if (result.data?.species) {
    breedSpecies.value = result.data.species
  }
}

const onSpeciesChange = async () => {
  // Reset breed and country when species changes
  editAnimal.value.breed_id = ''
  editAnimal.value.country = ''
  breedCountries.value = []
  availableBreeds.value = []
  
  if (editAnimal.value.species) {
    // Load countries for this species
    const result = await api.getBreedCountries(editAnimal.value.species)
    if (result.data?.countries) {
      breedCountries.value = result.data.countries
    }
    
    // Also load all breeds for this species
    loadingBreeds.value = true
    const breedsResult = await api.getBreeds({
      species: editAnimal.value.species,
      limit: 200
    })
    if (breedsResult.data?.breeds) {
      availableBreeds.value = breedsResult.data.breeds
    }
    loadingBreeds.value = false
  }
}

const onCountryChange = async () => {
  // Reset breed when country changes
  editAnimal.value.breed_id = ''
  
  if (editAnimal.value.species && editAnimal.value.country && editAnimal.value.country !== 'all') {
    // Load breeds for this species and country
    loadingBreeds.value = true
    const result = await api.getBreeds({
      species: editAnimal.value.species,
      country: editAnimal.value.country,
      limit: 200
    })
    if (result.data?.breeds) {
      availableBreeds.value = result.data.breeds
    }
    loadingBreeds.value = false
  } else if (editAnimal.value.species) {
    // Load all breeds for this species (no country filter)
    loadingBreeds.value = true
    const result = await api.getBreeds({
      species: editAnimal.value.species,
      limit: 200
    })
    if (result.data?.breeds) {
      availableBreeds.value = result.data.breeds
    }
    loadingBreeds.value = false
  }
}

const updateAnimal = async () => {
  if (!editAnimal.value.name || !editAnimal.value.species) {
    return
  }

  const payload = {
    name: editAnimal.value.name,
    species: editAnimal.value.species,
    breed_id: editAnimal.value.breed_id || null,
    tag_id: editAnimal.value.tag_id,
    facility_id: editAnimal.value.facility_id,
    date_added: editAnimal.value.date_added
  }

  const result = await api.updateAnimal(animalId.value, payload)
  
  if (result.data) {
    editDialogOpen.value = false
    await loadAnimal()
  }
}

onMounted(() => {
  loadAnimal()
  loadEvents()
})
</script>