export default defineNuxtRouteMiddleware((to, from) => {
  // Skip middleware on server side
  if (process.server) return

  // Public routes that don't require authentication
  const publicRoutes = ['/login', '/register', '/forgot-password']
  const isPublicRoute = publicRoutes.includes(to.path)
  const isPublicQRRoute = to.path.startsWith('/public/')

  // Check if user is authenticated
  const token = localStorage.getItem('auth_token')

  // If not authenticated and trying to access protected route, redirect to login
  if (!token && !isPublicRoute && !isPublicQRRoute) {
    return navigateTo('/login')
  }

  // If authenticated and trying to access login/register, redirect to dashboard
  if (token && (to.path === '/login' || to.path === '/register')) {
    return navigateTo('/dashboard')
  }
})
