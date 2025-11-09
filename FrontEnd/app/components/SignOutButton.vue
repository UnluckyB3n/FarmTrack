<template>
  <UiAlertDialog>
    <UiAlertDialogTrigger as-child>
      <slot>
        <UiButton variant="ghost" size="sm">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
            class="mr-2"
          >
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" x2="9" y1="12" y2="12" />
          </svg>
          Sign Out
        </UiButton>
      </slot>
    </UiAlertDialogTrigger>
    <UiAlertDialogContent>
      <UiAlertDialogHeader>
        <UiAlertDialogTitle>Sign Out</UiAlertDialogTitle>
        <UiAlertDialogDescription>
          Are you sure you want to sign out? You will need to log in again to access your account.
        </UiAlertDialogDescription>
      </UiAlertDialogHeader>
      <UiAlertDialogFooter>
        <UiAlertDialogCancel>Cancel</UiAlertDialogCancel>
        <UiAlertDialogAction @click="handleSignOut" class="bg-destructive hover:bg-destructive/90">
          Sign Out
        </UiAlertDialogAction>
      </UiAlertDialogFooter>
    </UiAlertDialogContent>
  </UiAlertDialog>
</template>

<script setup lang="ts">
const auth = useAuthManagement()
const signingOut = ref(false)

const handleSignOut = async () => {
  if (signingOut.value) return
  
  signingOut.value = true
  try {
    await auth.signOut()
  } catch (error) {
    console.error('Error signing out:', error)
  } finally {
    signingOut.value = false
  }
}
</script>
