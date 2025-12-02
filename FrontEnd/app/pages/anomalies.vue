<template>
  <NuxtLayout name="default">
    <div class="space-y-4">
      <!-- Header with Stats -->
      <div class="grid gap-4 md:grid-cols-3">
        <UiCard>
          <UiCardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <UiCardTitle class="text-sm font-medium">Total Anomalies</UiCardTitle>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="text-destructive"
            >
              <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3" />
              <path d="M12 9v4" />
              <path d="M12 17h.01" />
            </svg>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold text-destructive">{{ total }}</div>
            <p class="text-xs text-muted-foreground">Flagged events</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <UiCardTitle class="text-sm font-medium">Critical</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">{{ criticalCount }}</div>
            <p class="text-xs text-muted-foreground">Require immediate attention</p>
          </UiCardContent>
        </UiCard>

        <UiCard>
          <UiCardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
            <UiCardTitle class="text-sm font-medium">Resolution Rate</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <div class="text-2xl font-bold">65%</div>
            <p class="text-xs text-muted-foreground">Anomalies resolved</p>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- Anomalies List -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Detected Anomalies</UiCardTitle>
          <UiCardDescription>Events flagged by the plausibility engine</UiCardDescription>
        </UiCardHeader>
        <UiCardContent>
          <div v-if="loading" class="flex justify-center py-8">
            <UiSpinner />
          </div>
          <div v-else-if="anomalies && anomalies.length > 0" class="space-y-4">
            <div
              v-for="anomaly in anomalies"
              :key="anomaly.id"
              class="flex items-start justify-between border-l-4 border-destructive bg-destructive/5 p-4 rounded-r"
            >
              <div class="flex-1 space-y-2">
                <div class="flex items-center gap-2">
                  <UiBadge variant="destructive">{{ anomaly.event_type }}</UiBadge>
                  <span class="text-sm font-medium">
                    {{ anomaly.animal?.name }} ({{ anomaly.animal?.tag_id }})
                  </span>
                </div>
                <div class="space-y-1">
                  <p class="text-sm font-medium text-destructive">
                    ⚠️ {{ anomaly.anomaly_reason }}
                  </p>
                  <p class="text-xs text-muted-foreground">
                    {{ formatDate(anomaly.timestamp) }}
                  </p>
                  <p v-if="anomaly.metadata" class="text-xs text-muted-foreground">
                    {{ anomaly.metadata }}
                  </p>
                </div>
              </div>
              <div class="flex gap-2">
                <UiButton variant="outline" size="sm">
                  Investigate
                </UiButton>
                <UiButton variant="ghost" size="sm">
                  Dismiss
                </UiButton>
              </div>
            </div>

            <!-- Pagination -->
            <div class="mt-4 flex items-center justify-between pt-4 border-t">
              <p class="text-sm text-muted-foreground">
                Showing {{ anomalies.length }} of {{ total }} anomalies
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
            🎉 No anomalies detected
          </div>
        </UiCardContent>
      </UiCard>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const api = useApi()

const currentPage = ref(1)
const pageSize = ref(10)
const loading = ref(false)

const anomalies = ref<any[]>([])
const total = ref(0)
const criticalCount = ref(0)

const loadAnomalies = async () => {
  loading.value = true
  const params = {
    skip: (currentPage.value - 1) * pageSize.value,
    limit: pageSize.value,
  }

  const result = await api.getAnomalies(params)
  if (result.data) {
    anomalies.value = result.data.anomalies
    total.value = result.data.total
    // Count critical anomalies (simplified logic)
    criticalCount.value = anomalies.value.filter(a => 
      a.anomaly_reason?.includes('rapid') || a.anomaly_reason?.includes('inconsistent')
    ).length
  }
  loading.value = false
}

const changePage = (page: number) => {
  currentPage.value = page
  loadAnomalies()
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

onMounted(() => {
  loadAnomalies()
})
</script>
