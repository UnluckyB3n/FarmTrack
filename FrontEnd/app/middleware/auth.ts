export default defineNuxtRouteMiddleware((to, from) => {
  // Skip middleware on server side
  if (process.server) return

  // Check if user is authenticated
  const token = localStorage.getItem('auth_token')

  // If not authenticated and trying to access protected route, redirect to login
  if (!token && to.path !== '/login') {
    return navigateTo('/login')
  }

  // If authenticated and trying to access login, redirect to dashboard
  if (token && to.path === '/login') {
    return navigateTo('/dashboard')
  }
})
