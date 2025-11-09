<template>
  <NuxtLayout name="default">
    <div class="space-y-4">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-medium">Facilities Management</h3>
          <p class="text-sm text-muted-foreground">Manage farms, processors, and retailers</p>
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
          Add Facility
        </UiButton>
      </div>

      <!-- Search and Filters -->
      <UiCard>
        <UiCardContent class="pt-6">
          <div class="flex gap-4">
            <div class="flex-1">
              <UiInput v-model="searchQuery" placeholder="Search facilities..." />
            </div>
            <UiSelect v-model="selectedType">
              <UiSelectTrigger class="w-[180px]">
                <UiSelectValue placeholder="All Types" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem value="all">All Types</UiSelectItem>
                <UiSelectItem value="farm">Farm</UiSelectItem>
                <UiSelectItem value="processor">Processor</UiSelectItem>
                <UiSelectItem value="retailer">Retailer</UiSelectItem>
              </UiSelectContent>
            </UiSelect>
            <UiButton variant="outline" @click="applyFilters">Apply</UiButton>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Facilities Grid -->
      <div v-if="loading" class="flex justify-center py-8">
        <UiSpinner />
      </div>
      <div v-else-if="facilities && facilities.length > 0" class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <UiCard v-for="facility in facilities" :key="facility.id" class="cursor-pointer hover:shadow-md transition-shadow" @click="viewFacility(facility.id)">
          <UiCardHeader>
            <div class="flex items-start justify-between">
              <div>
                <UiCardTitle class="text-lg">{{ facility.name }}</UiCardTitle>
                <UiCardDescription>{{ facility.location }}</UiCardDescription>
              </div>
              <UiBadge :variant="getFacilityBadgeVariant(facility.facility_type)">
                {{ facility.facility_type }}
              </UiBadge>
            </div>
          </UiCardHeader>
          <UiCardContent>
            <div class="flex items-center gap-4 text-sm text-muted-foreground">
              <div class="flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <circle cx="11" cy="4" r="2" />
                  <circle cx="18" cy="8" r="2" />
                </svg>
                <span>View details</span>
              </div>
            </div>
          </UiCardContent>
        </UiCard>
      </div>
      <div v-else class="py-8 text-center text-muted-foreground">
        No facilities found
      </div>

      <!-- Pagination -->
      <div v-if="facilities && facilities.length > 0" class="flex items-center justify-between">
        <p class="text-sm text-muted-foreground">
          Showing {{ facilities.length }} of {{ total }} facilities
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
  </NuxtLayout>
</template>

<script setup lang="ts">
const api = useApi()
const router = useRouter()

const searchQuery = ref('')
const selectedType = ref('all')
const currentPage = ref(1)
const pageSize = ref(12)
const loading = ref(false)

const facilities = ref<any[]>([])
const total = ref(0)

const loadFacilities = async () => {
  loading.value = true
  const params: any = {
    skip: (currentPage.value - 1) * pageSize.value,
    limit: pageSize.value,
  }

  if (searchQuery.value) {
    params.search = searchQuery.value
  }

  if (selectedType.value && selectedType.value !== 'all') {
    params.facility_type = selectedType.value
  }

  const result = await api.getFacilities(params)
  if (result.data) {
    facilities.value = result.data.facilities
    total.value = result.data.total
  }
  loading.value = false
}

const applyFilters = () => {
  currentPage.value = 1
  loadFacilities()
}

const changePage = (page: number) => {
  currentPage.value = page
  loadFacilities()
}

const viewFacility = (id: number) => {
  router.push(`/facilities/${id}`)
}

const getFacilityBadgeVariant = (type: string) => {
  switch (type) {
    case 'farm':
      return 'default'
    case 'processor':
      return 'secondary'
    case 'retailer':
      return 'outline'
    default:
      return 'outline'
  }
}

onMounted(() => {
  loadFacilities()
})
</script>
