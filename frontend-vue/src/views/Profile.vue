<template>
  <div class="profile-page">
    <div class="container py-4">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <div class="card shadow-sm border-0">
            <div class="card-header bg-primary text-white">
              <h4 class="mb-0">
                <i class="bi bi-person-circle me-2"></i>
                My Profile
              </h4>
            </div>
            <div class="card-body p-4">
              <!-- Success/Error Messages -->
              <div v-if="successMessage" class="alert alert-success" role="alert">
                <i class="bi bi-check-circle me-2"></i>
                {{ successMessage }}
              </div>
              
              <div v-if="error" class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                {{ error }}
              </div>

              <!-- Profile Information -->
              <div v-if="!editing" class="profile-view">
                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">Full Name</label>
                      <p class="fs-5">{{ authStore.user?.name }}</p>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">Email Address</label>
                      <p class="fs-5">
                        <i class="bi bi-envelope me-2 text-primary"></i>
                        {{ authStore.user?.email }}
                      </p>
                      <small class="text-muted">Email cannot be changed</small>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">Phone Number</label>
                      <p class="fs-5">
                        <i class="bi bi-telephone me-2 text-success"></i>
                        {{ authStore.user?.phone }}
                      </p>
                      <small class="text-muted">Phone cannot be changed</small>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">Account Type</label>
                      <p class="fs-5">
                        <span class="badge bg-info fs-6">
                          <i class="bi bi-shield-check me-1"></i>
                          {{ authStore.user?.roles?.join(', ') }}
                        </span>
                      </p>
                    </div>
                  </div>
                </div>

                <hr class="my-4">

                <h5 class="text-primary mb-3">
                  <i class="bi bi-geo-alt me-2"></i>
                  Address Information
                </h5>

                <div class="mb-3">
                  <label class="form-label fw-bold text-muted">Street Address</label>
                  <p class="fs-6">{{ authStore.user?.address }}</p>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">Country</label>
                      <p class="fs-6">{{ authStore.user?.country }}</p>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">State/Province</label>
                      <p class="fs-6">{{ authStore.user?.state }}</p>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">District/City</label>
                      <p class="fs-6">{{ authStore.user?.district }}</p>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="mb-3">
                      <label class="form-label fw-bold text-muted">PIN/ZIP Code</label>
                      <p class="fs-6">{{ authStore.user?.pincode }}</p>
                    </div>
                  </div>
                </div>

                <div class="text-center mt-4">
                  <button @click="startEditing" class="btn btn-primary btn-lg">
                    <i class="bi bi-pencil me-2"></i>
                    Edit Profile
                  </button>
                </div>
              </div>

              <!-- Edit Profile Form -->
              <div v-else class="profile-edit">
                <form @submit.prevent="handleUpdate">
                  <h5 class="text-primary mb-3">
                    <i class="bi bi-pencil me-2"></i>
                    Edit Profile Information
                  </h5>

                  <div class="mb-3">
                    <label for="edit-name" class="form-label">Full Name *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="edit-name"
                      v-model="editForm.name"
                      required
                      :disabled="loading"
                    >
                  </div>

                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="form-label">Email Address</label>
                        <input
                          type="email"
                          class="form-control"
                          :value="authStore.user?.email"
                          disabled
                        >
                        <small class="text-muted">Email cannot be changed</small>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label class="form-label">Phone Number</label>
                        <input
                          type="tel"
                          class="form-control"
                          :value="authStore.user?.phone"
                          disabled
                        >
                        <small class="text-muted">Phone cannot be changed</small>
                      </div>
                    </div>
                  </div>

                  <h6 class="text-primary mb-3 mt-4">
                    <i class="bi bi-geo-alt me-2"></i>
                    Address Information
                  </h6>

                  <div class="mb-3">
                    <label for="edit-address" class="form-label">Street Address *</label>
                    <textarea
                      class="form-control"
                      id="edit-address"
                      v-model="editForm.address"
                      required
                      :disabled="loading"
                      rows="3"
                    ></textarea>
                  </div>

                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label for="edit-country" class="form-label">Country *</label>
                        <select
                          class="form-select"
                          id="edit-country"
                          v-model="editForm.country"
                          required
                          :disabled="loading"
                        >
                          <option value="">Select Country</option>
                          <option value="India">India</option>
                          <option value="USA">United States</option>
                          <option value="UK">United Kingdom</option>
                          <option value="Canada">Canada</option>
                          <option value="Australia">Australia</option>
                          <option value="Other">Other</option>
                        </select>
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label for="edit-state" class="form-label">State/Province *</label>
                        <input
                          type="text"
                          class="form-control"
                          id="edit-state"
                          v-model="editForm.state"
                          required
                          :disabled="loading"
                        >
                      </div>
                    </div>
                  </div>

                  <div class="row">
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label for="edit-district" class="form-label">District/City *</label>
                        <input
                          type="text"
                          class="form-control"
                          id="edit-district"
                          v-model="editForm.district"
                          required
                          :disabled="loading"
                        >
                      </div>
                    </div>
                    <div class="col-md-6">
                      <div class="mb-3">
                        <label for="edit-pincode" class="form-label">PIN/ZIP Code *</label>
                        <input
                          type="text"
                          class="form-control"
                          id="edit-pincode"
                          v-model="editForm.pincode"
                          required
                          :disabled="loading"
                          maxlength="10"
                        >
                      </div>
                    </div>
                  </div>

                  <div class="d-flex gap-2 justify-content-end mt-4">
                    <button
                      type="button"
                      class="btn btn-secondary"
                      @click="cancelEditing"
                      :disabled="loading"
                    >
                      <i class="bi bi-x me-2"></i>
                      Cancel
                    </button>
                    <button
                      type="submit"
                      class="btn btn-primary"
                      :disabled="loading"
                    >
                      <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                      <i v-else class="bi bi-check me-2"></i>
                      {{ loading ? 'Updating...' : 'Update Profile' }}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Profile',
  setup() {
    const authStore = useAuthStore()
    
    const editing = ref(false)
    const loading = ref(false)
    const error = ref('')
    const successMessage = ref('')
    
    const editForm = ref({
      name: '',
      address: '',
      country: '',
      state: '',
      district: '',
      pincode: ''
    })
    
    const startEditing = () => {
      // Populate edit form with current user data
      editForm.value = {
        name: authStore.user?.name || '',
        address: authStore.user?.address || '',
        country: authStore.user?.country || '',
        state: authStore.user?.state || '',
        district: authStore.user?.district || '',
        pincode: authStore.user?.pincode || ''
      }
      editing.value = true
      error.value = ''
      successMessage.value = ''
    }
    
    const cancelEditing = () => {
      editing.value = false
      error.value = ''
      successMessage.value = ''
    }
    
    const handleUpdate = async () => {
      loading.value = true
      error.value = ''
      successMessage.value = ''
      
      const result = await authStore.updateProfile(editForm.value)
      
      if (result.success) {
        successMessage.value = 'Profile updated successfully!'
        editing.value = false
      } else {
        error.value = result.error
      }
      
      loading.value = false
    }
    
    onMounted(async () => {
      // Ensure we have the latest user data
      await authStore.getProfile()
    })
    
    return {
      authStore,
      editing,
      loading,
      error,
      successMessage,
      editForm,
      startEditing,
      cancelEditing,
      handleUpdate
    }
  }
}
</script>

<style scoped>
.profile-page {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.card {
  border-radius: 12px;
}

.form-label {
  font-weight: 600;
  color: #495057;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge {
  font-size: 0.9rem !important;
}

.profile-view p {
  margin-bottom: 0.25rem;
}

.profile-view small {
  font-style: italic;
}
</style>
