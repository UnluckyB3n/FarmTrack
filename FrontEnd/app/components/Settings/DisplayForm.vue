<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { toast } from 'vue-sonner'
import { ref, onMounted } from 'vue'
import * as z from 'zod'
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '~/components/ui/form'
import { Button } from '~/components/ui/button'
import { Checkbox } from '~/components/ui/checkbox'
import { Separator } from '~/components/ui/separator'

const loading = ref(false)

const items = [
  {
    id: 'dashboard',
    label: 'Dashboard',
  },
  {
    id: 'animals',
    label: 'Animals',
  },
  {
    id: 'facilities',
    label: 'Facilities',
  },
  {
    id: 'events',
    label: 'Events',
  },
  {
    id: 'reports',
    label: 'Reports',
  },
  {
    id: 'settings',
    label: 'Settings',
  },
] as const

const displayFormSchema = toTypedSchema(z.object({
  items: z.array(z.string()).refine(value => value.some(item => item), {
    message: 'You have to select at least one item.',
  }),
}))

// Load saved items from localStorage or use defaults
const getSavedItems = () => {
  if (process.client) {
    const saved = localStorage.getItem('sidebar-display-items')
    if (saved) {
      try {
        return JSON.parse(saved)
      } catch (e) {
        console.error('Error parsing saved display items:', e)
      }
    }
  }
  return ['dashboard', 'animals', 'facilities', 'events']
}

const { handleSubmit, setValues } = useForm({
  validationSchema: displayFormSchema,
  initialValues: {
    items: getSavedItems(),
  },
})

// Load saved items on mount
onMounted(() => {
  const savedItems = getSavedItems()
  setValues({ items: savedItems })
})

const onSubmit = handleSubmit((values) => {
  loading.value = true
  
  try {
    // Save to localStorage
    localStorage.setItem('sidebar-display-items', JSON.stringify(values.items))
    
    toast.success('Display settings updated! Refreshing page...')
    
    // Reload the page after a short delay to apply changes
    setTimeout(() => {
      window.location.reload()
    }, 1000)
  } catch (error) {
    toast.error('Failed to update display settings')
    loading.value = false
  }
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h3 class="text-lg font-medium">
        Display
      </h3>
      <p class="text-sm text-muted-foreground mt-1">
        Turn items on or off to control what's displayed in the app.
      </p>
    </div>
    <Separator />
    <form class="space-y-6" @submit="onSubmit">
      <FormField name="items">
        <FormItem>
          <div class="mb-4">
            <FormLabel class="text-base">
              Sidebar Navigation
            </FormLabel>
            <FormDescription>
              Select the items you want to display in the sidebar.
            </FormDescription>
          </div>

          <div class="space-y-3">
            <FormField v-for="item in items" v-slot="{ value, handleChange }" :key="item.id" name="items">
              <FormItem :key="item.id" class="flex flex-row items-center space-x-3 space-y-0 rounded-lg border p-3">
                <FormControl>
                  <Checkbox
                    :model-value="value.includes(item.id)"
                    @update:model-value="(checked) => {
                      if (Array.isArray(value)) {
                        handleChange(checked ? [...value, item.id] : value.filter(id => id !== item.id))
                      }
                    }"
                  />
                </FormControl>
                <FormLabel class="font-normal cursor-pointer flex-1">
                  {{ item.label }}
                </FormLabel>
              </FormItem>
            </FormField>
          </div>
          <FormMessage />
        </FormItem>
      </FormField>

      <div class="flex gap-3 pt-4">
        <Button type="submit" :disabled="loading">
          {{ loading ? 'Updating...' : 'Update display' }}
        </Button>
      </div>
    </form>
  </div>
</template>