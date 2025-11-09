<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { FieldArray, useForm } from 'vee-validate'
import { ref, onMounted } from 'vue'
import * as z from 'zod'
import { cn } from '@/lib/utils'
import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '~/components/ui/form'

import { Button } from '~/components/ui/button'
import { Input } from '~/components/ui/input'
import { Separator } from '~/components/ui/separator'
import { Textarea } from '~/components/ui/textarea'

const settings = useSettings()
const loading = ref(false)

const profileFormSchema = toTypedSchema(z.object({
  username: z
    .string()
    .min(2, {
      message: 'Username must be at least 2 characters.',
    })
    .max(30, {
      message: 'Username must not be longer than 30 characters.',
    }),
  email: z
    .string()
    .email({ message: 'Please enter a valid email address.' })
    .optional()
    .or(z.literal('')),
  full_name: z.string().max(100).optional().or(z.literal('')),
  bio: z.string().max(160, { message: 'Bio must not be longer than 160 characters.' }).optional().or(z.literal('')),
}))

const { handleSubmit, resetForm, setValues } = useForm({
  validationSchema: profileFormSchema,
  initialValues: {
    username: '',
    email: '',
    full_name: '',
    bio: '',
  },
})

onMounted(async () => {
  await settings.loadProfile()
  if (settings.profile.value) {
    setValues({
      username: settings.profile.value.username || '',
      email: settings.profile.value.email || '',
      full_name: settings.profile.value.full_name || '',
      bio: settings.profile.value.bio || '',
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  const success = await settings.updateProfile(values)
  loading.value = false
  
  if (success) {
    // Reload profile to get updated data
    await settings.loadProfile()
  }
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h3 class="text-lg font-medium">
        Profile
      </h3>
      <p class="text-sm text-muted-foreground mt-1">
        This is how others will see you on the site.
      </p>
    </div>
    <Separator />
    <form class="space-y-6" @submit="onSubmit">
      <FormField v-slot="{ componentField }" name="username">
        <FormItem>
          <FormLabel>Username</FormLabel>
          <FormControl>
            <Input type="text" placeholder="shadcn" v-bind="componentField" />
          </FormControl>
          <FormDescription>
            This is your public display name. It can be your real name or a pseudonym.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <FormField v-slot="{ componentField }" name="email">
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl>
            <Input type="email" placeholder="your.email@example.com" v-bind="componentField" />
          </FormControl>
          <FormDescription>
            Your email address for account recovery and notifications.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <FormField v-slot="{ componentField }" name="full_name">
        <FormItem>
          <FormLabel>Full Name</FormLabel>
          <FormControl>
            <Input type="text" placeholder="John Doe" v-bind="componentField" />
          </FormControl>
          <FormDescription>
            Your full name as it should appear on the platform.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <FormField v-slot="{ componentField }" name="bio">
        <FormItem>
          <FormLabel>Bio</FormLabel>
          <FormControl>
            <Textarea 
              placeholder="Tell us a little bit about yourself" 
              class="resize-none min-h-[100px]"
              v-bind="componentField" 
            />
          </FormControl>
          <FormDescription>
            Brief description for your profile. Maximum 160 characters.
          </FormDescription>
          <FormMessage />
        </FormItem>
      </FormField>

      <div class="flex gap-3 pt-4">
        <Button type="submit" :disabled="loading || settings.loading.value">
          {{ loading || settings.loading.value ? 'Updating...' : 'Update profile' }}
        </Button>

        <Button
          type="button"
          variant="outline"
          @click="resetForm"
          :disabled="loading || settings.loading.value"
        >
          Reset
        </Button>
      </div>
    </form>
  </div>
</template>