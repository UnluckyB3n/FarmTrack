<template>
  <NuxtLayout name="default">
    <div class="space-y-6">
      <div>
        <h1 class="text-3xl font-bold">API Documentation</h1>
        <p class="text-muted-foreground mt-2">
          Comprehensive API reference for FarmTrack
        </p>
      </div>

      <!-- Quick Links -->
      <div class="grid gap-4 md:grid-cols-3">
        <UiCard class="hover:bg-muted/50 cursor-pointer" @click="openDocs('swagger')">
          <UiCardHeader>
            <UiCardTitle class="text-lg">Swagger UI</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <p class="text-sm text-muted-foreground">
              Interactive API documentation with try-it-out functionality
            </p>
          </UiCardContent>
        </UiCard>

        <UiCard class="hover:bg-muted/50 cursor-pointer" @click="openDocs('redoc')">
          <UiCardHeader>
            <UiCardTitle class="text-lg">ReDoc</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <p class="text-sm text-muted-foreground">
              Clean, responsive API documentation viewer
            </p>
          </UiCardContent>
        </UiCard>

        <UiCard class="hover:bg-muted/50 cursor-pointer" @click="openDocs('openapi')">
          <UiCardHeader>
            <UiCardTitle class="text-lg">OpenAPI Spec</UiCardTitle>
          </UiCardHeader>
          <UiCardContent>
            <p class="text-sm text-muted-foreground">
              Download the raw OpenAPI 3.0 specification JSON
            </p>
          </UiCardContent>
        </UiCard>
      </div>

      <!-- API Overview -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>API Overview</UiCardTitle>
          <UiCardDescription>
            FarmTrack API v1.0.0 - Livestock Traceability System
          </UiCardDescription>
        </UiCardHeader>
        <UiCardContent class="space-y-4">
          <div>
            <h3 class="font-semibold mb-2">Base URL</h3>
            <code class="bg-muted px-3 py-1 rounded text-sm">{{ baseUrl }}</code>
          </div>

          <div>
            <h3 class="font-semibold mb-2">Authentication</h3>
            <p class="text-sm text-muted-foreground mb-2">
              Most endpoints require JWT authentication. Include the token in the Authorization header:
            </p>
            <code class="bg-muted px-3 py-1 rounded text-sm block">
              Authorization: Bearer &lt;your_token&gt;
            </code>
          </div>

          <div>
            <h3 class="font-semibold mb-2">Getting Started</h3>
            <ol class="list-decimal list-inside space-y-2 text-sm text-muted-foreground">
              <li>Register a new account: <code>POST /api/v1/auth/register</code></li>
              <li>Login to get access token: <code>POST /api/v1/auth/login</code></li>
              <li>Include token in Authorization header for authenticated requests</li>
              <li>Explore the interactive Swagger UI for testing endpoints</li>
            </ol>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- Available Endpoints -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>Available Endpoints</UiCardTitle>
        </UiCardHeader>
        <UiCardContent>
          <div class="space-y-6">
            <div v-for="category in apiCategories" :key="category.name">
              <h3 class="font-semibold text-lg mb-3">{{ category.name }}</h3>
              <p class="text-sm text-muted-foreground mb-3">{{ category.description }}</p>
              <div class="space-y-2">
                <div 
                  v-for="endpoint in category.endpoints" 
                  :key="endpoint.path"
                  class="flex items-start gap-3 p-3 border rounded-lg"
                >
                  <UiBadge :variant="getMethodVariant(endpoint.method)" class="mt-0.5">
                    {{ endpoint.method }}
                  </UiBadge>
                  <div class="flex-1 min-w-0">
                    <code class="text-sm">{{ endpoint.path }}</code>
                    <p class="text-xs text-muted-foreground mt-1">{{ endpoint.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </UiCardContent>
      </UiCard>

      <!-- User Roles -->
      <UiCard>
        <UiCardHeader>
          <UiCardTitle>User Roles</UiCardTitle>
        </UiCardHeader>
        <UiCardContent>
          <div class="grid gap-4 md:grid-cols-3">
            <div class="space-y-2">
              <UiBadge>farmer</UiBadge>
              <p class="text-sm text-muted-foreground">
                Can manage their own animals and facilities
              </p>
            </div>
            <div class="space-y-2">
              <UiBadge variant="secondary">processor</UiBadge>
              <p class="text-sm text-muted-foreground">
                Can process animals and manage processing facilities
              </p>
            </div>
            <div class="space-y-2">
              <UiBadge variant="outline">regulator</UiBadge>
              <p class="text-sm text-muted-foreground">
                Can view all data for compliance and auditing
              </p>
            </div>
          </div>
        </UiCardContent>
      </UiCard>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()
const baseUrl = config.public.apiUrl || 'http://localhost:8000/api/v1'

const openDocs = (type: string) => {
  const urls = {
    swagger: 'http://localhost:8000/docs',
    redoc: 'http://localhost:8000/redoc',
    openapi: 'http://localhost:8000/openapi.json'
  }
  window.open(urls[type as keyof typeof urls], '_blank')
}

const getMethodVariant = (method: string) => {
  const variants: Record<string, any> = {
    GET: 'default',
    POST: 'secondary',
    PUT: 'outline',
    DELETE: 'destructive'
  }
  return variants[method] || 'default'
}

const apiCategories = [
  {
    name: 'Authentication',
    description: 'User authentication and registration',
    endpoints: [
      { method: 'POST', path: '/auth/login', description: 'Login and obtain JWT token' },
      { method: 'POST', path: '/auth/register', description: 'Register new user account' },
      { method: 'GET', path: '/auth/me', description: 'Get current user information' },
      { method: 'POST', path: '/auth/forgot-password', description: 'Request password reset token' },
      { method: 'POST', path: '/auth/reset-password', description: 'Reset password with token' }
    ]
  },
  {
    name: 'Animals',
    description: 'Manage animals, track movements, and generate QR codes',
    endpoints: [
      { method: 'GET', path: '/animals/', description: 'List all animals with pagination and filtering' },
      { method: 'POST', path: '/animals/', description: 'Create a new animal' },
      { method: 'GET', path: '/animals/{id}', description: 'Get animal details by ID' },
      { method: 'PUT', path: '/animals/{id}', description: 'Update animal information' },
      { method: 'DELETE', path: '/animals/{id}', description: 'Delete an animal' },
      { method: 'GET', path: '/animals/{id}/events', description: 'Get all events for an animal' },
      { method: 'GET', path: '/animals/{id}/qr', description: 'Generate QR code for animal' },
      { method: 'POST', path: '/animals/{id}/transfer', description: 'Transfer animal to new facility' },
      { method: 'GET', path: '/animals/{id}/movement-history', description: 'Get complete movement history' }
    ]
  },
  {
    name: 'Events',
    description: 'Record and query lifecycle events',
    endpoints: [
      { method: 'GET', path: '/events/', description: 'List all events with filtering' },
      { method: 'POST', path: '/events/', description: 'Create a new event' },
      { method: 'GET', path: '/events/{id}', description: 'Get event details by ID' },
      { method: 'GET', path: '/events/types', description: 'Get available event types' },
      { method: 'GET', path: '/events/anomalies', description: 'List events with anomalies' }
    ]
  },
  {
    name: 'Facilities',
    description: 'Manage farms, processors, and retailers',
    endpoints: [
      { method: 'GET', path: '/facilities/', description: 'List all facilities' },
      { method: 'POST', path: '/facilities/', description: 'Create a new facility' },
      { method: 'GET', path: '/facilities/{id}', description: 'Get facility details' },
      { method: 'PUT', path: '/facilities/{id}', description: 'Update facility information' },
      { method: 'DELETE', path: '/facilities/{id}', description: 'Delete a facility' },
      { method: 'GET', path: '/facilities/{id}/animals', description: 'List animals at facility' }
    ]
  },
  {
    name: 'Documents',
    description: 'Upload and manage documents',
    endpoints: [
      { method: 'POST', path: '/animals/{id}/documents', description: 'Upload document for animal' },
      { method: 'GET', path: '/animals/{id}/documents', description: 'List animal documents' },
      { method: 'GET', path: '/documents/{id}', description: 'Get document details' },
      { method: 'DELETE', path: '/documents/{id}', description: 'Delete a document' },
      { method: 'GET', path: '/documents/types', description: 'Get document types' }
    ]
  },
  {
    name: 'Breeds',
    description: 'Browse animal breed database',
    endpoints: [
      { method: 'GET', path: '/breeds/species', description: 'List available species' },
      { method: 'GET', path: '/breeds/countries', description: 'List countries by species' },
      { method: 'GET', path: '/breeds/breeds', description: 'Search breeds with filters' }
    ]
  },
  {
    name: 'Dashboard',
    description: 'Analytics and statistics',
    endpoints: [
      { method: 'GET', path: '/dashboard/overview', description: 'Get dashboard overview stats' },
      { method: 'GET', path: '/dashboard/recent-events', description: 'Get recent events' },
      { method: 'GET', path: '/dashboard/timeline', description: 'Get event timeline' }
    ]
  }
]
</script>
