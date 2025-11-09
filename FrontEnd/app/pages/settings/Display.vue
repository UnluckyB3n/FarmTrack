<template>
  <SettingsLayout>
    <DisplayForm />
  </SettingsLayout>
</template>

<script setup lang="ts">
import DisplayForm from '~/components/Settings/DisplayForm.vue'
import SettingsLayout from '~/layouts/SettingsLayout.vue'

definePageMeta({
  middleware: 'auth'
})
</script>
