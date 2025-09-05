<template>
  <div class="dashboard-page">
    <div class="container-fluid py-4">
      <!-- Welcome Section -->
      <div class="row mb-4">
        <div class="col">
          <div class="card border-0 shadow bg-primary text-white">
            <div class="card-body p-4">
              <div class="row align-items-center">
                <div class="col">
                  <h2 class="mb-1 text-white">
                    Welcome back, {{ authStore.user?.name }}!
                  </h2>
                  <p class="mb-0">
                    {{ authStore.user?.roles?.join(', ') | capitalize }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Dashboard Cards -->
      <div class="row g-4 mb-4">
        <!-- Student Dashboard -->
        <template v-if="authStore.isStudent">
          <!-- Draft Application Card (shows if user has a draft) -->
          <div v-if="applicationStatus === 'Draft'" class="col-12 mb-3">
            <div class="card border-warning shadow-sm">
              <div class="card-body p-4">
                <div class="row align-items-center">
                  <div class="col-auto">
                    <i class="bi bi-file-earmark-text text-warning" style="font-size: 2.5rem;"></i>
                  </div>
                  <div class="col">
                    <h5 class="card-title mb-1">
                      <i class="bi bi-exclamation-triangle text-warning me-2"></i>
                      Continue Your Draft Application
                    </h5>
                    <p class="card-text text-muted mb-2">
                      You have a saved draft application. Continue where you left off to complete your submission.
                    </p>
                    <small class="text-muted">
                      Last saved: {{ applications[0]?.date_created ? new Date(applications[0].date_created).toLocaleDateString() : 'Unknown' }}
                    </small>
                  </div>
                  <div class="col-auto">
                    <router-link to="/application" class="btn btn-warning me-2">
                      <i class="bi bi-pencil me-1"></i>
                      Continue Draft
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i class="bi bi-file-earmark-text text-primary" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">My Applications</h5>
                <p class="card-text text-muted">
                  View and manage your admission applications
                </p>
                <router-link to="/my-applications" class="btn btn-primary">
                  <i class="bi bi-arrow-right me-1"></i>
                  View Applications
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i class="bi bi-plus-circle text-success" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">New Application</h5>
                <p class="card-text text-muted">
                  Start a new admission application
                </p>
                <router-link to="/application" class="btn btn-success">
                  <i class="bi bi-plus me-1"></i>
                  Apply Now
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i class="bi bi-person text-info" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">Profile</h5>
                <p class="card-text text-muted">
                  Update your personal information
                </p>
                <router-link to="/profile" class="btn btn-info">
                  <i class="bi bi-pencil me-1"></i>
                  Edit Profile
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i :class="getStatusIcon(detailedStatusInfo.status)" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">{{ detailedStatusInfo.status }}</h5>
                <p class="card-text text-muted small">
                  {{ detailedStatusInfo.message }}
                </p>
                <div class="mb-2">
                  <span :class="statusBadgeClass" class="badge fs-6">
                    {{ detailedStatusInfo.status }}
                  </span>
                </div>
                <div class="text-muted small">
                  <div v-if="detailedStatusInfo.course">
                    <i class="bi bi-book me-1"></i>
                    {{ detailedStatusInfo.course }}
                  </div>
                  <div v-if="detailedStatusInfo.date">
                    <i class="bi bi-calendar me-1"></i>
                    {{ detailedStatusInfo.date }}
                  </div>
                  <div v-if="detailedStatusInfo.applicationId">
                    <i class="bi bi-hash me-1"></i>
                    App ID: {{ detailedStatusInfo.applicationId }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- Admin Dashboard -->
        <template v-if="authStore.isAdmin">
          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i class="bi bi-files text-primary" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">All Applications</h5>
                <h3 class="text-primary mb-2">{{ totalApplications }}</h3>
                <p class="card-text text-muted">Total applications received</p>
                <router-link to="/admin" class="btn btn-primary">
                  <i class="bi bi-eye me-1"></i>
                  Review Applications
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i class="bi bi-hourglass-split text-warning" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">Pending Review</h5>
                <h3 class="text-warning mb-2">{{ pendingApplications }}</h3>
                <p class="card-text text-muted">Applications awaiting review</p>
                <router-link to="/admin?filter=pending" class="btn btn-warning">
                  <i class="bi bi-clock me-1"></i>
                  Review Pending
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i class="bi bi-check-circle text-success" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">Approved</h5>
                <h3 class="text-success mb-2">{{ approvedApplications }}</h3>
                <p class="card-text text-muted">Applications approved</p>
                <router-link to="/admin?filter=approved" class="btn btn-success">
                  <i class="bi bi-check me-1"></i>
                  View Approved
                </router-link>
              </div>
            </div>
          </div>

          <div class="col-md-6 col-lg-3">
            <div class="card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="mb-3">
                  <i class="bi bi-x-circle text-danger" style="font-size: 3rem;"></i>
                </div>
                <h5 class="card-title">Rejected</h5>
                <h3 class="text-danger mb-2">{{ rejectedApplications }}</h3>
                <p class="card-text text-muted">Applications rejected</p>
                <router-link to="/admin?filter=rejected" class="btn btn-danger">
                  <i class="bi bi-x me-1"></i>
                  View Rejected
                </router-link>
              </div>
            </div>
          </div>
        </template>
      </div>

      <!-- Recent Activity -->
      <div class="row">
        <div class="col">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-light">
              <h5 class="mb-0">
                <i class="bi bi-clock-history me-2"></i>
                Recent Activity
              </h5>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2 text-muted">Loading recent activity...</p>
              </div>
              
              <div v-else-if="recentActivities.length === 0" class="text-center py-4 text-muted">
                <i class="bi bi-inbox" style="font-size: 3rem;"></i>
                <p class="mt-2">No recent activity found</p>
              </div>
              
              <div v-else>
                <div 
                  v-for="activity in recentActivities" 
                  :key="activity.id"
                  class="d-flex align-items-center py-3 border-bottom"
                >
                  <div class="me-3">
                    <div :class="getActivityIconClass(activity.type)" class="rounded-circle p-2">
                      <i :class="getActivityIcon(activity.type)"></i>
                    </div>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="mb-1">{{ activity.title }}</h6>
                    <p class="mb-1 text-muted small">{{ activity.description }}</p>
                    <small class="text-muted">{{ formatDate(activity.date) }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useApplicationStore } from '../stores/application'

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore()
    const applicationStore = useApplicationStore()
    
    const loading = ref(false)
    const applications = ref([])
    const recentActivities = ref([])
    
    // Computed properties for application stats
    const totalApplications = computed(() => applications.value.length)
    const pendingApplications = computed(() => 
      applications.value.filter(app => app.status === 'pending').length
    )
    const approvedApplications = computed(() => 
      applications.value.filter(app => app.status === 'approved').length
    )
    const rejectedApplications = computed(() => 
      applications.value.filter(app => app.status === 'rejected').length
    )
    
    const applicationStatus = computed(() => {
      if (applications.value.length === 0) return 'No Application'
      
      // Sort applications by date to get the latest one
      const sortedApps = [...applications.value].sort((a, b) => 
        new Date(b.date_created) - new Date(a.date_created)
      )
      const latest = sortedApps[0]
      
      // Enhanced status with more details
      const status = latest.status.charAt(0).toUpperCase() + latest.status.slice(1)
      
      // Add course information for better context
      if (latest.course_applied) {
        return `${status} - ${latest.course_applied}`
      }
      
      return status
    })
    
    const detailedStatusInfo = computed(() => {
      if (applications.value.length === 0) {
        return {
          status: 'No Application',
          message: 'Start your admission journey by submitting an application',
          date: null,
          course: null,
          reviewedBy: null
        }
      }
      
      // Get the latest application
      const sortedApps = [...applications.value].sort((a, b) => 
        new Date(b.date_created) - new Date(a.date_created)
      )
      const latest = sortedApps[0]
      
      let message = ''
      let date = latest.date_created
      
      switch (latest.status.toLowerCase()) {
        case 'draft':
          message = 'Your application is saved as draft. Continue to complete and submit it.'
          break
        case 'pending':
          message = 'Your application is under review by the admissions committee.'
          break
        case 'approved':
          message = 'Congratulations! Your application has been approved.'
          date = latest.reviewed_at || latest.date_created
          break
        case 'rejected':
          message = 'Your application was not approved. You may apply for other programs.'
          date = latest.reviewed_at || latest.date_created
          break
        default:
          message = 'Application status unknown.'
      }
      
      return {
        status: latest.status.charAt(0).toUpperCase() + latest.status.slice(1),
        message,
        date: date ? new Date(date).toLocaleDateString() : null,
        course: latest.course_applied || 'Not specified',
        reviewedBy: latest.review_comments || null,
        applicationId: latest.id
      }
    })
    
    const statusBadgeClass = computed(() => {
      const status = applicationStatus.value.toLowerCase()
      return {
        'bg-warning': status === 'pending' || status === 'draft',
        'bg-success': status === 'approved',
        'bg-danger': status === 'rejected',
        'bg-secondary': status === 'no application'
      }
    })
    
    const loadDashboardData = async () => {
      loading.value = true
      
      try {
        if (authStore.isAdmin) {
          const result = await applicationStore.getAllApplications()
          if (result.success) {
            applications.value = result.applications
            generateRecentActivities(result.applications)
          }
        } else if (authStore.isStudent) {
          const result = await applicationStore.getUserApplications()
          if (result.success) {
            applications.value = result.applications
            generateStudentActivities(result.applications)
          }
        }
      } catch (error) {
        console.error('Error loading dashboard data:', error)
      } finally {
        loading.value = false
      }
    }
    
    const generateRecentActivities = (apps) => {
      const activities = []
      
      // Get recent applications
      const recentApps = apps
        .sort((a, b) => new Date(b.date_created) - new Date(a.date_created))
        .slice(0, 5)
      
      recentApps.forEach(app => {
        activities.push({
          id: app.id,
          type: 'application',
          title: `New Application Received`,
          description: `Application for ${app.course_applied} by ${app.student?.name}`,
          date: app.date_created
        })
        
        if (app.reviewed_at) {
          activities.push({
            id: `review-${app.id}`,
            type: app.status,
            title: `Application ${app.status}`,
            description: `Application for ${app.course_applied} has been ${app.status}`,
            date: app.reviewed_at
          })
        }
      })
      
      recentActivities.value = activities
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, 8)
    }
    
    const generateStudentActivities = (apps) => {
      const activities = []
      
      apps.forEach(app => {
        activities.push({
          id: app.id,
          type: 'application',
          title: `Application Submitted`,
          description: `Your application for ${app.course_applied} has been submitted`,
          date: app.date_created
        })
        
        if (app.reviewed_at) {
          activities.push({
            id: `review-${app.id}`,
            type: app.status,
            title: `Application ${app.status}`,
            description: `Your application for ${app.course_applied} has been ${app.status}`,
            date: app.reviewed_at
          })
        }
      })
      
      recentActivities.value = activities
        .sort((a, b) => new Date(b.date) - new Date(a.date))
        .slice(0, 8)
    }
    
    const getActivityIcon = (type) => {
      switch (type) {
        case 'application': return 'bi bi-file-earmark-plus'
        case 'approved': return 'bi bi-check-circle'
        case 'rejected': return 'bi bi-x-circle'
        case 'pending': return 'bi bi-clock'
        default: return 'bi bi-circle'
      }
    }
    
    const getActivityIconClass = (type) => {
      switch (type) {
        case 'application': return 'bg-primary text-white'
        case 'approved': return 'bg-success text-white'
        case 'rejected': return 'bg-danger text-white'
        case 'pending': return 'bg-warning text-white'
        default: return 'bg-secondary text-white'
      }
    }
    
    const getStatusIcon = (status) => {
      const statusLower = status.toLowerCase()
      switch (statusLower) {
        case 'approved':
          return 'bi bi-check-circle text-success'
        case 'rejected':
          return 'bi bi-x-circle text-danger'
        case 'pending':
          return 'bi bi-clock text-warning'
        case 'draft':
          return 'bi bi-file-earmark-text text-warning'
        case 'no application':
          return 'bi bi-plus-circle text-secondary'
        default:
          return 'bi bi-info-circle text-info'
      }
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      const now = new Date()
      const diff = now - date
      const days = Math.floor(diff / (1000 * 60 * 60 * 24))
      
      if (days === 0) {
        const hours = Math.floor(diff / (1000 * 60 * 60))
        if (hours === 0) {
          const minutes = Math.floor(diff / (1000 * 60))
          return `${minutes} minutes ago`
        }
        return `${hours} hours ago`
      } else if (days === 1) {
        return 'Yesterday'
      } else if (days < 7) {
        return `${days} days ago`
      } else {
        return date.toLocaleDateString()
      }
    }

    onMounted(() => {
      loadDashboardData()
    })
    
    return {
      authStore,
      loading,
      totalApplications,
      pendingApplications,
      approvedApplications,
      rejectedApplications,
      applicationStatus,
      detailedStatusInfo,
      statusBadgeClass,
      recentActivities,
      getActivityIcon,
      getActivityIconClass,
      getStatusIcon,
      formatDate
    }
  }
}
</script>

<style scoped>
.dashboard-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1) !important;
}

.bg-primary {
  background: linear-gradient(135deg, #0d6efd 0%, #0056b3 100%) !important;
}

.border-bottom:last-child {
  border-bottom: none !important;
}
</style>
