<template>
  <div :class="cn('flex flex-col gap-6', props.class)">
    <Card>
      <CardHeader class="text-center">
        <CardTitle class="text-xl">
          Create your FarmTrack account
        </CardTitle>
        <CardDescription>
          Join our farm-to-table traceability platform
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div class="grid gap-6">
            <!-- Google SSO Button -->
            <div class="flex flex-col gap-4">
              <Button variant="outline" class="w-full" @click="registerWithGoogle" type="button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="mr-2 h-4 w-4">
                  <path
                    d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
                    fill="currentColor"
                  />
                </svg>
                Sign up with Google
              </Button>
            </div>

            <div class="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t">
              <span class="bg-card text-muted-foreground relative z-10 px-2">
                Or continue with credentials
              </span>
            </div>

            <!-- Registration Form -->
            <div class="grid gap-3">
              <Label for="username">Username *</Label>
              <Input
                id="username"
                v-model="username"
                type="text"
                placeholder="farm_user"
                required
                :disabled="loading"
              />
              <p class="text-xs text-muted-foreground">
                Minimum 3 characters, alphanumeric with underscores
              </p>
            </div>

            <div class="grid gap-3">
              <Label for="email">Email (optional)</Label>
              <Input
                id="email"
                v-model="email"
                type="email"
                placeholder="user@example.com"
                :disabled="loading"
              />
            </div>

            <div class="grid gap-3">
              <Label for="full_name">Full Name (optional)</Label>
              <Input
                id="full_name"
                v-model="fullName"
                type="text"
                placeholder="John Doe"
                :disabled="loading"
              />
            </div>

            <div class="grid gap-3">
              <Label for="role">Role *</Label>
              <Select v-model="role" :disabled="loading">
                <SelectTrigger id="role">
                  <SelectValue placeholder="Select your role" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="farmer">
                    <div class="flex flex-col items-start">
                      <span class="font-medium">Farmer</span>
                      <span class="text-xs text-muted-foreground">Manage animals, facilities, and events</span>
                    </div>
                  </SelectItem>
                  <SelectItem value="processor">
                    <div class="flex flex-col items-start">
                      <span class="font-medium">Processor</span>
                      <span class="text-xs text-muted-foreground">Process and package products</span>
                    </div>
                  </SelectItem>
                  <SelectItem value="regulator">
                    <div class="flex flex-col items-start">
                      <span class="font-medium">Regulator</span>
                      <span class="text-xs text-muted-foreground">Audit and compliance oversight</span>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div class="grid gap-3">
              <Label for="password">Password *</Label>
              <Input
                id="password"
                v-model="password"
                type="password"
                placeholder="••••••••"
                required
                :disabled="loading"
              />
              <p class="text-xs text-muted-foreground">
                Minimum 6 characters
              </p>
            </div>

            <div class="grid gap-3">
              <Label for="confirm_password">Confirm Password *</Label>
              <Input
                id="confirm_password"
                v-model="confirmPassword"
                type="password"
                placeholder="••••••••"
                required
                :disabled="loading"
              />
            </div>

            <div v-if="error" class="rounded-lg bg-destructive/10 border border-destructive px-3 py-2 text-sm text-destructive">
              {{ error }}
            </div>

            <div v-if="success" class="rounded-lg bg-green-50 border border-green-200 px-3 py-2 text-sm text-green-700">
              {{ success }}
            </div>

            <Button type="submit" class="w-full" :disabled="loading" @click.prevent="handleRegister">
              {{ loading ? 'Creating account...' : 'Create Account' }}
            </Button>
          </div>
        </form>

        <div class="mt-4 text-center text-sm">
          Already have an account?
          <NuxtLink to="/login" class="text-primary hover:underline font-medium">
            Sign in
          </NuxtLink>
        </div>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import type { HTMLAttributes } from "vue"
import { cn } from "@/lib/utils"
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useAuth } from '#imports'

const props = defineProps<{
  class?: HTMLAttributes["class"]
}>()

const router = useRouter()
const api = useApi()
const { signIn } = useAuth()

const username = ref('')
const email = ref('')
const fullName = ref('')
const role = ref('farmer')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

const registerWithGoogle = async () => {
  await signIn('google', { callbackUrl: '/dashboard' })
}

const handleRegister = async () => {
  // Clear previous messages
  error.value = ''
  success.value = ''

  // Validate inputs
  if (!username.value || !password.value || !confirmPassword.value || !role.value) {
    error.value = 'Please fill in all required fields'
    return
  }

  // Validate username length
  if (username.value.trim().length < 3) {
    error.value = 'Username must be at least 3 characters'
    return
  }

  // Validate password length
  if (password.value.length < 6) {
    error.value = 'Password must be at least 6 characters'
    return
  }

  // Validate password match
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }

  // Validate email format if provided
  if (email.value && !isValidEmail(email.value)) {
    error.value = 'Please enter a valid email address'
    return
  }

  loading.value = true

  try {
    // Prepare registration data
    const registrationData = {
      username: username.value.trim(),
      password: password.value,
      role: role.value,
      email: email.value.trim() || null,
      full_name: fullName.value.trim() || null,
    }

    const result = await api.register(registrationData)
    
    if (result.error) {
      error.value = result.error
      console.error('Registration failed:', result.error)
    } else if (result.data && result.data.access_token) {
      // Registration successful - store token and redirect
      localStorage.setItem('auth_token', result.data.access_token)
      localStorage.setItem('username', result.data.user.username)
      
      success.value = 'Account created successfully! Redirecting...'
      
      // Redirect to dashboard after short delay
      setTimeout(async () => {
        await router.push('/dashboard')
      }, 1500)
    } else {
      error.value = 'Invalid response from server'
      console.error('Unexpected response:', result)
    }
  } catch (err: any) {
    console.error('Registration exception:', err)
    error.value = err.message || 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}

const isValidEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}
</script>
