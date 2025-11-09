<template>
  <NuxtLayout name="default">
    <div v-if="loading" class="flex justify-center items-center min-h-[400px]">
      <UiSpinner class="h-8 w-8" />
    </div>
    <div v-else-if="facility" class="space-y-6">
      <!-- Header -->
      <div class="flex items-start justify-between">
        <div>
          <h1 class="text-3xl font-bold">{{ facility.name }}</h1>
          <p class="text-muted-foreground mt-1">{{ facility.location }}</p>
        </div>
        <div class="flex gap-2">
          <UiButton variant="outline" @click="router.push('/facilities')">
            Back to Facilities
          </UiButton>
          <UiButton>Edit Facility</UiButton>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid gap-4 md:grid-cols-4">
        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Type</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <UiBadge>{{ facility.facility_type }}</UiBadge>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Total Animals</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ stats?.total_animals || 0 }}</div>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Active Animals</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ stats?.active_animals || 0 }}</div>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="pb-3">
            <UiCardTitle class="text-sm font-medium">Total Events</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ stats?.total_events || 0 }}</div>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Animals at This Facility -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Animals at this Facility</UiCardTitle>
          <UiCardDescription>Currently registered animals</UiCardDescription>
        </UiCardHeader>
        <UiCardContent>
          <div v-if="loadingAnimals" class="flex justify-center py-8">
            <UiSpinner />
          </div>
          <div v-else-if="animals && animals.length > 0">
            <div class="rounded-md border">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b bg-muted/50">
                    <th class="h-12 px-4 text-left align-middle font-medium">Name</th>
                    <th class="h-12 px-4 text-left align-middle font-medium">Tag ID</th>
                    <th class="h-12 px-4 text-left align-middle font-medium">Species</th>
                    <th class="h-12 px-4 text-left align-middle font-medium">Breed</th>
                    <th class="h-12 px-4 text-left align-middle font-medium">Status</th>
                    <th class="h-12 px-4 text-right align-middle font-medium">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="animal in animals"
                    :key="animal.id"
                    class="border-b transition-colors hover:bg-muted/50"
                  >
                    <td class="p-4 align-middle">{{ animal.name }}</td>
                    <td class="p-4 align-middle">{{ animal.tag_id }}</td>
                    <td class="p-4 align-middle">{{ animal.species }}</td>
                    <td class="p-4 align-middle">{{ animal.breed?.name || 'N/A' }}</td>
                    <td class="p-4 align-middle">
                      <UiBadge :variant="animal.date_of_death ? 'destructive' : 'default'">
                        {{ animal.date_of_death ? 'Deceased' : 'Active' }}
                      </UiBadge>
                    </td>
                    <td class="p-4 align-middle text-right">
                      <UiButton
                        variant="ghost"
                        size="sm"
                        @click="router.push(`/animals/${animal.id}`)"
                      >
                        View Details
                      </UiButton>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination -->
            <div class="mt-4 flex items-center justify-between pt-4 border-t">
              <p class="text-sm text-muted-foreground">
                Showing {{ animals.length }} of {{ totalAnimals }} animals
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
                  :disabled="currentPage * pageSize >= totalAnimals"
                  @click="changePage(currentPage + 1)"
                >
                  Next
                </UiButton>
              </div>
            </div>
          </div>
          <div v-else class="py-8 text-center text-muted-foreground">
            No animals registered at this facility
          </div>
        </UiCardContent>
      </UiCard>
    </div>
    <div v-else class="text-center py-12">
      <p class="text-muted-foreground">Facility not found</p>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const api = useApi()

const facilityId = computed(() => parseInt(route.params.id as string))

const facility = ref<any>(null)
const stats = ref<any>(null)
const animals = ref<any[]>([])
const totalAnimals = ref(0)

const loading = ref(true)
const loadingAnimals = ref(true)

const currentPage = ref(1)
const pageSize = ref(10)

const loadFacility = async () => {
  loading.value = true
  const result = await api.getFacility(facilityId.value)
  if (result.data) {
    facility.value = result.data
  }
  loading.value = false
}

const loadStats = async () => {
  const result = await api.getFacilityStats(facilityId.value)
  if (result.data) {
    stats.value = result.data
  }
}

const loadAnimals = async () => {
  loadingAnimals.value = true
  const params = {
    skip: (currentPage.value - 1) * pageSize.value,
    limit: pageSize.value,
  }
  const result = await api.getFacilityAnimals(facilityId.value, params)
  if (result.data) {
    animals.value = result.data.animals
    totalAnimals.value = result.data.total
  }
  loadingAnimals.value = false
}

const changePage = (page: number) => {
  currentPage.value = page
  loadAnimals()
}

onMounted(() => {
  loadFacility()
  loadStats()
  loadAnimals()
})
</script>
