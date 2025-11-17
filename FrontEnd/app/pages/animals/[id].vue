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
          <UiButton variant="outline" @click="openQRDialog">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/><path d="M21 21v.01"/><path d="M12 7v3a2 2 0 0 1-2 2H7"/><path d="M3 12h.01"/><path d="M12 3h.01"/><path d="M12 16v.01"/><path d="M16 12h1"/><path d="M21 12v.01"/><path d="M12 21v-1"/></svg>
            View QR Code
          </UiButton>
          <UiButton variant="outline" @click="downloadPDF">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
            Download PDF
          </UiButton>
          <UiButton variant="outline" @click="openTransferDialog">Transfer</UiButton>
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

      <!-- Documents -->
      <UiCard>
        <UiCardHeader>
          <div class="flex items-center justify-between">
            <div>
              <UiCardTitle>Documents</UiCardTitle>
              <UiCardDescription>Vaccination records, certificates, and other files</UiCardDescription>
            </div>
            <UiButton @click="openUploadDialog" size="sm">
              Upload Document
            </UiButton>
          </div>
        </UiCardHeader>
        <UiCardContent>
          <div v-if="loadingDocuments" class="flex justify-center py-8">
            <UiSpinner />
          </div>
          <div v-else-if="documents && documents.length > 0" class="space-y-3">
            <div
              v-for="doc in documents"
              :key="doc.id"
              class="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50"
            >
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                  <p class="font-medium text-sm truncate">{{ doc.file_name }}</p>
                  <UiBadge variant="outline" class="text-xs">{{ doc.document_type }}</UiBadge>
                </div>
                <p v-if="doc.description" class="text-xs text-muted-foreground mb-1">
                  {{ doc.description }}
                </p>
                <p class="text-xs text-muted-foreground">
                  {{ formatFileSize(doc.file_size) }} • Uploaded {{ formatDate(doc.uploaded_at) }} by {{ doc.uploaded_by }}
                </p>
              </div>
              <UiButton variant="ghost" size="sm" @click="deleteDoc(doc.id)">
                Delete
              </UiButton>
            </div>
          </div>
          <div v-else class="py-8 text-center text-muted-foreground">
            No documents uploaded yet
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

    <!-- Transfer Animal Dialog -->
    <UiDialog v-model:open="transferDialogOpen">
      <UiDialogContent>
        <UiDialogHeader>
          <UiDialogTitle>Transfer Animal</UiDialogTitle>
          <UiDialogDescription>
            Move {{ animal?.name }} to a different facility
          </UiDialogDescription>
        </UiDialogHeader>

        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <UiLabel>Current Facility</UiLabel>
            <div class="p-3 bg-muted rounded-md text-sm">
              {{ animal?.facility?.name || 'No facility' }}
              <span v-if="animal?.facility?.facility_type" class="text-muted-foreground">
                ({{ animal.facility.facility_type }})
              </span>
            </div>
          </div>

          <div class="space-y-2">
            <UiLabel for="new-facility">New Facility *</UiLabel>
            <UiSelect v-model="transferForm.to_facility_id">
              <UiSelectTrigger id="new-facility">
                <UiSelectValue placeholder="Select destination facility" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem 
                  v-for="facility in availableFacilities" 
                  :key="facility.id" 
                  :value="facility.id.toString()"
                >
                  {{ facility.name }} ({{ facility.facility_type }})
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>

          <div class="space-y-2">
            <UiLabel for="transfer-notes">Notes</UiLabel>
            <UiTextarea 
              id="transfer-notes" 
              v-model="transferForm.notes" 
              placeholder="Optional notes about this transfer"
              rows="3"
            />
          </div>
        </div>

        <UiDialogFooter>
          <UiButton variant="outline" @click="transferDialogOpen = false">Cancel</UiButton>
          <UiButton @click="transferAnimal" :disabled="!transferForm.to_facility_id">
            Transfer Animal
          </UiButton>
        </UiDialogFooter>
      </UiDialogContent>
    </UiDialog>

    <!-- QR Code Dialog -->
    <UiDialog v-model:open="qrDialogOpen">
      <UiDialogContent class="max-w-md">
        <UiDialogHeader>
          <UiDialogTitle>QR Code for {{ animal?.name }}</UiDialogTitle>
          <UiDialogDescription>
            Scan this code to view public traceability information
          </UiDialogDescription>
        </UiDialogHeader>

        <div class="space-y-4 py-4">
          <!-- QR Code Image -->
          <div class="flex justify-center bg-white p-6 rounded-lg border-2 border-primary/20">
            <img 
              :src="qrCodeUrl" 
              alt="Animal QR Code"
              class="w-64 h-64"
            />
          </div>

          <!-- Public URL -->
          <div class="space-y-2">
            <UiLabel>Public Tracking URL</UiLabel>
            <div class="flex gap-2">
              <UiInput 
                :value="publicUrl" 
                readonly 
                class="flex-1"
              />
              <UiButton 
                variant="outline" 
                size="sm"
                @click="copyPublicUrl"
              >
                {{ urlCopied ? '✓ Copied' : 'Copy' }}
              </UiButton>
            </div>
            <p class="text-xs text-muted-foreground">
              Anyone can scan the QR code or visit this URL to view traceability information
            </p>
          </div>

          <!-- Download QR Code -->
          <div class="flex gap-2">
            <UiButton 
              variant="outline" 
              class="flex-1"
              @click="downloadQRCode"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
              Download QR Code
            </UiButton>
            <UiButton 
              variant="outline" 
              class="flex-1"
              @click="printQRCode"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect width="12" height="8" x="6" y="14"/></svg>
              Print
            </UiButton>
          </div>
        </div>

        <UiDialogFooter>
          <UiButton @click="qrDialogOpen = false">Close</UiButton>
        </UiDialogFooter>
      </UiDialogContent>
    </UiDialog>

    <!-- Upload Document Dialog -->
    <UiDialog v-model:open="uploadDialogOpen">
      <UiDialogContent>
        <UiDialogHeader>
          <UiDialogTitle>Upload Document</UiDialogTitle>
          <UiDialogDescription>
            Upload a document for {{ animal?.name }}
          </UiDialogDescription>
        </UiDialogHeader>

        <div class="space-y-4 py-4">
          <div class="space-y-2">
            <UiLabel for="doc-type">Document Type *</UiLabel>
            <UiSelect v-model="uploadForm.document_type">
              <UiSelectTrigger id="doc-type">
                <UiSelectValue placeholder="Select document type" />
              </UiSelectTrigger>
              <UiSelectContent>
                <UiSelectItem 
                  v-for="type in documentTypes" 
                  :key="type.value" 
                  :value="type.value"
                >
                  {{ type.label }}
                </UiSelectItem>
              </UiSelectContent>
            </UiSelect>
          </div>

          <div class="space-y-2">
            <UiLabel for="doc-file">File *</UiLabel>
            <input 
              id="doc-file" 
              type="file" 
              @change="onFileChange"
              accept=".pdf,.jpg,.jpeg,.png,.doc,.docx,.txt"
              class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
            />
            <p class="text-xs text-muted-foreground">
              Max 10MB. Allowed: PDF, JPG, PNG, DOC, DOCX, TXT
            </p>
          </div>

          <div class="space-y-2">
            <UiLabel for="doc-description">Description</UiLabel>
            <UiTextarea 
              id="doc-description" 
              v-model="uploadForm.description" 
              placeholder="Optional notes about this document"
              rows="3"
            />
          </div>
        </div>

        <UiDialogFooter>
          <UiButton variant="outline" @click="uploadDialogOpen = false">Cancel</UiButton>
          <UiButton @click="uploadDocument" :disabled="!uploadForm.file || !uploadForm.document_type || uploading">
            <UiSpinner v-if="uploading" class="mr-2 h-4 w-4" />
            {{ uploading ? 'Uploading...' : 'Upload' }}
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

