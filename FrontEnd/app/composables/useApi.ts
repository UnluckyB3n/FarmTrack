export const useApi = () => {
  const config = useRuntimeConfig()
  
  // Use Docker service name for SSR (server-side), localhost for client-side
  const baseURL = process.server 
    ? 'http://traceability_api:8000/api/v1'
    : (config.public.apiUrl || 'http://localhost:8000/api/v1')

  const apiFetch = async (endpoint: string, options: any = {}) => {
    try {
      const response = await $fetch(`${baseURL}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      })
      return { data: response, error: null }
    } catch (error: any) {
      console.error('API Error:', error)
      const errorMessage = error?.data?.detail || error?.message || 'An error occurred'
      return { data: null, error: errorMessage }
    }
  }

  return {
    // Dashboard
    getDashboardOverview: () => apiFetch('/dashboard/overview'),
    getRecentEvents: (limit = 10) => apiFetch(`/dashboard/recent-events?limit=${limit}`),
    getEventTimeline: (days = 30) => apiFetch(`/dashboard/timeline?days=${days}`),
    getTopFacilities: (limit = 5) => apiFetch(`/dashboard/top-facilities?limit=${limit}`),
    getSpeciesDistribution: () => apiFetch('/dashboard/species-distribution'),

    // Animals
    getAnimals: (params: any = {}) => {
      const query = new URLSearchParams(params).toString()
      return apiFetch(`/animals/?${query}`)
    },
    getAnimal: (id: number) => apiFetch(`/animals/${id}`),
    createAnimal: (data: any) => apiFetch('/animals/', { method: 'POST', body: data }),
    updateAnimal: (id: number, data: any) => apiFetch(`/animals/${id}`, { method: 'PUT', body: data }),
    deleteAnimal: (id: number) => apiFetch(`/animals/${id}`, { method: 'DELETE' }),
    getAnimalEvents: (id: number) => apiFetch(`/animals/${id}/events`),
    getAnimalSpecies: () => apiFetch('/animals/species/'),
    getAnimalStats: () => apiFetch('/animals/stats/'),

    // Breeds
    getBreedSpecies: () => apiFetch('/breeds/species'),
    getBreeds: (params: any = {}) => {
      const query = new URLSearchParams(params).toString()
      return apiFetch(`/breeds/breeds?${query}`)
    },
    getBreedCountries: (species?: string) => {
      const query = species ? `?species=${species}` : ''
      return apiFetch(`/breeds/countries${query}`)
    },
    getBreedDetails: (id: number) => apiFetch(`/breeds/breeds/${id}`),

    // Facilities
    getFacilities: (params: any = {}) => {
      const query = new URLSearchParams(params).toString()
      return apiFetch(`/facilities/?${query}`)
    },
    getFacility: (id: number) => apiFetch(`/facilities/${id}`),
    createFacility: (data: any) => apiFetch('/facilities/', { method: 'POST', body: data }),
    updateFacility: (id: number, data: any) => apiFetch(`/facilities/${id}`, { method: 'PUT', body: data }),
    deleteFacility: (id: number) => apiFetch(`/facilities/${id}`, { method: 'DELETE' }),
    getFacilityAnimals: (id: number, params: any = {}) => {
      const query = new URLSearchParams(params).toString()
      return apiFetch(`/facilities/${id}/animals?${query}`)
    },
    getFacilityStats: (id: number) => apiFetch(`/facilities/${id}/stats`),
    getFacilityTypes: () => apiFetch('/facilities/types'),

    // Events
    getEvents: (params: any = {}) => {
      const query = new URLSearchParams(params).toString()
      return apiFetch(`/events/?${query}`)
    },
    getEvent: (id: number) => apiFetch(`/events/${id}`),
    createEvent: (data: any) => apiFetch('/events/', { method: 'POST', body: data }),
    getEventTypes: () => apiFetch('/events/types'),
    getAnomalies: (params: any = {}) => {
      const query = new URLSearchParams(params).toString()
      return apiFetch(`/events/anomalies?${query}`)
    },
    getEventStats: () => apiFetch('/events/stats'),

    // Users
    getUsers: (params: any = {}) => {
      const query = new URLSearchParams(params).toString()
      return apiFetch(`/users/?${query}`)
    },
    getUser: (id: number) => apiFetch(`/users/${id}`),
    createUser: (data: any) => apiFetch('/users/', { method: 'POST', body: data }),
    updateUser: (id: number, data: any) => apiFetch(`/users/${id}`, { method: 'PUT', body: data }),
    deleteUser: (id: number) => apiFetch(`/users/${id}`, { method: 'DELETE' }),

    // Auth
    login: async (username: string, password: string) => {
      try {
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)
        
        const response = await $fetch(`${baseURL}/auth/login`, {
          method: 'POST',
          body: formData.toString(),
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        })
        return { data: response, error: null }
      } catch (error: any) {
        console.error('Login Error:', error)
        const errorMessage = error?.data?.detail || error?.message || 'Invalid credentials'
        return { data: null, error: errorMessage }
      }
    },

    // Settings
    getProfile: (username: string) => apiFetch(`/settings/profile?username=${username}`),
    updateProfile: (username: string, data: any) => apiFetch(`/settings/profile?username=${username}`, { method: 'PUT', body: data }),
    getAccount: (username: string) => apiFetch(`/settings/account?username=${username}`),
    updateAccount: (username: string, data: any) => apiFetch(`/settings/account?username=${username}`, { method: 'PUT', body: data }),
    getNotifications: (username: string) => apiFetch(`/settings/notifications?username=${username}`),
    updateNotifications: (username: string, data: any) => apiFetch(`/settings/notifications?username=${username}`, { method: 'PUT', body: data }),
    changePassword: (username: string, data: any) => apiFetch(`/settings/password?username=${username}`, { method: 'POST', body: data }),
  }
}
