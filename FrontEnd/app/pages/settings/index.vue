<template>
  <SettingsLayout>
    <ProfileForm />
  </SettingsLayout>
</template>

<script setup lang="ts">
import ProfileForm from '~/components/Settings/ProfileForm.vue'
import SettingsLayout from '~/layouts/SettingsLayout.vue'

definePageMeta({
  middleware: 'auth'
})
</script>
