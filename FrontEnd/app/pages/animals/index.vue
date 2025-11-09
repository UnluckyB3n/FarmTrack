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
                  <UiTableCell>Facility #{{ animal.facility_id }}</UiTableCell>
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
  </NuxtLayout>
</template>

<script setup lang="ts">
const api = useApi()
const router = useRouter()

const searchQuery = ref('')
const selectedSpecies = ref('all')
const currentPage = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const showAddDialog = ref(false)

const animals = ref<any[]>([])
const total = ref(0)
const speciesList = ref<string[]>([])

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
  // TODO: Implement edit dialog
  console.log('Edit animal:', animal)
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleDateString()
}

onMounted(() => {
  loadAnimals()
  loadSpecies()
})
</script>
