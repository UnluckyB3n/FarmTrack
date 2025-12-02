<template>
  <div class="min-h-screen flex">
    <!-- Left side - Branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-primary to-primary/80 p-12 text-white flex-col justify-between">
      <div>
        <h1 class="text-4xl font-bold mb-4">FarmTrack</h1>
        <p class="text-lg opacity-90">Livestock Traceability System</p>
      </div>
      <div>
        <p class="text-sm opacity-75">
          Reset your password to regain access to your account.
        </p>
      </div>
    </div>

    <!-- Right side - Reset Form -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-md space-y-8">
        <div class="text-center">
          <h2 class="text-3xl font-bold">Forgot Password</h2>
          <p class="text-muted-foreground mt-2">
            Enter your email to receive a reset token
          </p>
        </div>

        <!-- Step 1: Request Token -->
        <div v-if="!tokenReceived" class="space-y-4">
          <UiCard>
            <UiCardContent class="pt-6">
              <form @submit.prevent="requestReset" class="space-y-4">
                <div class="space-y-2">
                  <UiLabel for="email">Email Address</UiLabel>
                  <UiInput
                    id="email"
                    v-model="email"
                    type="email"
                    placeholder="you@example.com"
                    required
                  />
                </div>

                <UiButton type="submit" class="w-full" :disabled="loading">
                  <UiSpinner v-if="loading" class="mr-2 h-4 w-4" />
                  {{ loading ? 'Sending...' : 'Send Reset Token' }}
                </UiButton>
              </form>
            </UiCardContent>
          </UiCard>

          <div class="text-center">
            <NuxtLink to="/login" class="text-sm text-primary hover:underline">
              Back to Login
            </NuxtLink>
          </div>
        </div>

        <!-- Step 2: Enter Token and New Password -->
        <div v-else class="space-y-4">
          <!-- Dev Mode: Show Token -->
          <UiAlert v-if="resetToken" class="bg-primary/10 border-primary">
            <div class="space-y-2">
              <p class="font-semibold text-sm">Development Mode - Reset Token:</p>
              <code class="text-xs break-all block bg-background p-2 rounded">
                {{ resetToken }}
              </code>
              <p class="text-xs text-muted-foreground">
                In production, this would be sent to {{ email }} via email.
              </p>
            </div>
          </UiAlert>

          <UiCard>
            <UiCardContent class="pt-6">
              <form @submit.prevent="resetPassword" class="space-y-4">
                <div class="space-y-2">
                  <UiLabel for="token">Reset Token</UiLabel>
                  <UiInput
                    id="token"
                    v-model="token"
                    placeholder="Paste your reset token"
                    required
                  />
                  <p class="text-xs text-muted-foreground">
                    Token expires in 1 hour
                  </p>
                </div>

                <div class="space-y-2">
                  <UiLabel for="new-password">New Password</UiLabel>
                  <UiInput
                    id="new-password"
                    v-model="newPassword"
                    type="password"
                    placeholder="Enter new password"
                    required
                  />
                </div>

                <div class="space-y-2">
                  <UiLabel for="confirm-password">Confirm Password</UiLabel>
                  <UiInput
                    id="confirm-password"
                    v-model="confirmPassword"
                    type="password"
                    placeholder="Confirm new password"
                    required
                  />
                </div>

                <UiButton type="submit" class="w-full" :disabled="loading || !passwordsMatch">
                  <UiSpinner v-if="loading" class="mr-2 h-4 w-4" />
                  {{ loading ? 'Resetting...' : 'Reset Password' }}
                </UiButton>

                <p v-if="!passwordsMatch && confirmPassword" class="text-sm text-destructive">
                  Passwords do not match
                </p>
              </form>
            </UiCardContent>
          </UiCard>

          <div class="text-center">
            <button @click="startOver" class="text-sm text-primary hover:underline">
              Request new token
            </button>
          </div>
        </div>

        <!-- Error Display -->
        <UiAlert v-if="error" variant="destructive">
          {{ error }}
        </UiAlert>

        <!-- Success Display -->
        <UiAlert v-if="success" class="bg-green-50 border-green-200">
          <p class="text-green-800">{{ success }}</p>
          <NuxtLink to="/login" class="text-sm text-green-600 hover:underline mt-2 block">
            Go to Login
          </NuxtLink>
        </UiAlert>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false
})

const api = useApi()
const router = useRouter()

const email = ref('')
const token = ref('')
const resetToken = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
const tokenReceived = ref(false)

const passwordsMatch = computed(() => {
  if (!newPassword.value || !confirmPassword.value) return true
  return newPassword.value === confirmPassword.value
})

const requestReset = async () => {
  if (!email.value) return
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const result = await api.forgotPassword(email.value)
    
    if (result.error) {
      error.value = result.error
      return
    }
    
    if (result.data?.dev_mode && result.data?.reset_token) {
      // Development mode - show token
      resetToken.value = result.data.reset_token
      token.value = result.data.reset_token
      tokenReceived.value = true
    } else {
      // Production mode - token sent via email
      tokenReceived.value = true
    }
  } catch (err: any) {
    error.value = err.message || 'Failed to request password reset'
  } finally {
    loading.value = false
  }
}

const resetPassword = async () => {
  if (!token.value || !newPassword.value || !passwordsMatch.value) return
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const result = await api.resetPassword({
      token: token.value,
      new_password: newPassword.value
    })
    
    if (result.error) {
      error.value = result.error
      return
    }
    
    success.value = 'Password reset successfully! Redirecting to login...'
    
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err: any) {
    error.value = err.message || 'Failed to reset password'
  } finally {
    loading.value = false
  }
}

const startOver = () => {
  tokenReceived.value = false
  token.value = ''
  resetToken.value = ''
  newPassword.value = ''
  confirmPassword.value = ''
  error.value = ''
  success.value = ''
}
</script>
