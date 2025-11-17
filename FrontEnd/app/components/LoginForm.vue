<template>
  <div :class="cn('flex flex-col gap-6', props.class)">
    <Card>
      <CardHeader class="text-center">
        <CardTitle class="text-xl">
          Welcome back to FarmTrack!
        </CardTitle>
        <CardDescription>
          Login with your Google account or use credentials
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div class="grid gap-6">
            <!-- Google SSO Button -->
            <div class="flex flex-col gap-4">
              <Button variant="outline" class="w-full" @click="loginWithGoogle" type="button">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="mr-2 h-4 w-4">
                  <path
                    d="M12.48 10.92v3.28h7.84c-.24 1.84-.853 3.187-1.787 4.133-1.147 1.147-2.933 2.4-6.053 2.4-4.827 0-8.6-3.893-8.6-8.72s3.773-8.72 8.6-8.72c2.6 0 4.507 1.027 5.907 2.347l2.307-2.307C18.747 1.44 16.133 0 12.48 0 5.867 0 .307 5.387.307 12s5.56 12 12.173 12c3.573 0 6.267-1.173 8.373-3.36 2.16-2.16 2.84-5.213 2.84-7.667 0-.76-.053-1.467-.173-2.053H12.48z"
                    fill="currentColor"
                  />
                </svg>
                Login with Google
              </Button>
            </div>

            <div class="after:border-border relative text-center text-sm after:absolute after:inset-0 after:top-1/2 after:z-0 after:flex after:items-center after:border-t">
              <span class="bg-card text-muted-foreground relative z-10 px-2">
                Or continue with credentials
              </span>
            </div>

            <!-- Username/Password Form -->
            <div class="grid gap-3">
              <Label for="username">Username</Label>
              <Input
                id="username"
                v-model="username"
                type="text"
                placeholder="farm_admin"
                required
                :disabled="loading"
              />
            </div>
            <div class="grid gap-3">
              <div class="flex items-center justify-between">
                <Label for="password">Password</Label>
                <NuxtLink to="/forgot-password" class="text-xs text-primary hover:underline">
                  Forgot password?
                </NuxtLink>
              </div>
              <Input
                id="password"
                v-model="password"
                type="password"
                placeholder="••••••••"
                required
                :disabled="loading"
              />
            </div>

            <div v-if="error" class="rounded-lg bg-destructive/10 border border-destructive px-3 py-2 text-sm text-destructive">
              {{ error }}
            </div>

            <Button type="submit" class="w-full" :disabled="loading" @click.prevent="handleLogin">
              {{ loading ? 'Signing in...' : 'Sign In' }}
            </Button>
          </div>
        </form>

        <div class="mt-4 rounded-lg border bg-muted p-3 text-sm">
          <p class="font-medium mb-2">Test Accounts:</p>
          <ul class="space-y-1 text-xs text-muted-foreground">
            <li><strong>Admin:</strong> farm_admin / admin123</li>
            <li><strong>Farmer:</strong> j_farmer / farmer123</li>
            <li><strong>Processor:</strong> m_processor / process123</li>
          </ul>
        </div>

        <div class="mt-4 text-center text-sm">
          Don't have an account?
          <NuxtLink to="/register" class="text-primary hover:underline font-medium">
            Sign up
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
import { useAuth } from '#imports'

const props = defineProps<{
  class?: HTMLAttributes["class"]
}>()

const router = useRouter()
const api = useApi()
const { signIn } = useAuth()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const loginWithGoogle = async () => {
  await signIn('google', { callbackUrl: '/dashboard' })
}

const handleLogin = async () => {
  // Validate inputs
  if (!username.value || !password.value) {
    error.value = 'Please enter both username and password'
    return
  }

  loading.value = true
  error.value = ''

  try {
    // Trim whitespace from inputs
    const trimmedUsername = username.value.trim()
    const trimmedPassword = password.value.trim()
    
    const result = await api.login(trimmedUsername, trimmedPassword)
    
    if (result.error) {
      error.value = result.error
      console.error('Login failed:', result.error)
    } else if (result.data && result.data.access_token) {
      // Store token in localStorage
      localStorage.setItem('auth_token', result.data.access_token)
      localStorage.setItem('username', trimmedUsername)
      
      // Redirect to dashboard
      await router.push('/dashboard')
    } else {
      error.value = 'Invalid response from server'
      console.error('Unexpected response:', result)
    }
  } catch (err: any) {
    console.error('Login exception:', err)
    error.value = err.message || 'An unexpected error occurred'
  } finally {
    loading.value = false
  }
}
</script>