// Set page title
useHead({
  title: 'Animal Details - FarmTrack'
})

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

// Transfer dialog state
const transferDialogOpen = ref(false)
const transferForm = ref({
  to_facility_id: '',
  notes: ''
})
const availableFacilities = ref<any[]>([])

// Documents state
const documents = ref<any[]>([])
const loadingDocuments = ref(false)
const uploadDialogOpen = ref(false)
const uploadForm = ref({
  file: null as File | null,
  document_type: '',
  description: ''
})
const documentTypes = ref<any[]>([])
const uploading = ref(false)

// QR Code state
const qrDialogOpen = ref(false)
const qrCodeUrl = ref('')
const publicUrl = ref('')
const urlCopied = ref(false)

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatFileSize = (bytes: number) => {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

const loadAnimal = async () => {
  loading.value = true
  const result = await api.getAnimal(animalId.value)
  if (result.data) {
    animal.value = result.data
  }
  loading.value = false
}

const loadDocuments = async () => {
  loadingDocuments.value = true
  const result = await api.getAnimalDocuments(animalId.value)
  if (result.data?.documents) {
    documents.value = result.data.documents
  }
  loadingDocuments.value = false
}

const loadDocumentTypes = async () => {
  const result = await api.getDocumentTypes()
  if (result.data?.document_types) {
    documentTypes.value = result.data.document_types
  }
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

const openTransferDialog = async () => {
  // Reset form
  transferForm.value = {
    to_facility_id: '',
    notes: ''
  }
  
  // Load available facilities
  const result = await api.getFacilities()
  if (result.data?.facilities) {
    // Filter out the current facility
    availableFacilities.value = result.data.facilities.filter(
      (f: any) => f.id !== animal.value?.facility_id
    )
  }
  
  transferDialogOpen.value = true
}

const transferAnimal = async () => {
  if (!transferForm.value.to_facility_id) {
    return
  }

  const { data: userData } = await api.getCurrentUser()
  
  const payload = {
    to_facility_id: parseInt(transferForm.value.to_facility_id),
    actor_id: userData?.id,
    notes: transferForm.value.notes
  }

  const result = await api.transferAnimal(animalId.value, payload)
  
  if (result.data) {
    transferDialogOpen.value = false
    await loadAnimal()
    await loadEvents()
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

const openUploadDialog = async () => {
  uploadForm.value = {
    file: null,
    document_type: '',
    description: ''
  }
  
  await loadDocumentTypes()
  uploadDialogOpen.value = true
}

const onFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    uploadForm.value.file = target.files[0]
  }
}

const uploadDocument = async () => {
  if (!uploadForm.value.file || !uploadForm.value.document_type) return
  
  uploading.value = true
  
  const formData = new FormData()
  formData.append('file', uploadForm.value.file)
  formData.append('document_type', uploadForm.value.document_type)
  if (uploadForm.value.description) {
    formData.append('description', uploadForm.value.description)
  }
  
  const result = await api.uploadDocument(animalId.value, formData)
  
  if (result.data) {
    uploadDialogOpen.value = false
    await loadDocuments()
  }
  
  uploading.value = false
}

const deleteDoc = async (docId: number) => {
  if (!confirm('Are you sure you want to delete this document?')) return
  
  const result = await api.deleteDocument(docId)
  
  if (result.data) {
    await loadDocuments()
  }
}

const openQRDialog = () => {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiUrl || 'http://localhost:8000/api/v1'
  const frontendUrl = config.public.siteUrl || 'http://localhost:3000'
  
  // Set QR code URL (backend generates the QR image)
  qrCodeUrl.value = `${baseUrl}/animals/${animalId.value}/qr`
  
  // Set public tracking URL
  publicUrl.value = `${frontendUrl}/public/${animalId.value}`
  
  qrDialogOpen.value = true
  urlCopied.value = false
}

const copyPublicUrl = async () => {
  try {
    await navigator.clipboard.writeText(publicUrl.value)
    urlCopied.value = true
    setTimeout(() => {
      urlCopied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy URL:', err)
  }
}

const downloadQRCode = () => {
  // Create a link to download the QR code image
  const link = document.createElement('a')
  link.href = qrCodeUrl.value
  link.download = `animal_${animalId.value}_qr_code.png`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const printQRCode = () => {
  // Open QR code in new window for printing
  const printWindow = window.open(qrCodeUrl.value, '_blank')
  if (printWindow) {
    printWindow.onload = () => {
      printWindow.print()
    }
  }
}

const downloadPDF = () => {
  const token = localStorage.getItem('token')
  const url = api.downloadAnimalPDF(animalId.value)
  
  // Create a temporary link and trigger download
  const link = document.createElement('a')
  link.href = url + `?token=${token}`
  link.download = `animal_${animalId.value}_traceability_report.pdf`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  loadAnimal()
  loadEvents()
  loadDocuments()
})
</script>