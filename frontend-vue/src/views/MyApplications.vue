<template>
  <div class="my-applications-page">
    <div class="container py-4">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h1 class="h3 mb-1">My Applications</h1>
              <p class="text-muted">View and track your admission applications</p>
            </div>
            <router-link to="/application" class="btn btn-primary">
              <i class="bi bi-plus-circle me-2"></i>
              New Application
            </router-link>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-muted">Loading your applications...</p>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="alert alert-danger" role="alert">
        <i class="bi bi-exclamation-triangle me-2"></i>
        {{ error }}
      </div>

      <!-- No Applications -->
      <div v-else-if="applications.length === 0" class="text-center py-5">
        <div class="mb-4">
          <i class="bi bi-file-earmark-text text-muted" style="font-size: 4rem;"></i>
        </div>
        <h4 class="text-muted">No Applications Found</h4>
        <p class="text-muted mb-4">You haven't submitted any applications yet.</p>
        <router-link to="/application" class="btn btn-primary">
          <i class="bi bi-plus-circle me-2"></i>
          Submit Your First Application
        </router-link>
      </div>

      <!-- Applications List -->
      <div v-else class="row">
        <div class="col-12">
          <div class="row g-4">
            <div v-for="application in applications" :key="application.id" class="col-md-6 col-lg-4">
              <div class="card h-100 shadow-sm">
                <div class="card-header bg-white">
                  <div class="d-flex justify-content-between align-items-center">
                    <h6 class="card-title mb-0">
                      Application #{{ application.id }}
                    </h6>
                    <span :class="getStatusBadgeClass(application.status)" class="badge">
                      {{ application.status.charAt(0).toUpperCase() + application.status.slice(1) }}
                    </span>
                  </div>
                </div>
                <div class="card-body">
                  <div class="mb-3">
                    <strong>Course Applied:</strong><br>
                    <span class="text-primary">{{ application.course_applied }}</span>
                  </div>
                  
                  <div class="mb-3">
                    <strong>Submitted:</strong><br>
                    <small class="text-muted">{{ formatDate(application.date_created) }}</small>
                  </div>

                  <div v-if="application.reviewed_at" class="mb-3">
                    <strong>Reviewed:</strong><br>
                    <small class="text-muted">{{ formatDate(application.reviewed_at) }}</small>
                    <div v-if="application.reviewed_by" class="mt-1">
                      <small class="text-muted">by {{ application.reviewed_by }}</small>
                    </div>
                  </div>

                  <div v-if="application.review_comments" class="mb-3">
                    <strong>Comments:</strong><br>
                    <small class="text-muted">{{ application.review_comments }}</small>
                  </div>
                </div>
                <div class="card-footer bg-white">
                  <div class="d-grid gap-2">
                    <button 
                      class="btn btn-outline-primary btn-sm"
                      @click="viewApplication(application)"
                    >
                      <i class="bi bi-eye me-2"></i>
                      View Details
                    </button>
                    
                    <!-- Offer Letter Download Button for Approved Applications -->
                    <button 
                      v-if="application.status === 'approved'"
                      class="btn btn-success btn-sm"
                      @click="downloadOfferLetter(application.id)"
                    >
                      <i class="bi bi-download me-2"></i>
                      Download Offer Letter
                    </button>
                  </div>
                </div>
              </div>
            </div>
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
            <!-- Course Information -->
            <h6 class="text-primary mb-3">Course Information</h6>
            <div class="row mb-3">
              <div class="col-md-6">
                <strong>Course Applied:</strong> {{ selectedApplication.course_applied }}
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

            <!-- Offer Letter Section for Approved Applications -->
            <div v-if="selectedApplication.status === 'approved'" class="mt-4">
              <h6 class="text-success mb-3">
                <i class="bi bi-check-circle me-2"></i>
                Congratulations! Your Application has been Approved
              </h6>
              <div class="alert alert-success" role="alert">
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <strong>🎉 Admission Confirmed!</strong><br>
                    <small>Your offer letter is ready for download</small>
                  </div>
                  <button 
                    class="btn btn-success"
                    @click="downloadOfferLetter(selectedApplication.id)"
                  >
                    <i class="bi bi-download me-2"></i>
                    Download Offer Letter
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useApplicationStore } from '../stores/application'
import { Modal } from 'bootstrap'

export default {
  name: 'MyApplications',
  setup() {
    const applicationStore = useApplicationStore()
    const loading = ref(false)
    const error = ref('')
    const applications = ref([])
    const selectedApplication = ref(null)

    const loadApplications = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const response = await fetch('http://localhost:5000/api/application/list', {
          headers: {
            'Authentication-Token': localStorage.getItem('auth_token')
          }
        })

        if (response.ok) {
          const data = await response.json()
          applications.value = data.applications
        } else {
          const errorData = await response.json()
          error.value = errorData.error || 'Failed to load applications'
        }
      } catch (err) {
        error.value = 'Failed to load applications'
        console.error('Error loading applications:', err)
      } finally {
        loading.value = false
      }
    }

    const viewApplication = (application) => {
      selectedApplication.value = application
      const modal = new Modal(document.getElementById('applicationModal'))
      modal.show()
    }

    const downloadDocument = async (applicationId, documentType) => {
      try {
        const token = localStorage.getItem('auth_token')
        const response = await fetch(`http://localhost:5000/api/application/document/${applicationId}/${documentType}?action=download`, {
          headers: {
            'Authentication-Token': token
          }
        })

        if (response.ok) {
          const contentDisposition = response.headers.get('Content-Disposition')
          let filename = `${documentType}.pdf`
          if (contentDisposition) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition)
            if (matches != null && matches[1]) {
              filename = matches[1].replace(/['"]/g, '')
            }
          }

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
          alert('Failed to download document')
        }
      } catch (error) {
        console.error('Error downloading document:', error)
        alert('Error downloading document')
      }
    }

    const downloadOfferLetter = async (applicationId) => {
      try {
        const token = localStorage.getItem('auth_token')
        const response = await fetch(`http://localhost:5000/api/application/offer-letter/${applicationId}`, {
          headers: {
            'Authentication-Token': token
          }
        })

        if (response.ok) {
          const contentDisposition = response.headers.get('Content-Disposition')
          let filename = 'offer_letter.pdf'
          if (contentDisposition) {
            const matches = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/.exec(contentDisposition)
            if (matches != null && matches[1]) {
              filename = matches[1].replace(/['"]/g, '')
            }
          }

          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = url
          link.download = filename
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(url)

          // Show success message
          alert('Offer letter downloaded successfully!')
        } else {
          const errorData = await response.json()
          alert(errorData.error || 'Failed to download offer letter')
        }
      } catch (error) {
        console.error('Error downloading offer letter:', error)
        alert('Error downloading offer letter')
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

    onMounted(() => {
      loadApplications()
    })

    return {
      loading,
      error,
      applications,
      selectedApplication,
      loadApplications,
      viewApplication,
      downloadDocument,
      downloadOfferLetter,
      getStatusBadgeClass,
      formatDate
    }
  }
}
</script>

<style scoped>
.my-applications-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  border-bottom: 1px solid #e9ecef;
}

.card-footer {
  border-top: 1px solid #e9ecef;
}

.badge {
  font-size: 0.75rem;
}

.btn-group-sm .btn {
  font-size: 0.75rem;
}
</style>
