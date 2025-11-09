<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { ref, onMounted } from 'vue'
import * as z from 'zod'
import { useForm } from 'vee-validate'

import { Button } from '~/components/ui/button'
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '~/components/ui/form'
import { Input } from '~/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '~/components/ui/select'
import { Separator } from '~/components/ui/separator'

const settings = useSettings()
const loading = ref(false)

const languages = [
  { label: 'English', value: 'en' },
  { label: 'French', value: 'fr' },
  { label: 'German', value: 'de' },
  { label: 'Spanish', value: 'es' },
  { label: 'Portuguese', value: 'pt' },
  { label: 'Russian', value: 'ru' },
  { label: 'Japanese', value: 'ja' },
  { label: 'Korean', value: 'ko' },
  { label: 'Chinese', value: 'zh' },
] as const

const accountFormSchema = toTypedSchema(z.object({
  full_name: z
    .string()
    .min(2, {
      message: 'Name must be at least 2 characters.',
    })
    .max(100, {
      message: 'Name must not be longer than 100 characters.',
    })
    .optional()
    .or(z.literal('')),
  date_of_birth: z.string().optional().or(z.literal('')),
  language: z.string().min(1, 'Please select a language.'),
}))

const { handleSubmit, setValues } = useForm({
  validationSchema: accountFormSchema,
  initialValues: {
    full_name: '',
    date_of_birth: '',
    language: 'en',
  },
})

onMounted(async () => {
  await settings.loadAccount()
  if (settings.account.value) {
    setValues({
      full_name: settings.account.value.full_name || '',
      date_of_birth: settings.account.value.date_of_birth || '',
      language: settings.account.value.language || 'en',
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  const success = await settings.updateAccount(values)
  loading.value = false
  
  if (success) {
    await settings.loadAccount()
  }
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h3 class="text-lg font-medium">
        Account
      </h3>
      <p class="text-sm text-muted-foreground mt-1">
        Update your account settings. Set your preferred language and timezone.
      </p>
    </div>
    <Separator />
    <form class="space-y-6" @submit="onSubmit">
      <FormField v-slot="{ componentField }" name="full_name">
        <FormItem>
          <FormLabel>Full Name</FormLabel>
          <FormControl>
            <Input type="text" placeholder="Your full name" v-bind="componentField" />
          </FormControl>
          <FormDescription>
            This is the name that will be displayed on your profile and in emails.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <FormField v-slot="{ componentField }" name="date_of_birth">
        <FormItem>
          <FormLabel>Date of Birth</FormLabel>
          <FormControl>
            <Input type="date" v-bind="componentField" class="max-w-xs" />
          </FormControl>
          <FormDescription>
            Your date of birth is used to calculate your age.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <FormField v-slot="{ componentField }" name="language">
        <FormItem>
          <FormLabel>Language</FormLabel>
          <Select v-bind="componentField">
            <FormControl>
              <SelectTrigger class="max-w-xs">
                <SelectValue placeholder="Select a language" />
              </SelectTrigger>
            </FormControl>
            <SelectContent>
              <SelectItem v-for="language in languages" :key="language.value" :value="language.value">
                {{ language.label }}
              </SelectItem>
            </SelectContent>
          </Select>
          <FormDescription>
            This is the language that will be used in the dashboard.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <div class="flex gap-3 pt-4">
        <Button type="submit" :disabled="loading || settings.loading.value">
          {{ loading || settings.loading.value ? 'Updating...' : 'Update account' }}
        </Button>
      </div>
    </form>
  </div>
</template>