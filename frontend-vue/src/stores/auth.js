import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'
import router from '../router'

const API_BASE_URL = 'http://localhost:5000'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token'))
  const loading = ref(false)
  const error = ref(null)

  // Configure axios defaults
  if (token.value) {
    axios.defaults.headers.common['Authentication-Token'] = token.value
  }

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  
  const isAdmin = computed(() => user.value?.roles?.includes('admin'))
  
  const isStudent = computed(() => user.value?.roles?.includes('student'))

  // Login function
  const login = async (credentials) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, credentials)
      
      if (response.data.token) {
        token.value = response.data.token
        user.value = response.data.user
        
        // Store token in localStorage
        localStorage.setItem('auth_token', response.data.token)
        
        // Set axios default header
        axios.defaults.headers.common['Authentication-Token'] = response.data.token
        
        // Redirect to dashboard
        router.push('/dashboard')
        
        return { success: true, message: response.data.message }
      }
    } catch (err) {
      error.value = err.response?.data?.error || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Register function
  const register = async (userData) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.post(`${API_BASE_URL}/api/auth/register`, userData)
      
      return { success: true, message: response.data.message }
    } catch (err) {
      error.value = err.response?.data?.error || 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Logout function
  const logout = async () => {
    try {
      if (token.value) {
        await axios.post(`${API_BASE_URL}/api/auth/logout`)
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local state regardless of API call success
      user.value = null
      token.value = null
      localStorage.removeItem('auth_token')
      delete axios.defaults.headers.common['Authentication-Token']
      router.push('/login')
    }
  }

  // Get profile function
  const getProfile = async () => {
    try {
      if (!token.value) return
      
      const response = await axios.get(`${API_BASE_URL}/api/auth/profile`)
      user.value = response.data.user
      return { success: true, user: response.data.user }
    } catch (err) {
      // If profile fetch fails, user might be logged out
      if (err.response?.status === 401) {
        logout()
      }
      return { success: false, error: err.response?.data?.error }
    }
  }

  // Update profile function
  const updateProfile = async (profileData) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.put(`${API_BASE_URL}/api/auth/profile/edit`, profileData)
      
      // Update local user data
      user.value = { ...user.value, ...response.data.user }
      
      return { success: true, message: response.data.message }
    } catch (err) {
      error.value = err.response?.data?.error || 'Profile update failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Initialize store (check if user is already logged in)
  const init = async () => {
    if (token.value) {
      await getProfile()
    }
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    isAdmin,
    isStudent,
    login,
    register,
    logout,
    getProfile,
    updateProfile,
    init
  }
})
