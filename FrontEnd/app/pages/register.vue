<template>
  <div class="flex min-h-screen">
    <!-- Left side - Branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-primary items-center justify-center p-12">
      <div class="max-w-md text-white">
        <h1 class="text-4xl font-bold mb-4">Join FarmTrack</h1>
        <p class="text-lg opacity-90">
          Create an account to start tracking your livestock with complete traceability from farm to consumer.
        </p>
      </div>
    </div>

    <!-- Right side - Registration Form -->
    <div class="flex-1 flex items-center justify-center p-8">
      <div class="w-full max-w-md space-y-8">
        <div class="text-center">
          <h2 class="text-3xl font-bold">Create Account</h2>
          <p class="text-muted-foreground mt-2">Sign up to get started</p>
        </div>

        <UiCard>
          <UiCardContent class="pt-6">
            <form @submit.prevent="handleRegister" class="space-y-4">
              <div class="space-y-2">
                <UiLabel for="username">Username *</UiLabel>
                <UiInput 
                  id="username" 
                  v-model="username" 
                  placeholder="Enter username"
                  required
                  :disabled="loading"
                />
              </div>

              <div class="space-y-2">
                <UiLabel for="email">Email</UiLabel>
                <UiInput 
                  id="email" 
                  v-model="email" 
                  type="email"
                  placeholder="Enter email (optional)"
                  :disabled="loading"
                />
              </div>

              <div class="space-y-2">
                <UiLabel for="full_name">Full Name</UiLabel>
                <UiInput 
                  id="full_name" 
                  v-model="fullName" 
                  placeholder="Enter full name (optional)"
                  :disabled="loading"
                />
              </div>

              <div class="space-y-2">
                <UiLabel for="role">Account Type *</UiLabel>
                <UiSelect v-model="role" required>
                  <UiSelectTrigger id="role">
                    <UiSelectValue placeholder="Select account type" />
                  </UiSelectTrigger>
                  <UiSelectContent>
                    <UiSelectItem value="farmer">Farmer</UiSelectItem>
                    <UiSelectItem value="processor">Processor</UiSelectItem>
                    <UiSelectItem value="regulator">Regulator</UiSelectItem>
                  </UiSelectContent>
                </UiSelect>
              </div>

              <div class="space-y-2">
                <UiLabel for="password">Password *</UiLabel>
                <UiInput 
                  id="password" 
                  v-model="password" 
                  type="password"
                  placeholder="Enter password (min 6 characters)"
                  required
                  :disabled="loading"
                />
              </div>

              <div class="space-y-2">
                <UiLabel for="confirm_password">Confirm Password *</UiLabel>
                <UiInput 
                  id="confirm_password" 
                  v-model="confirmPassword" 
                  type="password"
                  placeholder="Confirm password"
                  required
                  :disabled="loading"
                />
              </div>

              <UiAlert v-if="error" variant="destructive">
                <UiAlertDescription>{{ error }}</UiAlertDescription>
              </UiAlert>

              <UiButton type="submit" class="w-full" :disabled="loading">
                <UiSpinner v-if="loading" class="mr-2 h-4 w-4" />
                {{ loading ? 'Creating Account...' : 'Create Account' }}
              </UiButton>
            </form>

            <div class="mt-6 text-center text-sm">
              <span class="text-muted-foreground">Already have an account?</span>
              <NuxtLink to="/login" class="text-primary hover:underline ml-1">
                Sign in
              </NuxtLink>
            </div>
          </UiCardContent>
        </UiCard>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const router = useRouter()
const api = useApi()

const username = ref('')
const email = ref('')
const fullName = ref('')
const role = ref('farmer')
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')

const handleRegister = async () => {
  error.value = ''
  
  // Validation
  if (!username.value || !password.value || !role.value) {
    error.value = 'Please fill in all required fields'
    return
  }
  
  if (username.value.length < 3) {
    error.value = 'Username must be at least 3 characters'
    return
  }
  
  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }
  
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  
  loading.value = true
  
  try {
    const payload = {
      username: username.value.trim(),
      password: password.value,
      role: role.value,
      email: email.value.trim() || null,
      full_name: fullName.value.trim() || null
    }
    
    const result = await api.register(payload)
    
    if (result.error) {
      error.value = result.error
    } else if (result.data && result.data.access_token) {
      // Store token and redirect to dashboard
      localStorage.setItem('auth_token', result.data.access_token)
      localStorage.setItem('username', username.value)
      
      await router.push('/dashboard')
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  } catch (err: any) {
    error.value = err.message || 'An error occurred during registration'
  } finally {
    loading.value = false
  }
}
</script>