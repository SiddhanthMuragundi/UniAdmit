<template>
  <div class="application-page">
    <div class="container py-4">
      <!-- Application Form -->
      <div class="card shadow-sm border-0">
        <div class="card-header">
          <h4 class="mb-0">University Application Form</h4>
        </div>
        <div class="card-body p-4">
          <!-- Form Instructions -->
          <div class="alert alert-info mb-4">
            <strong>Application Instructions:</strong>
            <ul class="mb-0 mt-2">
              <li>Fields marked with <span class="text-danger">*</span> are required</li>
              <li>Please ensure all information is accurate before submitting</li>
              <li>You can save your progress and continue later</li>
            </ul>
          </div>

          <!-- Progress Steps -->
          <div class="progress-steps mb-4">
            <div class="progress-step" :class="{ active: currentStep === 1, completed: currentStep > 1 }">
              <div class="progress-step-circle">1</div>
              <small>Basic Info</small>
            </div>
            <div class="progress-step" :class="{ active: currentStep === 2, completed: currentStep > 2 }">
              <div class="progress-step-circle">2</div>
              <small>Academic Details</small>
            </div>
            <div class="progress-step" :class="{ active: currentStep === 3, completed: currentStep > 3 }">
              <div class="progress-step-circle">3</div>
              <small>Documents</small>
            </div>
            <div class="progress-step" :class="{ active: currentStep === 4 }">
              <div class="progress-step-circle">4</div>
              <small>Review & Submit</small>
            </div>
          </div>

          <!-- Alert Messages -->
          <div v-if="successMessage" class="alert alert-success" role="alert">
            <i class="bi bi-check-circle me-2"></i>
            {{ successMessage }}
          </div>
          
          <div v-if="error" class="alert alert-danger" role="alert">
            <i class="bi bi-exclamation-triangle me-2"></i>
            {{ error }}
          </div>

          <!-- Draft Status Indicator -->
          <div v-if="isDraftLoaded" class="alert alert-warning" role="alert">
            <i class="bi bi-file-earmark-text me-2"></i>
            <strong>Editing Draft:</strong> Continuing from {{ getStepName(currentStep) }}. Your previous progress has been restored.
          </div>

          <!-- Step 1: Basic Information -->
          <div v-if="currentStep === 1" class="step-content">
            <h5 class="mb-4 fw-semibold">Step 1: Basic Information</h5>

            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="course" class="form-label">
                  Course Applied For <span class="text-danger">*</span>
                </label>
                <select
                  class="form-select"
                  id="course"
                  v-model="formData.course_applied"
                  required
                >
                  <option value="">Select Course</option>
                  <option value="Computer Science Engineering">Computer Science Engineering</option>
                  <option value="Electrical Engineering">Electrical Engineering</option>
                  <option value="Mechanical Engineering">Mechanical Engineering</option>
                  <option value="Civil Engineering">Civil Engineering</option>
                  <option value="Electronics Engineering">Electronics Engineering</option>
                  <option value="Business Administration">Business Administration</option>
                  <option value="Master of Computer Applications">Master of Computer Applications</option>
                  <option value="Master of Business Administration">Master of Business Administration</option>
                </select>
              </div>
              <div class="col-md-6 mb-3">
                <label for="graduation_year" class="form-label">
                  Expected Graduation Year <span class="text-danger">*</span>
                </label>
                <select
                  class="form-select"
                  id="graduation_year"
                  v-model="formData.graduation_year"
                  required
                >
                  <option value="">Select Year</option>
                  <option v-for="year in graduationYears" :key="year" :value="year">
                    {{ year }}
                  </option>
                </select>
              </div>
            </div>

            <div class="mb-3">
              <label for="previous_qualification" class="form-label">
                Previous Qualification <span class="text-danger">*</span>
              </label>
              <input
                type="text"
                class="form-control"
                id="previous_qualification"
                v-model="formData.previous_qualification"
                required
                placeholder="e.g., 12th Grade, Bachelor's Degree"
              >
            </div>

            <div class="mb-3">
              <label for="previous_institution" class="form-label">
                Previous Institution <span class="text-danger">*</span>
              </label>
              <input
                type="text"
                class="form-control"
                id="previous_institution"
                v-model="formData.previous_institution"
                required
                placeholder="Name of your previous school/college"
              >
            </div>
          </div>

          <!-- Step 2: Academic Details -->
          <div v-if="currentStep === 2" class="step-content">
            <h5 class="text-primary mb-3">
              <i class="bi bi-mortarboard me-2"></i>
              Step 2: Academic Details
            </h5>

            <h6 class="mb-3">Class 10th Details</h6>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="tenth_percentage" class="form-label">10th Percentage *</label>
                <input
                  type="number"
                  class="form-control"
                  id="tenth_percentage"
                  v-model="formData.tenth_percentage"
                  required
                  min="0"
                  max="100"
                  step="0.01"
                  placeholder="Enter percentage"
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="tenth_board" class="form-label">10th Board *</label>
                <select
                  class="form-select"
                  id="tenth_board"
                  v-model="formData.tenth_board"
                  required
                >
                  <option value="">Select Board</option>
                  <option value="CBSE">CBSE</option>
                  <option value="ICSE">ICSE</option>
                  <option value="State Board">State Board</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <h6 class="mb-3 mt-4">Class 12th Details</h6>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label for="twelfth_percentage" class="form-label">12th Percentage *</label>
                <input
                  type="number"
                  class="form-control"
                  id="twelfth_percentage"
                  v-model="formData.twelfth_percentage"
                  required
                  min="0"
                  max="100"
                  step="0.01"
                  placeholder="Enter percentage"
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="twelfth_board" class="form-label">12th Board *</label>
                <select
                  class="form-select"
                  id="twelfth_board"
                  v-model="formData.twelfth_board"
                  required
                >
                  <option value="">Select Board</option>
                  <option value="CBSE">CBSE</option>
                  <option value="ICSE">ICSE</option>
                  <option value="State Board">State Board</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            <h6 class="mb-3 mt-4">Address Details</h6>
            <div class="row">
              <div class="col-md-12 mb-3">
                <label for="address" class="form-label">Address *</label>
                <textarea
                  class="form-control"
                  id="address"
                  v-model="formData.address"
                  required
                  rows="2"
                  placeholder="Enter your full address"
                ></textarea>
              </div>
              <div class="col-md-6 mb-3">
                <label for="country" class="form-label">Country *</label>
                <input
                  type="text"
                  class="form-control"
                  id="country"
                  v-model="formData.country"
                  required
                  placeholder="Enter country"
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="state" class="form-label">State *</label>
                <input
                  type="text"
                  class="form-control"
                  id="state"
                  v-model="formData.state"
                  required
                  placeholder="Enter state"
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="district" class="form-label">District *</label>
                <input
                  type="text"
                  class="form-control"
                  id="district"
                  v-model="formData.district"
                  required
                  placeholder="Enter district"
                >
              </div>
              <div class="col-md-6 mb-3">
                <label for="pincode" class="form-label">Pincode *</label>
                <input
                  type="text"
                  class="form-control"
                  id="pincode"
                  v-model="formData.pincode"
                  required
                  placeholder="Enter pincode"
                  pattern="[0-9]{6}"
                  title="Please enter a valid 6-digit pincode"
                >
              </div>
            </div>
          </div>

          <!-- Step 3: Documents -->
          <div v-if="currentStep === 3" class="step-content">
            <h5 class="text-primary mb-3">
              <i class="bi bi-file-earmark-arrow-up me-2"></i>
              Step 3: Upload Documents
            </h5>

            <div class="mb-4">
              <label for="degree_certificate" class="form-label">Degree Certificate *</label>
              <div class="file-upload-area" @click="$refs.degreeInput.click()">
                <input
                  type="file"
                  ref="degreeInput"
                  @change="handleFileUpload($event, 'degree_certificate')"
                  accept=".pdf,.jpg,.jpeg,.png"
                  class="d-none"
                >
                <div v-if="!formData.degree_certificate" class="text-center">
                  <i class="bi bi-cloud-upload text-muted" style="font-size: 3rem;"></i>
                  <p class="mt-2 mb-1">Click to upload degree certificate</p>
                  <small class="text-muted">PDF, JPG, PNG files only (Max 5MB)</small>
                </div>
                <div v-else class="text-center">
                  <i class="bi bi-file-earmark-check text-success" style="font-size: 3rem;"></i>
                  <p class="mt-2 mb-1 text-success">{{ degreeCertificateName }}</p>
                  <small class="text-muted">Click to change file</small>
                </div>
              </div>
            </div>

            <div class="mb-4">
              <label for="id_proof" class="form-label">ID Proof *</label>
              <div class="file-upload-area" @click="$refs.idProofInput.click()">
                <input
                  type="file"
                  ref="idProofInput"
                  @change="handleFileUpload($event, 'id_proof')"
                  accept=".pdf,.jpg,.jpeg,.png"
                  class="d-none"
                >
                <div v-if="!formData.id_proof" class="text-center">
                  <i class="bi bi-cloud-upload text-muted" style="font-size: 3rem;"></i>
                  <p class="mt-2 mb-1">Click to upload ID proof</p>
                  <small class="text-muted">PDF, JPG, PNG files only (Max 5MB)</small>
                </div>
                <div v-else class="text-center">
                  <i class="bi bi-file-earmark-check text-success" style="font-size: 3rem;"></i>
                  <p class="mt-2 mb-1 text-success">{{ idProofName }}</p>
                  <small class="text-muted">Click to change file</small>
                </div>
              </div>
            </div>
          </div>

          <!-- Step 4: Review & Submit -->
          <div v-if="currentStep === 4" class="step-content">
            <h5 class="text-primary mb-3">
              <i class="bi bi-check-circle me-2"></i>
              Step 4: Review & Submit
            </h5>

            <div class="row">
              <div class="col-md-6">
                <h6>Basic Information</h6>
                <ul class="list-unstyled">
                  <li><strong>Course:</strong> {{ formData.course_applied }}</li>
                  <li><strong>Graduation Year:</strong> {{ formData.graduation_year }}</li>
                  <li><strong>Previous Qualification:</strong> {{ formData.previous_qualification }}</li>
                  <li><strong>Previous Institution:</strong> {{ formData.previous_institution }}</li>
                </ul>
              </div>
              <div class="col-md-6">
                <h6>Academic Details</h6>
                <ul class="list-unstyled">
                  <li><strong>10th Percentage:</strong> {{ formData.tenth_percentage }}%</li>
                  <li><strong>10th Board:</strong> {{ formData.tenth_board }}</li>
                  <li><strong>12th Percentage:</strong> {{ formData.twelfth_percentage }}%</li>
                  <li><strong>12th Board:</strong> {{ formData.twelfth_board }}</li>
                </ul>
                
                <h6 class="mt-3">Address Details</h6>
                <ul class="list-unstyled">
                  <li><strong>Address:</strong> {{ formData.address }}</li>
                  <li><strong>Country:</strong> {{ formData.country }}</li>
                  <li><strong>State:</strong> {{ formData.state }}</li>
                  <li><strong>District:</strong> {{ formData.district }}</li>
                  <li><strong>Pincode:</strong> {{ formData.pincode }}</li>
                </ul>
              </div>
            </div>

            <h6 class="mt-3">Uploaded Documents</h6>
            <ul class="list-unstyled">
              <li><i class="bi bi-file-earmark-check text-success me-2"></i>{{ degreeCertificateName }}</li>
              <li><i class="bi bi-file-earmark-check text-success me-2"></i>{{ idProofName }}</li>
            </ul>

            <div class="alert alert-info mt-3">
              <i class="bi bi-info-circle me-2"></i>
              Please review all information carefully before submitting. Once submitted, you cannot modify your application.
            </div>
          </div>

          <!-- Navigation Buttons -->
          <div class="d-flex justify-content-between mt-4">
            <div class="d-flex gap-2">
              <!-- Cancel Button - visible on all steps -->
              <button
                type="button"
                class="btn btn-outline-danger"
                @click="cancelApplication"
                :disabled="loading"
              >
                <i class="bi bi-x-circle me-2"></i>
                Cancel
              </button>
              
              <button
                v-if="currentStep > 1"
                type="button"
                class="btn btn-outline-secondary"
                @click="previousStep"
                :disabled="loading"
              >
                <i class="bi bi-arrow-left me-2"></i>
                Previous
              </button>
            </div>

            <div class="d-flex gap-2">
              <button
                v-if="currentStep < 4"
                type="button"
                class="btn btn-outline-primary"
                @click="saveDraft"
                :disabled="loading"
              >
                <span v-if="savingDraft" class="spinner-border spinner-border-sm me-2" role="status"></span>
                <i v-else class="bi bi-save me-2"></i>
                {{ savingDraft ? 'Saving...' : 'Save Draft' }}
              </button>

              <button
                v-if="currentStep < 4"
                type="button"
                class="btn btn-primary"
                @click="nextStep"
                :disabled="!canProceed || loading"
              >
                Next
                <i class="bi bi-arrow-right ms-2"></i>
              </button>

              <button
                v-if="currentStep === 4"
                type="button"
                class="btn btn-success btn-lg"
                @click="submitApplication"
                :disabled="loading"
              >
                <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                <i v-else class="bi bi-send me-2"></i>
                {{ loading ? 'Submitting...' : 'Submit Application' }}
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
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Application',
  setup() {
    const applicationStore = useApplicationStore()
    const authStore = useAuthStore()
    const router = useRouter()
    
    const currentStep = ref(1)
    const loading = ref(false)
    const savingDraft = ref(false)
    const error = ref('')
    const successMessage = ref('')
    const isDraftLoaded = ref(false)
    
    const formData = ref({
      course_applied: '',
      tenth_percentage: null,
      tenth_board: '',
      twelfth_percentage: null,
      twelfth_board: '',
      previous_qualification: '',
      previous_institution: '',
      graduation_year: null,
      address: '',
      country: '',
      state: '',
      district: '',
      pincode: '',
      degree_certificate: null,
      id_proof: null
    })
    
    const degreeCertificateName = ref('')
    const idProofName = ref('')
    
    const graduationYears = computed(() => {
      const currentYear = new Date().getFullYear()
      const years = []
      for (let i = currentYear; i <= currentYear + 6; i++) {
        years.push(i)
      }
      return years
    })
    
    const canProceed = computed(() => {
      switch (currentStep.value) {
        case 1:
          return formData.value.course_applied && 
                 formData.value.graduation_year && 
                 formData.value.previous_qualification && 
                 formData.value.previous_institution
        case 2:
          return formData.value.tenth_percentage && 
                 formData.value.tenth_board && 
                 formData.value.twelfth_percentage && 
                 formData.value.twelfth_board &&
                 formData.value.address && 
                 formData.value.country && 
                 formData.value.state && 
                 formData.value.district && 
                 formData.value.pincode
        case 3:
          return formData.value.degree_certificate && formData.value.id_proof
        default:
          return true
      }
    })
    
    const nextStep = () => {
      if (canProceed.value && currentStep.value < 4) {
        currentStep.value++
        error.value = ''
        successMessage.value = ''
      }
    }
    
    const previousStep = () => {
      if (currentStep.value > 1) {
        currentStep.value--
        error.value = ''
        successMessage.value = ''
      }
    }
    
    const handleFileUpload = (event, fieldName) => {
      const file = event.target.files[0]
      if (!file) return
      
      // Validate file size (5MB)
      if (file.size > 5 * 1024 * 1024) {
        error.value = 'File size must be less than 5MB'
        return
      }
      
      // Validate file type
      const allowedTypes = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
      if (!allowedTypes.includes(file.type)) {
        error.value = 'Only PDF, JPG, and PNG files are allowed'
        return
      }
      
      formData.value[fieldName] = file
      
      if (fieldName === 'degree_certificate') {
        degreeCertificateName.value = file.name
      } else if (fieldName === 'id_proof') {
        idProofName.value = file.name
      }
      
      error.value = ''
    }
    
    const saveDraft = async () => {
      savingDraft.value = true
      error.value = ''
      
      const result = await applicationStore.saveDraft(formData.value)
      
      if (result.success) {
        successMessage.value = 'Draft saved successfully!'
      } else {
        error.value = result.error
      }
      
      savingDraft.value = false
    }
    
    const submitApplication = async () => {
      loading.value = true
      error.value = ''
      
      // Prepare form data with files and address from form
      const submitData = {
        ...formData.value
      }
      
      const result = await applicationStore.submitApplication(submitData)
      
      if (result.success) {
        successMessage.value = 'Application submitted successfully!'
        setTimeout(() => {
          router.push('/dashboard')
        }, 2000)
      } else {
        error.value = result.error
      }
      
      loading.value = false
    }
    
    const loadDraft = async () => {
      try {
        const result = await applicationStore.getDraft()
        if (result.success && result.draft) {
          // Load all draft data into the form including address fields
          Object.keys(result.draft).forEach(key => {
            if (formData.value.hasOwnProperty(key)) {
              // Convert numeric values properly and handle empty strings
              if (key.includes('percentage') || key === 'graduation_year') {
                formData.value[key] = result.draft[key] || ''
              } else {
                formData.value[key] = result.draft[key] || ''
              }
            }
          })
          
          // Update file names if files exist (for existing drafts with files)
          if (result.draft.degree_certificate && result.draft.degree_certificate !== 'draft') {
            degreeCertificateName.value = result.draft.degree_certificate_filename || 'Degree Certificate'
          }
          if (result.draft.id_proof && result.draft.id_proof !== 'draft') {
            idProofName.value = result.draft.id_proof_filename || 'ID Proof'
          }
          
          // Set draft loaded flag
          isDraftLoaded.value = true
          
          // Determine the appropriate step based on filled data
          currentStep.value = determineCurrentStep()
          
          console.log('Draft loaded successfully for editing:', result.draft)
          console.log('Starting at step:', currentStep.value)
        } else {
          isDraftLoaded.value = false
          console.log('No draft found, starting fresh application')
        }
      } catch (error) {
        console.error('Error loading draft:', error)
        error.value = 'Failed to load draft application'
        isDraftLoaded.value = false
      }
    }
    
    const determineCurrentStep = () => {
      // Step 1: Basic Info (course, graduation year, previous qualification/institution)
      const hasBasicInfo = formData.value.course_applied && 
                          formData.value.graduation_year && 
                          formData.value.previous_qualification && 
                          formData.value.previous_institution
      
      // Step 2: Academic Details (10th and 12th marks)
      const hasAcademicInfo = formData.value.tenth_percentage && 
                             formData.value.tenth_board && 
                             formData.value.twelfth_percentage && 
                             formData.value.twelfth_board
      
      // Step 3: Documents (files uploaded)
      const hasDocuments = (degreeCertificateName.value && degreeCertificateName.value !== 'No file chosen') &&
                          (idProofName.value && idProofName.value !== 'No file chosen')
      
      // Determine step based on completion
      if (hasDocuments) {
        return 4 // Review step - everything is filled
      } else if (hasAcademicInfo) {
        return 3 // Documents step - academic info is complete
      } else if (hasBasicInfo) {
        return 2 // Academic step - basic info is complete
      } else {
        return 1 // Basic info step - start from beginning
      }
    }
    
    const getStepName = (step) => {
      const stepNames = {
        1: 'Basic Information',
        2: 'Academic Details', 
        3: 'Documents Upload',
        4: 'Review & Submit'
      }
      return stepNames[step] || 'Unknown Step'
    }
    
    const cancelApplication = () => {
      // Show confirmation dialog
      if (confirm('Are you sure you want to cancel? Any unsaved changes will be lost.')) {
        // Reset form data
        formData.value = {
          course_applied: '',
          graduation_year: '',
          previous_qualification: '',
          previous_institution: '',
          tenth_percentage: '',
          tenth_board: '',
          twelfth_percentage: '',
          twelfth_board: '',
          degree_certificate: null,
          id_proof: null
        }
        
        // Reset step and messages
        currentStep.value = 1
        error.value = ''
        successMessage.value = ''
        
        // Navigate back to dashboard
        router.push('/dashboard')
      }
    }
    
    onMounted(async () => {
      // Check if user has profile data to populate address fields
      if (authStore.user) {
        formData.value.address = authStore.user.address || ''
        formData.value.country = authStore.user.country || ''
        formData.value.state = authStore.user.state || ''
        formData.value.district = authStore.user.district || ''
        formData.value.pincode = authStore.user.pincode || ''
      }
      
      // Load draft data if available
      await loadDraft()
    })
    
    return {
      currentStep,
      loading,
      savingDraft,
      error,
      successMessage,
      isDraftLoaded,
      formData,
      degreeCertificateName,
      idProofName,
      graduationYears,
      canProceed,
      nextStep,
      previousStep,
      handleFileUpload,
      saveDraft,
      submitApplication,
      cancelApplication,
      determineCurrentStep,
      getStepName
    }
  }
}
</script>

<style scoped>
.application-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.step-content {
  min-height: 400px;
}

.file-upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 10px;
  padding: 2rem;
  text-align: center;
  transition: all 0.3s ease;
  cursor: pointer;
  background-color: #fafafa;
}

.file-upload-area:hover {
  border-color: var(--bs-primary);
  background-color: #f8f9ff;
}

.progress-steps {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
  position: relative;
}

.progress-step {
  flex: 1;
  text-align: center;
  position: relative;
}

.progress-step::after {
  content: '';
  position: absolute;
  top: 20px;
  left: 50%;
  width: 100%;
  height: 2px;
  background-color: #dee2e6;
  z-index: 1;
}

.progress-step:last-child::after {
  display: none;
}

.progress-step.completed::after {
  background-color: var(--bs-success);
}

.progress-step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #dee2e6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin: 0 auto 0.5rem;
  position: relative;
  z-index: 2;
}

.progress-step.active .progress-step-circle {
  background-color: var(--bs-primary);
}

.progress-step.completed .progress-step-circle {
  background-color: var(--bs-success);
}
</style>
