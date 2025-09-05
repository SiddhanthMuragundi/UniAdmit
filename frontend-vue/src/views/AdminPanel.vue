<template>
  <div class="admin-panel">
    <div class="container-fluid py-4">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col">
          <div class="card border-0 bg-gradient-primary text-white">
            <div class="card-body p-4">
              <h2 class="mb-0">
                <i class="bi bi-shield-check me-2"></i>
                Admin Panel
              </h2>
              <p class="mb-0 opacity-75">Manage student applications and system settings</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="mb-2">
                <i class="bi bi-files text-primary" style="font-size: 2.5rem;"></i>
              </div>
              <h3 class="text-primary">{{ totalApplications }}</h3>
              <p class="text-muted mb-0">Total Applications</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="mb-2">
                <i class="bi bi-hourglass-split text-warning" style="font-size: 2.5rem;"></i>
              </div>
              <h3 class="text-warning">{{ pendingCount }}</h3>
              <p class="text-muted mb-0">Pending Review</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="mb-2">
                <i class="bi bi-check-circle text-success" style="font-size: 2.5rem;"></i>
              </div>
              <h3 class="text-success">{{ approvedCount }}</h3>
              <p class="text-muted mb-0">Approved</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="mb-2">
                <i class="bi bi-x-circle text-danger" style="font-size: 2.5rem;"></i>
              </div>
              <h3 class="text-danger">{{ rejectedCount }}</h3>
              <p class="text-muted mb-0">Rejected</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Applications Table -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <div class="row align-items-center">
            <div class="col">
              <h5 class="mb-0">
                <i class="bi bi-table me-2"></i>
                Application Management
              </h5>
            </div>
            <div class="col-auto">
              <div class="d-flex gap-2">
                <!-- Filter Dropdown -->
                <div class="dropdown">
                  <button class="btn btn-outline-primary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <i class="bi bi-funnel me-1"></i>
                    {{ currentFilter === 'all' ? 'All Status' : currentFilter.charAt(0).toUpperCase() + currentFilter.slice(1) }}
                  </button>
                  <ul class="dropdown-menu">
                    <li><a class="dropdown-item" href="#" @click="setFilter('all')">All Status</a></li>
                    <li><a class="dropdown-item" href="#" @click="setFilter('pending')">Pending</a></li>
                    <li><a class="dropdown-item" href="#" @click="setFilter('approved')">Approved</a></li>
                    <li><a class="dropdown-item" href="#" @click="setFilter('rejected')">Rejected</a></li>
                  </ul>
                </div>
                <!-- Refresh Button -->
                <button class="btn btn-outline-secondary" @click="refreshApplications" :disabled="loading">
                  <i class="bi bi-arrow-clockwise" :class="{ 'spin': loading }"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="card-body p-0">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-2 text-muted">Loading applications...</p>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredApplications.length === 0" class="text-center py-5">
            <i class="bi bi-inbox text-muted" style="font-size: 4rem;"></i>
            <h5 class="mt-3 text-muted">No applications found</h5>
            <p class="text-muted">No applications match the current filter criteria.</p>
          </div>

          <!-- Applications Table -->
          <div v-else class="table-responsive">
            <table class="table table-hover mb-0">
              <thead class="bg-light">
                <tr>
                  <th>ID</th>
                  <th>Student Name</th>
                  <th>Course</th>
                  <th>Applied Date</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="application in paginatedApplications" :key="application.id">
                  <td class="fw-bold">#{{ application.id }}</td>
                  <td>
                    <div class="d-flex align-items-center">
                      <div class="avatar-circle me-2">
                        {{ application.student?.name?.charAt(0)?.toUpperCase() }}
                      </div>
                      <div>
                        <div class="fw-semibold">{{ application.student?.name }}</div>
                        <small class="text-muted">{{ application.student?.email }}</small>
                      </div>
                    </div>
                  </td>
                  <td>{{ application.course_applied }}</td>
                  <td>{{ formatDate(application.date_created) }}</td>
                  <td>
                    <span :class="getStatusBadgeClass(application.status)" class="badge">
                      {{ application.status.charAt(0).toUpperCase() + application.status.slice(1) }}
                    </span>
                  </td>
                  <td>
                    <div class="btn-group" role="group">
                      <button
                        class="btn btn-sm btn-outline-primary"
                        @click="viewApplication(application)"
                        title="View Details"
                      >
                        <i class="bi bi-eye"></i>
                      </button>
                      <button
                        v-if="application.status === 'pending'"
                        class="btn btn-sm btn-outline-success"
                        @click="approveApplication(application)"
                        title="Approve"
                      >
                        <i class="bi bi-check"></i>
                      </button>
                      <button
                        v-if="application.status === 'pending'"
                        class="btn btn-sm btn-outline-danger"
                        @click="rejectApplication(application)"
                        title="Reject"
                      >
                        <i class="bi bi-x"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="d-flex justify-content-center p-3">
            <nav>
              <ul class="pagination mb-0">
                <li class="page-item" :class="{ disabled: currentPage === 1 }">
                  <button class="page-link" @click="setPage(currentPage - 1)" :disabled="currentPage === 1">
                    Previous
                  </button>
                </li>
                <li
                  v-for="page in visiblePages"
                  :key="page"
                  class="page-item"
                  :class="{ active: page === currentPage }"
                >
                  <button class="page-link" @click="setPage(page)">{{ page }}</button>
                </li>
                <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                  <button class="page-link" @click="setPage(currentPage + 1)" :disabled="currentPage === totalPages">
                    Next
                  </button>
                </li>
              </ul>
            </nav>
          </div>
        </div>
      </div>
    </div>

    <!-- Application Details Modal -->
    <div class="modal fade" id="applicationModal" tabindex="-1" aria-labelledby="applicationModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="applicationModalLabel">
              <i class="bi bi-file-earmark-text me-2"></i>
              Application Details
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedApplication">
            <!-- Student Information -->
            <h6 class="text-primary mb-3">Student Information</h6>
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>Name:</strong> {{ selectedApplication.student?.name }}
              </div>
              <div class="col-md-6">
                <strong>Email:</strong> {{ selectedApplication.student?.email }}
              </div>
            </div>
            <div class="row mb-4">
              <div class="col-md-6">
                <strong>Phone:</strong> {{ selectedApplication.student?.phone }}
              </div>
              <div class="col-md-6">
                <strong>Applied Date:</strong> {{ formatDate(selectedApplication.date_created) }}
              </div>
            </div>

            <!-- Course Information -->
            <h6 class="text-primary mb-3">Course Information</h6>
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>Course:</strong> {{ selectedApplication.course_applied }}
              </div>
              <div class="col-md-6">
                <strong>Graduation Year:</strong> {{ selectedApplication.graduation_year }}
              </div>
            </div>
            <div class="row mb-4">
              <div class="col-md-6">
                <strong>Previous Qualification:</strong> {{ selectedApplication.previous_qualification }}
              </div>
              <div class="col-md-6">
                <strong>Previous Institution:</strong> {{ selectedApplication.previous_institution }}
              </div>
            </div>

            <!-- Academic Details -->
            <h6 class="text-primary mb-3">Academic Details</h6>
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>10th Percentage:</strong> {{ selectedApplication.tenth_percentage }}%
              </div>
              <div class="col-md-6">
                <strong>10th Board:</strong> {{ selectedApplication.tenth_board }}
              </div>
            </div>
            <div class="row mb-4">
              <div class="col-md-6">
                <strong>12th Percentage:</strong> {{ selectedApplication.twelfth_percentage }}%
              </div>
              <div class="col-md-6">
                <strong>12th Board:</strong> {{ selectedApplication.twelfth_board }}
              </div>
            </div>

            <!-- Address Details -->
            <h6 class="text-primary mb-3">Address Details</h6>
            <div class="row mb-3">
              <div class="col-md-12">
                <strong>Address:</strong> {{ selectedApplication.address }}
              </div>
            </div>
            <div class="row mb-4">
              <div class="col-md-6">
                <strong>Country:</strong> {{ selectedApplication.country }}
              </div>
              <div class="col-md-6">
                <strong>State:</strong> {{ selectedApplication.state }}
              </div>
            </div>
            <div class="row mb-4">
              <div class="col-md-6">
                <strong>District:</strong> {{ selectedApplication.district }}
              </div>
              <div class="col-md-6">
                <strong>Pincode:</strong> {{ selectedApplication.pincode }}
              </div>
            </div>

            <!-- Documents Section -->
            <h6 class="text-primary mb-3">Uploaded Documents</h6>
            <div class="row mb-4">
              <div class="col-md-6">
                <div class="card">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i class="bi bi-file-earmark-pdf me-2"></i>
                      Degree Certificate
                    </h6>
                    <p class="card-text text-muted">{{ selectedApplication.degree_certificate_filename }}</p>
                    <div class="btn-group btn-group-sm">
                      <button 
                        class="btn btn-outline-primary"
                        @click="downloadDocument(selectedApplication.id, 'degree_certificate')"
                        :disabled="!selectedApplication.has_degree_certificate"
                      >
                        <i class="bi bi-download me-1"></i>Download
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              <div class="col-md-6">
                <div class="card">
                  <div class="card-body">
                    <h6 class="card-title">
                      <i class="bi bi-file-earmark-image me-2"></i>
                      ID Proof
                    </h6>
                    <p class="card-text text-muted">{{ selectedApplication.id_proof_filename }}</p>
                    <div class="btn-group btn-group-sm">
                      <button 
                        class="btn btn-outline-primary"
                        @click="downloadDocument(selectedApplication.id, 'id_proof')"
                        :disabled="!selectedApplication.has_id_proof"
                      >
                        <i class="bi bi-download me-1"></i>Download
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Status and Review -->
            <h6 class="text-primary mb-3">Application Status</h6>
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>Current Status:</strong>
                <span :class="getStatusBadgeClass(selectedApplication.status)" class="badge ms-2">
                  {{ selectedApplication.status.charAt(0).toUpperCase() + selectedApplication.status.slice(1) }}
                </span>
              </div>
              <div class="col-md-6" v-if="selectedApplication.reviewed_at">
                <strong>Reviewed Date:</strong> {{ formatDate(selectedApplication.reviewed_at) }}
              </div>
            </div>
            <div v-if="selectedApplication.review_comments" class="mb-3">
              <strong>Review Comments:</strong>
              <p class="mt-1 p-2 bg-light rounded">{{ selectedApplication.review_comments }}</p>
            </div>

            <!-- Review Actions -->
            <div v-if="selectedApplication.status === 'pending'" class="mt-4">
              <h6 class="text-primary mb-3">Review Application</h6>
              <div class="mb-3">
                <label for="reviewComments" class="form-label">Review Comments</label>
                <textarea
                  class="form-control"
                  id="reviewComments"
                  v-model="reviewComments"
                  rows="3"
                  placeholder="Add your review comments here..."
                ></textarea>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <div v-if="selectedApplication?.status === 'pending'" class="btn-group">
              <button
                type="button"
                class="btn btn-success"
                @click="approveApplicationFromModal"
                :disabled="reviewLoading"
              >
                <span v-if="reviewLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                <i v-else class="bi bi-check me-2"></i>
                Approve
              </button>
              <button
                type="button"
                class="btn btn-danger"
                @click="rejectApplicationFromModal"
                :disabled="reviewLoading"
              >
                <span v-if="reviewLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                <i v-else class="bi bi-x me-2"></i>
                Reject
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useApplicationStore } from '../stores/application'
import { Modal } from 'bootstrap'

