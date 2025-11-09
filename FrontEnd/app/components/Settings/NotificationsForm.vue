<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { ref, onMounted } from 'vue'
import * as z from 'zod'

import { FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from '~/components/ui/form'
import { Button } from '~/components/ui/button'
import { Separator } from '~/components/ui/separator'
import { Switch } from '~/components/ui/switch'

const settings = useSettings()
const loading = ref(false)

const notificationsFormSchema = toTypedSchema(z.object({
  mobile_notifications: z.boolean().default(false).optional(),
  communication_emails: z.boolean().default(false).optional(),
  social_emails: z.boolean().default(false).optional(),
  marketing_emails: z.boolean().default(false).optional(),
  security_emails: z.boolean().default(true),
}))

const { handleSubmit, setValues } = useForm({
  validationSchema: notificationsFormSchema,
  initialValues: {
    communication_emails: false,
    marketing_emails: false,
    social_emails: true,
    security_emails: true,
    mobile_notifications: false,
  },
})

onMounted(async () => {
  await settings.loadNotifications()
  if (settings.notifications.value) {
    setValues({
      communication_emails: settings.notifications.value.communication_emails ?? false,
      marketing_emails: settings.notifications.value.marketing_emails ?? false,
      social_emails: settings.notifications.value.social_emails ?? true,
      security_emails: settings.notifications.value.security_emails ?? true,
      mobile_notifications: settings.notifications.value.mobile_notifications ?? false,
    })
  }
})

const onSubmit = handleSubmit(async (values) => {
  loading.value = true
  const success = await settings.updateNotifications(values)
  loading.value = false
  
  if (success) {
    await settings.loadNotifications()
  }
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h3 class="text-lg font-medium">
        Notifications
      </h3>
      <p class="text-sm text-muted-foreground mt-1">
        Configure how you receive notifications.
      </p>
    </div>
    <Separator />
    <form class="space-y-6" @submit="onSubmit">
      <div>
        <h3 class="mb-4 text-base font-medium">Email Notifications</h3>
        <div class="space-y-3">
          <FormField v-slot="{ value, handleChange }" name="communication_emails">
            <FormItem class="flex flex-row items-center justify-between rounded-lg border p-4">
              <div class="space-y-0.5 pr-4">
                <FormLabel class="text-base">
                  Communication emails
                </FormLabel>
                <FormDescription>
                  Receive emails about your account activity.
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  :checked="value"
                  @update:checked="handleChange"
                />
              </FormControl>
            </FormItem>
          </FormField>
          
          <FormField v-slot="{ value, handleChange }" name="marketing_emails">
            <FormItem class="flex flex-row items-center justify-between rounded-lg border p-4">
              <div class="space-y-0.5 pr-4">
                <FormLabel class="text-base">
                  Marketing emails
                </FormLabel>
                <FormDescription>
                  Receive emails about new products, features, and more.
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  :checked="value"
                  @update:checked="handleChange"
                />
              </FormControl>
            </FormItem>
          </FormField>
          
          <FormField v-slot="{ value, handleChange }" name="social_emails">
            <FormItem class="flex flex-row items-center justify-between rounded-lg border p-4">
              <div class="space-y-0.5 pr-4">
                <FormLabel class="text-base">
                  Social emails
                </FormLabel>
                <FormDescription>
                  Receive emails for friend requests, follows, and more.
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  :checked="value"
                  @update:checked="handleChange"
                />
              </FormControl>
            </FormItem>
          </FormField>
          
          <FormField v-slot="{ value, handleChange }" name="security_emails">
            <FormItem class="flex flex-row items-center justify-between rounded-lg border p-4 bg-muted/50">
              <div class="space-y-0.5 pr-4">
                <FormLabel class="text-base">
                  Security emails
                </FormLabel>
                <FormDescription>
                  Receive emails about your account security (required).
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  :checked="value"
                  @update:checked="handleChange"
                  disabled
                />
              </FormControl>
            </FormItem>
          </FormField>
        </div>
      </div>

      <div>
        <h3 class="mb-4 text-base font-medium">Mobile</h3>
        <FormField v-slot="{ value, handleChange }" name="mobile_notifications">
          <FormItem class="flex flex-row items-center justify-between rounded-lg border p-4">
            <div class="space-y-0.5 pr-4">
              <FormLabel class="text-base">
                Push notifications
              </FormLabel>
              <FormDescription>
                Receive push notifications on your mobile device.
              </FormDescription>
            </div>
            <FormControl>
              <Switch
                :checked="value"
                @update:checked="handleChange"
              />
            </FormControl>
          </FormItem>
        </FormField>
      </div>

      <div class="flex gap-3 pt-4">
        <Button type="submit" :disabled="loading || settings.loading.value">
          {{ loading || settings.loading.value ? 'Updating...' : 'Update notifications' }}
        </Button>
      </div>
    </form>
  </div>
</template>