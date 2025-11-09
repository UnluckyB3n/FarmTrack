export const useAuthManagement = () => {
  const router = useRouter()
  
  const isAuthenticated = () => {
    if (process.server) return false
    return !!localStorage.getItem('auth_token')
  }

  const getUsername = () => {
    if (process.server) return null
    return localStorage.getItem('username')
  }

  const signOut = async () => {
    try {
      // Check if using SSO (nuxt-auth)
      const { signOut: ssoSignOut, status } = useAuth()
      
      // Clear local storage (for credential-based auth)
      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('username')
      }
      
      // If using SSO, sign out from SSO provider
      if (status.value === 'authenticated') {
        await ssoSignOut({ callbackUrl: '/login' })
      } else {
        // For credential-based auth, just redirect to login
        await router.push('/login')
      }
      
      console.log('User signed out successfully')
    } catch (error) {
      console.error('Sign out error:', error)
      // Fallback: clear storage and redirect anyway
      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('username')
      }
      await router.push('/login')
    }
  }

  return {
    isAuthenticated,
    getUsername,
    signOut,
  }
}
