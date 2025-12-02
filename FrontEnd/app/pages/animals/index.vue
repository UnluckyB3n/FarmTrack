<template>
  <NuxtLayout name="default">
    <div class="space-y-4">
      <!-- Header with Actions -->
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium">Animals Management</h3>
          <p class="text-sm text-muted-foreground">View and manage your livestock inventory</p>
        </div>
        <UiButton @click="showAddDialog = true">
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
          Add Animal
        </UiButton>
      </div>

      <!-- Search and Filters -->
      <UiCard>
        <UiCardContent class="pt-6">
          <div class="flex gap-4">
            <div class="flex-1">
              <UiInput v-model="searchQuery" placeholder="Search by name or tag ID..." />
            </div>
            <UiSelect v-model="selectedSpecies">
              <UiSelectTrigger class="w-[180px]">
                <UiSelectValue placeholder="All Species" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem value="all">All Species</UiSelectItem>
                <UiSelectItem v-for="species in speciesList" :key="species" :value="species">
                  {{ species }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
            <UiButton variant="outline" @click="applyFilters">Apply Filters</UiButton>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Animals Table -->
      <UiCard>
        <UiCardContent class="pt-6">
          <div v-if="loading" class="flex justify-center py-8">
            <UiSpinner />
          </div>
          <div v-else-if="animals && animals.length > 0">
            <UiTable>
              <UiTableHeader>
                <UiTableRow>
                  <UiTableHead>Tag ID</UiTableHead>
                  <UiTableHead>Name</UiTableHead>
                  <UiTableHead>Species</UiTableHead>
                  <UiTableHead>Date Added</UiTableHead>
                  <UiTableHead>Facility</UiTableHead>
                  <UiTableHead>Actions</UiTableHead>
                </UiTableRow>
              </UiTableHeader>
              <UiTableBody>
                <UiTableRow v-for="animal in animals" :key="animal.id">
                  <UiTableCell class="font-medium">{{ animal.tag_id }}</UiTableCell>
                  <UiTableCell>{{ animal.name }}</UiTableCell>
                  <UiTableCell>
                    <UiBadge variant="outline">{{ animal.species }}</UiBadge>
                  </UiTableCell>
                  <UiTableCell>{{ formatDate(animal.date_added) }}</UiTableCell>
                  <UiTableCell>{{ getFacilityName(animal.facility_id) }}</UiTableCell>
                  <UiTableCell>
                    <div class="flex gap-2">
                      <UiButton variant="ghost" size="sm" @click="viewAnimal(animal.id)">
                        View
                      </UiButton>
                      <UiButton variant="ghost" size="sm" @click="editAnimal(animal)">
                        Edit
                      </UiButton>
                    </div>
                  </UiTableCell>
                </UiTableRow>
              </UiTableBody>
            </UiTable>

            <!-- Pagination -->
            <div class="mt-4 flex items-center justify-between">
              <p class="text-sm text-muted-foreground">
                Showing {{ animals.length }} of {{ total }} animals
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
            No animals found
          </div>
        </UiCardContent>
      </UiCard>
    </div>

    <!-- Add Animal Dialog -->
    <UiDialog v-model:open="showAddDialog">
      <UiDialogContent class="sm:max-w-[500px]">
        <UiDialogHeader>
          <UiDialogTitle>Add New Animal</UiDialogTitle>
          <UiDialogDescription>
            Enter the details of the new animal to add to your inventory.
          </UiDialogDescription>
        </UiDialogHeader>
        
        <div class="grid gap-4 py-4">
          <div class="grid gap-2">
            <label class="text-sm font-medium">Name *</label>
            <UiInput v-model="newAnimal.name" placeholder="Animal name" />
          </div>
          
          <div class="grid gap-2">
            <label class="text-sm font-medium">Species *</label>
            <UiSelect v-model="newAnimal.species" @update:model-value="onSpeciesChange">
              <UiSelectTrigger>
                <UiSelectValue placeholder="Select species" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem v-for="sp in breedSpecies" :key="sp" :value="sp">
                  {{ sp }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>
          
          <div v-if="newAnimal.species && breedCountries.length > 0" class="grid gap-2">
            <label class="text-sm font-medium">Country (Optional)</label>
            <UiSelect v-model="newAnimal.country" @update:model-value="onCountryChange">
              <UiSelectTrigger>
                <UiSelectValue placeholder="All countries" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem value="all">All countries</UiSelectItem>
                <UiSelectItem v-for="country in breedCountries" :key="country.iso3" :value="country.name">
                  {{ country.name }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>
          
          <div v-if="newAnimal.species" class="grid gap-2">
            <label class="text-sm font-medium">Breed (Optional)</label>
            <UiSelect v-model="newAnimal.breed_id" :disabled="loadingBreeds">
              <UiSelectTrigger>
                <UiSelectValue :placeholder="loadingBreeds ? 'Loading breeds...' : 'Select breed'" />
              </UiSelectTrigger>
              <UiSelectContent>
                <div v-if="availableBreeds.length === 0" class="px-3 py-2 text-sm text-muted-foreground">
                  {{ loadingBreeds ? 'Loading...' : 'No breeds available' }}
                </div>
                <UiSelectItem v-for="breed in availableBreeds" :key="breed.id" :value="breed.id.toString()">
                  {{ breed.breed_name }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
            <p class="text-xs text-muted-foreground">
              {{ availableBreeds.length }} breed{{ availableBreeds.length !== 1 ? 's' : '' }} available
            </p>
          </div>
          
          <div class="grid gap-2">
            <label class="text-sm font-medium">Tag ID</label>
            <UiInput v-model="newAnimal.tag_id" placeholder="e.g., US123456" />
          </div>
          
          <div class="grid gap-2">
            <label class="text-sm font-medium">Facility</label>
            <UiSelect v-model="newAnimal.facility_id">
              <UiSelectTrigger>
                <UiSelectValue placeholder="Select facility" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem v-for="facility in facilities" :key="facility.id" :value="facility.id.toString()">
                  {{ facility.name }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>
          
          <div class="grid gap-2">
            <label class="text-sm font-medium">Date Added</label>
            <UiInput v-model="newAnimal.date_added" type="date" />
          </div>
        </div>
        
        <UiDialogFooter>
          <UiButton variant="outline" @click="showAddDialog = false">
            Cancel
          </UiButton>
          <UiButton @click="createAnimal" :disabled="creatingAnimal">
            {{ creatingAnimal ? 'Creating...' : 'Create Animal' }}
          </UiButton>
        </UiDialogFooter>
      </UiDialogContent>
    </UiDialog>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { toast } from 'vue-sonner'

// Set page title
useHead({
  title: 'Animals - FarmTrack'
})

const api = useApi()
const router = useRouter()

const searchQuery = ref('')
const selectedSpecies = ref('all')
const currentPage = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const showAddDialog = ref(false)
const creatingAnimal = ref(false)

const animals = ref<any[]>([])
const total = ref(0)
const speciesList = ref<string[]>([])
const facilities = ref<any[]>([])

const newAnimal = ref({
  name: '',
  species: '',
  breed_id: '',
  country: '',
  tag_id: '',
  facility_id: '',
  date_added: new Date().toISOString().split('T')[0], // Today's date in YYYY-MM-DD format
})

const breedSpecies = ref<string[]>([])
const breedCountries = ref<any[]>([])
const availableBreeds = ref<any[]>([])
const loadingBreeds = ref(false)

const resetNewAnimal = () => {
  newAnimal.value = {
    name: '',
    species: '',
    breed_id: '',
    country: '',
    tag_id: '',
    facility_id: '',
    date_added: new Date().toISOString().split('T')[0],
  }
  availableBreeds.value = []
  breedCountries.value = []
}

const loadAnimals = async () => {
  loading.value = true
  const params: any = {
    skip: (currentPage.value - 1) * pageSize.value,
    limit: pageSize.value,
  }

  if (searchQuery.value) {
    params.search = searchQuery.value
  }

  if (selectedSpecies.value && selectedSpecies.value !== 'all') {
    params.species = selectedSpecies.value
  }

  const result = await api.getAnimals(params)
  if (result.data) {
    animals.value = result.data.animals
    total.value = result.data.total
  }
  loading.value = false
}

const loadSpecies = async () => {
  const result = await api.getAnimalSpecies()
  if (result.data) {
    speciesList.value = result.data.species
  }
}

const loadFacilities = async () => {
  const result = await api.getFacilities({ limit: 100 })
  if (result.data?.facilities) {
    facilities.value = result.data.facilities
  }
}

const loadBreedSpecies = async () => {
  const result = await api.getBreedSpecies()
  if (result.data?.species) {
    breedSpecies.value = result.data.species
  }
}

const onSpeciesChange = async () => {
  // Reset breed and country when species changes
  newAnimal.value.breed_id = ''
  newAnimal.value.country = ''
  availableBreeds.value = []
  breedCountries.value = []
  
  if (newAnimal.value.species) {
    // Load countries for this species
    const result = await api.getBreedCountries(newAnimal.value.species)
    if (result.data?.countries) {
      breedCountries.value = result.data.countries
    }
  }
}

const onCountryChange = async () => {
  // Reset breed when country changes
  newAnimal.value.breed_id = ''
  
  if (newAnimal.value.species && newAnimal.value.country && newAnimal.value.country !== 'all') {
    // Load breeds for this species and country
    loadingBreeds.value = true
    const result = await api.getBreeds({
      species: newAnimal.value.species,
      country: newAnimal.value.country,
      limit: 200
    })
    if (result.data?.breeds) {
      availableBreeds.value = result.data.breeds
    }
    loadingBreeds.value = false
  } else if (newAnimal.value.species) {
    // Load all breeds for this species (no country filter)
    loadingBreeds.value = true
    const result = await api.getBreeds({
      species: newAnimal.value.species,
      limit: 200
    })
    if (result.data?.breeds) {
      availableBreeds.value = result.data.breeds
    }
    loadingBreeds.value = false
  }
}

const createAnimal = async () => {
  if (!newAnimal.value.name || !newAnimal.value.species) {
    toast.error('Please fill in required fields (Name and Species)')
    return
  }

  creatingAnimal.value = true
  
  try {
    // Get current user info for owner_id
    const username = localStorage.getItem('username')
    
    const payload = {
      name: newAnimal.value.name,
      species: newAnimal.value.species,
      breed_id: newAnimal.value.breed_id ? parseInt(newAnimal.value.breed_id) : null,
      tag_id: newAnimal.value.tag_id || null,
      facility_id: newAnimal.value.facility_id ? parseInt(newAnimal.value.facility_id) : null,
      date_added: newAnimal.value.date_added || new Date().toISOString(),
      owner_id: 1 // Default owner for now - should be current user
    }

    const result = await api.createAnimal(payload)
    
    if (result.data) {
      toast.success('Animal created successfully!')
      showAddDialog.value = false
      resetNewAnimal()
      await loadAnimals() // Refresh the list
    } else {
      toast.error('Failed to create animal')
    }
  } catch (error: any) {
    toast.error(error.message || 'Failed to create animal')
  } finally {
    creatingAnimal.value = false
  }
}

const applyFilters = () => {
  currentPage.value = 1
  loadAnimals()
}

const changePage = (page: number) => {
  currentPage.value = page
  loadAnimals()
}

const viewAnimal = (id: number) => {
  router.push(`/animals/${id}`)
}

const editAnimal = (animal: any) => {
  // Navigate to animal detail page where edit dialog is available
  router.push(`/animals/${animal.id}`)
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

const getFacilityName = (facilityId: number | null) => {
  if (!facilityId) return 'No Facility'
  const facility = facilities.value.find(f => f.id === facilityId)
  return facility ? facility.name : 'Unknown'
}

onMounted(() => {
  loadAnimals()
  loadSpecies()
  loadFacilities()
  loadBreedSpecies()
})
</script>
