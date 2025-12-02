import { ref } from 'vue'
import { toast } from 'vue-sonner'

export const useSettings = () => {
  const api = useApi()
  const auth = useAuthManagement()
  
  const loading = ref(false)
  const profile = ref<any>(null)
  const account = ref<any>(null)
  const notifications = ref<any>(null)

  const getUsername = () => {
    return auth.getUsername()
  }

  const loadProfile = async () => {
    const username = getUsername()
    if (!username) return

    loading.value = true
    try {
      const { data, error } = await api.getProfile(username)
      if (error) {
        toast.error('Failed to load profile', { description: error })
        return
      }
      profile.value = data
    } catch (err: any) {
      toast.error('Failed to load profile', { description: err.message })
    } finally {
      loading.value = false
    }
  }

  const updateProfile = async (profileData: any) => {
    const username = getUsername()
    if (!username) return

    loading.value = true
    try {
      const { data, error } = await api.updateProfile(username, profileData)
      if (error) {
        toast.error('Failed to update profile', { description: error })
        return false
      }
      
      profile.value = data.profile
      
      // Update username in localStorage if it was changed
      if (profileData.username && profileData.username !== username) {
        localStorage.setItem('username', profileData.username)
      }
      
      toast.success('Profile updated successfully!')
      return true
    } catch (err: any) {
      toast.error('Failed to update profile', { description: err.message })
      return false
    } finally {
      loading.value = false
    }
  }

  const loadAccount = async () => {
    const username = getUsername()
    if (!username) return

    loading.value = true
    try {
      const { data, error } = await api.getAccount(username)
      if (error) {
        toast.error('Failed to load account settings', { description: error })
        return
      }
      account.value = data
    } catch (err: any) {
      toast.error('Failed to load account settings', { description: err.message })
    } finally {
      loading.value = false
    }
  }

  const updateAccount = async (accountData: any) => {
    const username = getUsername()
    if (!username) return

    loading.value = true
    try {
      const { data, error } = await api.updateAccount(username, accountData)
      if (error) {
        toast.error('Failed to update account settings', { description: error })
        return false
      }
      
      account.value = data.account
      toast.success('Account settings updated successfully!')
      return true
    } catch (err: any) {
      toast.error('Failed to update account settings', { description: err.message })
      return false
    } finally {
      loading.value = false
    }
  }

  const loadNotifications = async () => {
    const username = getUsername()
    if (!username) return

    loading.value = true
    try {
      const { data, error } = await api.getNotifications(username)
      if (error) {
        toast.error('Failed to load notification settings', { description: error })
        return
      }
      notifications.value = data
    } catch (err: any) {
      toast.error('Failed to load notification settings', { description: err.message })
    } finally {
      loading.value = false
    }
  }

  const updateNotifications = async (notificationData: any) => {
    const username = getUsername()
    if (!username) return

    loading.value = true
    try {
      const { data, error } = await api.updateNotifications(username, notificationData)
      if (error) {
        toast.error('Failed to update notification settings', { description: error })
        return false
      }
      
      notifications.value = data.notifications
      toast.success('Notification settings updated successfully!')
      return true
    } catch (err: any) {
      toast.error('Failed to update notification settings', { description: err.message })
      return false
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (currentPassword: string, newPassword: string) => {
    const username = getUsername()
    if (!username) return

    loading.value = true
    try {
      const { data, error } = await api.changePassword(username, {
        current_password: currentPassword,
        new_password: newPassword
      })
      if (error) {
        toast.error('Failed to change password', { description: error })
        return false
      }
      
      toast.success('Password changed successfully!')
      return true
    } catch (err: any) {
      toast.error('Failed to change password', { description: err.message })
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    profile,
    account,
    notifications,
    loadProfile,
    updateProfile,
    loadAccount,
    updateAccount,
    loadNotifications,
    updateNotifications,
    changePassword,
  }
}