export default {
  name: 'AdminPanel',
  setup() {
    const applicationStore = useApplicationStore()
    
    const loading = ref(false)
    const reviewLoading = ref(false)
    const applications = ref([])
    const selectedApplication = ref(null)
    const reviewComments = ref('')
    const currentFilter = ref('all')
    const currentPage = ref(1)
    const itemsPerPage = 10
    
    // Computed properties
    const totalApplications = computed(() => applications.value.length)
    const pendingCount = computed(() => applications.value.filter(app => app.status === 'pending').length)
    const approvedCount = computed(() => applications.value.filter(app => app.status === 'approved').length)
    const rejectedCount = computed(() => applications.value.filter(app => app.status === 'rejected').length)
    
    const filteredApplications = computed(() => {
      if (currentFilter.value === 'all') {
        return applications.value
      }
      return applications.value.filter(app => app.status === currentFilter.value)
    })
    
    const totalPages = computed(() => Math.ceil(filteredApplications.value.length / itemsPerPage))
    
    const paginatedApplications = computed(() => {
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      return filteredApplications.value.slice(start, end)
    })
    
    const visiblePages = computed(() => {
      const pages = []
      const total = totalPages.value
      const current = currentPage.value
      
      if (total <= 7) {
        for (let i = 1; i <= total; i++) {
          pages.push(i)
        }
      } else {
        if (current <= 4) {
          for (let i = 1; i <= 5; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        } else if (current >= total - 3) {
          pages.push(1)
          pages.push('...')
          for (let i = total - 4; i <= total; i++) {
            pages.push(i)
          }
        } else {
          pages.push(1)
          pages.push('...')
          for (let i = current - 1; i <= current + 1; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        }
      }
      
      return pages
    })
    
    // Methods
    const refreshApplications = async () => {
      loading.value = true
      try {
        const result = await applicationStore.getAllApplications()
        if (result.success) {
          applications.value = result.applications
        }
      } catch (error) {
        console.error('Error loading applications:', error)
      } finally {
        loading.value = false
      }
    }
    
    const setFilter = (filter) => {
      currentFilter.value = filter
      currentPage.value = 1
    }
    
    const setPage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page
      }
    }
    
    const viewApplication = (application) => {
      selectedApplication.value = application
      reviewComments.value = application.review_comments || ''
      const modal = new Modal(document.getElementById('applicationModal'))
      modal.show()
    }
    
    const approveApplication = async (application) => {
      if (confirm('Are you sure you want to approve this application?')) {
        await updateApplicationStatus(application.id, 'approved')
      }
    }
    
    const rejectApplication = async (application) => {
      if (confirm('Are you sure you want to reject this application?')) {
        await updateApplicationStatus(application.id, 'rejected')
      }
    }
    
    const approveApplicationFromModal = async () => {
      await updateApplicationStatus(selectedApplication.value.id, 'approved', reviewComments.value)
      const modal = Modal.getInstance(document.getElementById('applicationModal'))
      modal.hide()
    }
    
    const rejectApplicationFromModal = async () => {
      await updateApplicationStatus(selectedApplication.value.id, 'rejected', reviewComments.value)
      const modal = Modal.getInstance(document.getElementById('applicationModal'))
      modal.hide()
    }
    
    const updateApplicationStatus = async (applicationId, status, comments = '') => {
      reviewLoading.value = true
      try {
        const result = await applicationStore.updateApplicationStatus(applicationId, status, comments)
        if (result.success) {
          // Update local application data
          const appIndex = applications.value.findIndex(app => app.id === applicationId)
          if (appIndex !== -1) {
            applications.value[appIndex].status = status
            applications.value[appIndex].review_comments = comments
            applications.value[appIndex].reviewed_at = new Date().toISOString()
          }
          
          // Update selected application if it's the same
          if (selectedApplication.value?.id === applicationId) {
            selectedApplication.value.status = status
            selectedApplication.value.review_comments = comments
            selectedApplication.value.reviewed_at = new Date().toISOString()
          }
        }
      } catch (error) {
        console.error('Error updating application status:', error)
      } finally {
        reviewLoading.value = false
      }
    }
    
    const getStatusBadgeClass = (status) => {
      switch (status) {
        case 'pending':
          return 'bg-warning text-dark'
        case 'approved':
          return 'bg-success'
        case 'rejected':
          return 'bg-danger'
        case 'draft':
          return 'bg-secondary'
        default:
          return 'bg-secondary'
      }
    }
    
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const downloadDocument = async (applicationId, documentType) => {
      try {
        const token = localStorage.getItem('token')
        const response = await fetch(`/api/application/admin/document/${applicationId}/${documentType}?action=download`, {
          headers: {
            'Authentication-Token': token
          }
        })

        if (response.ok) {
          // Get filename from response headers or use default
          const contentDisposition = response.headers.get('Content-Disposition')
          let filename = `${documentType}.pdf`
          if (contentDisposition) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition)
            if (matches != null && matches[1]) {
              filename = matches[1].replace(/['"]/g, '')
            }
          }

          // Create download link
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = url
          link.download = filename
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(url)
        } else {
          console.error('Failed to download document')
          alert('Failed to download document')
        }
      } catch (error) {
        console.error('Error downloading document:', error)
        alert('Error downloading document')
      }
    }
    
    onMounted(() => {
      refreshApplications()
    })
    
    return {
      loading,
      reviewLoading,
      applications,
      selectedApplication,
      reviewComments,
      currentFilter,
      currentPage,
      totalApplications,
      pendingCount,
      approvedCount,
      rejectedCount,
      filteredApplications,
      paginatedApplications,
      totalPages,
      visiblePages,
      refreshApplications,
      setFilter,
      setPage,
      viewApplication,
      approveApplication,
      rejectApplication,
      approveApplicationFromModal,
      rejectApplicationFromModal,
      getStatusBadgeClass,
      formatDate,
      downloadDocument
    }
  }
}
</script>

<style scoped>
.admin-panel {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.bg-gradient-primary {
  background: linear-gradient(135deg, #0d6efd 0%, #0056b3 100%);
}

.avatar-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #6c757d;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.875rem;
}

.table-hover tbody tr:hover {
  background-color: rgba(13, 110, 253, 0.05);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.btn-group .btn {
  border-radius: 0.375rem !important;
  margin-right: 0.25rem;
}

.btn-group .btn:last-child {
  margin-right: 0;
}

.page-link {
  color: #0d6efd;
}

.page-item.active .page-link {
  background-color: #0d6efd;
  border-color: #0d6efd;
}
</style>
