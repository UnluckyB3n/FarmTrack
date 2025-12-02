<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { ChevronDown } from 'lucide-vue-next'
import { useForm } from 'vee-validate'
import { toast } from 'vue-sonner'
import { ref, watch, onMounted } from 'vue'

import * as z from 'zod'
import { cn } from '@/lib/utils'
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '~/components/ui/form'
import { RadioGroup, RadioGroupItem } from '~/components/ui/radio-group'
import { Button, buttonVariants } from '~/components/ui/button'
import { Separator } from '~/components/ui/separator'

const colorMode = useColorMode()
const loading = ref(false)

const appearanceFormSchema = toTypedSchema(z.object({
  theme: z.enum(['light', 'dark'], {
    required_error: 'Please select a theme.',
  }),
  font: z.enum(['inter', 'manrope', 'system'], {
    invalid_type_error: 'Select a font',
    required_error: 'Please select a font.',
  }),
}))

const { handleSubmit, setFieldValue } = useForm({
  validationSchema: appearanceFormSchema,
  initialValues: {
    theme: 'light',
    font: 'inter',
  },
})

// Load saved preferences on mount
onMounted(() => {
  // Load theme from colorMode
  const currentTheme = colorMode.preference as 'light' | 'dark'
  setFieldValue('theme', currentTheme === 'dark' ? 'dark' : 'light')
  
  // Load font from localStorage
  const savedFont = localStorage.getItem('font-preference') as 'inter' | 'manrope' | 'system' | null
  if (savedFont) {
    setFieldValue('font', savedFont)
  }
})

const onSubmit = handleSubmit((values) => {
  loading.value = true
  
  try {
    // Update color mode - this will trigger the theme change
    colorMode.preference = values.theme
    
    // Save font preference to localStorage
    if (values.font) {
      localStorage.setItem('font-preference', values.font)
      // Apply font class to body
      document.body.className = document.body.className.replace(/font-\w+/g, '')
      document.body.classList.add(`font-${values.font}`)
    }
    
    toast.success('Appearance settings updated successfully!')
  } catch (error) {
    toast.error('Failed to update appearance settings')
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h3 class="text-lg font-medium">
        Appearance
      </h3>
      <p class="text-sm text-muted-foreground mt-1">
        Customize the appearance of the app. Automatically switch between day and night themes.
      </p>
    </div>
    <Separator />
    <form class="space-y-8" @submit="onSubmit">
      <FormField v-slot="{ componentField }" type="radio" name="theme">
        <FormItem class="space-y-3">
          <FormLabel class="text-base">Theme</FormLabel>
          <FormDescription>
            Select the theme for the dashboard.
          </FormDescription>
          <FormMessage />

          <RadioGroup
            class="grid max-w-md grid-cols-2 gap-6 pt-2"
            v-bind="componentField"
          >
            <FormItem>
              <FormLabel class="[&:has([data-state=checked])>div]:border-primary cursor-pointer">
                <FormControl>
                  <RadioGroupItem value="light" class="sr-only" />
                </FormControl>
                <div class="items-center rounded-md border-2 border-muted p-1 hover:border-accent transition-colors">
                  <div class="space-y-2 rounded-sm bg-[#ecedef] p-2">
                    <div class="space-y-2 rounded-md bg-white p-2 shadow-sm">
                      <div class="h-2 w-20 rounded-lg bg-[#ecedef]" />
                      <div class="h-2 w-[100px] rounded-lg bg-[#ecedef]" />
                    </div>
                    <div class="flex items-center space-x-2 rounded-md bg-white p-2 shadow-sm">
                      <div class="h-4 w-4 rounded-full bg-[#ecedef]" />
                      <div class="h-2 w-[100px] rounded-lg bg-[#ecedef]" />
                    </div>
                    <div class="flex items-center space-x-2 rounded-md bg-white p-2 shadow-sm">
                      <div class="h-4 w-4 rounded-full bg-[#ecedef]" />
                      <div class="h-2 w-[100px] rounded-lg bg-[#ecedef]" />
                    </div>
                  </div>
                </div>
                <span class="block w-full p-2 text-center font-normal">
                  Light
                </span>
              </FormLabel>
            </FormItem>
            <FormItem>
              <FormLabel class="[&:has([data-state=checked])>div]:border-primary cursor-pointer">
                <FormControl>
                  <RadioGroupItem value="dark" class="sr-only" />
                </FormControl>
                <div class="items-center rounded-md border-2 border-muted bg-popover p-1 hover:bg-accent hover:text-accent-foreground transition-colors">
                  <div class="space-y-2 rounded-sm bg-slate-950 p-2">
                    <div class="space-y-2 rounded-md bg-slate-800 p-2 shadow-sm">
                      <div class="h-2 w-20 rounded-lg bg-slate-400" />
                      <div class="h-2 w-[100px] rounded-lg bg-slate-400" />
                    </div>
                    <div class="flex items-center space-x-2 rounded-md bg-slate-800 p-2 shadow-sm">
                      <div class="h-4 w-4 rounded-full bg-slate-400" />
                      <div class="h-2 w-[100px] rounded-lg bg-slate-400" />
                    </div>
                    <div class="flex items-center space-x-2 rounded-md bg-slate-800 p-2 shadow-sm">
                      <div class="h-4 w-4 rounded-full bg-slate-400" />
                      <div class="h-2 w-[100px] rounded-lg bg-slate-400" />
                    </div>
                  </div>
                </div>
                <span class="block w-full p-2 text-center font-normal">
                  Dark
                </span>
              </FormLabel>
            </FormItem>
          </RadioGroup>
        </FormItem>
      </FormField>

      <FormField v-slot="{ field }" name="font">
        <FormItem>
          <FormLabel class="text-base">Font</FormLabel>
          <div class="relative w-full max-w-xs">
            <FormControl>
              <select
                :class="cn(
                  buttonVariants({ variant: 'outline' }),
                  'w-full appearance-none font-normal',
                )"
                v-bind="field"
              >
                <option value="inter">
                  Inter
                </option>
                <option value="manrope">
                  Manrope
                </option>
                <option value="system">
                  System
                </option>
              </select>
            </FormControl>
            <ChevronDown class="pointer-events-none absolute right-3 top-2.5 h-4 w-4 opacity-50" />
          </div>
          <FormDescription>
            Set the font you want to use in the dashboard.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <div class="flex gap-2 pt-4">
        <Button type="submit" :disabled="loading">
          {{ loading ? 'Updating...' : 'Update preferences' }}
        </Button>
      </div>
    </form>
  </div>
</template>