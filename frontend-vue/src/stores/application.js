import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'

export const useApplicationStore = defineStore('application', () => {
  const applications = ref([])
  const currentApplication = ref(null)
  const loading = ref(false)
  const error = ref(null)

  // Save draft application
  const saveDraft = async (applicationData) => {
    try {
      loading.value = true
      error.value = null
      
      // Clean up the data - convert empty strings to null for better backend handling
      const cleanedData = {}
      Object.keys(applicationData).forEach(key => {
        const value = applicationData[key]
        // Only include non-empty values, but allow 0 as a valid value
        if (value !== '' && value !== null && value !== undefined) {
          cleanedData[key] = value
        }
      })
      
      // If no data to send, send an empty object to create a blank draft
      const dataToSend = Object.keys(cleanedData).length > 0 ? cleanedData : {}
      
      const response = await axios.post(`${API_BASE_URL}/api/application/save-draft`, dataToSend)
      
      return { success: true, message: response.data.message, applicationId: response.data.application_id }
    } catch (err) {
      console.error('Save draft error:', err.response?.data || err.message)
      error.value = err.response?.data?.error || 'Failed to save draft'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Get draft application
  const getDraft = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.get(`${API_BASE_URL}/api/application/get-draft`)
      
      if (response.data.draft) {
        currentApplication.value = response.data.draft
        return { success: true, draft: response.data.draft }
      } else {
        return { success: false, message: 'No draft found' }
      }
    } catch (err) {
      if (err.response?.status === 404) {
        return { success: false, message: 'No draft found' }
      }
      error.value = err.response?.data?.error || 'Failed to get draft'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Submit application
  const submitApplication = async (applicationData) => {
    try {
      loading.value = true
      error.value = null
      
      // Create FormData for file uploads
      const formData = new FormData()
      
      // Add all form fields
      Object.keys(applicationData).forEach(key => {
        if (applicationData[key] !== null && applicationData[key] !== undefined) {
          formData.append(key, applicationData[key])
        }
      })
      
      const response = await axios.post(`${API_BASE_URL}/api/application/submit`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      return { success: true, message: response.data.message, applicationId: response.data.application_id }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to submit application'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Get user applications
  const getUserApplications = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.get(`${API_BASE_URL}/api/application/status`)
      
      // Convert single application to array for consistency
      const application = response.data.application
      applications.value = application ? [application] : []
      return { success: true, applications: applications.value }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to get applications'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Get all applications (admin only)
  const getAllApplications = async () => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.get(`${API_BASE_URL}/api/application/admin/list-all`)
      
      applications.value = response.data.applications
      return { success: true, applications: response.data.applications }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to get all applications'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Update application status (admin only)
  const updateApplicationStatus = async (applicationId, status, comments = '') => {
    try {
      loading.value = true
      error.value = null
      
      // Convert status to action format expected by backend
      const action = status === 'approved' ? 'approve' : 'reject'
      
      const response = await axios.post(`${API_BASE_URL}/api/application/admin/review/${applicationId}`, {
        action,
        comments
      })
      
      // Update local applications array
      const index = applications.value.findIndex(app => app.id === applicationId)
      if (index !== -1) {
        applications.value[index] = { ...applications.value[index], ...response.data.application }
      }
      
      return { success: true, message: response.data.message }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to update application status'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Get application details
  const getApplicationDetails = async (applicationId) => {
    try {
      loading.value = true
      error.value = null
      
      const response = await axios.get(`${API_BASE_URL}/api/application/admin/${applicationId}`)
      
      return { success: true, application: response.data.application }
    } catch (err) {
      error.value = err.response?.data?.error || 'Failed to get application details'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  return {
    applications,
    currentApplication,
    loading,
    error,
    saveDraft,
    getDraft,
    submitApplication,
    getUserApplications,
    getAllApplications,
    updateApplicationStatus,
    getApplicationDetails
  }
})
