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
      // Check how user logged in
      const authMethod = process.client ? localStorage.getItem('auth_method') : null
      
      console.log('Signing out, auth method:', authMethod)
      
      // If user logged in with Google SSO, try to sign out from Google first
      if (authMethod === 'google') {
        try {
          const { signOut: ssoSignOut, status } = useAuth()
          console.log('SSO status:', status.value)
          
          if (status.value === 'authenticated') {
            // Clear local storage before SSO redirect
            if (process.client) {
              localStorage.removeItem('auth_token')
              localStorage.removeItem('username')
              localStorage.removeItem('auth_method')
            }
            
            await ssoSignOut({ callbackUrl: '/login', redirect: true })
            return // Let SSO handle the redirect
          }
        } catch (ssoError) {
          console.log('SSO sign out failed, continuing with regular sign out:', ssoError)
        }
      }
      
      // Clear local storage for credential-based auth
      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('username')
        localStorage.removeItem('auth_method')
      }
      
      console.log('User signed out successfully, redirecting to login')
      
      // Redirect to login page
      await router.push('/login')
    } catch (error) {
      console.error('Sign out error:', error)
      // Fallback: clear storage and redirect anyway
      if (process.client) {
        localStorage.removeItem('auth_token')
        localStorage.removeItem('username')
        localStorage.removeItem('auth_method')
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
