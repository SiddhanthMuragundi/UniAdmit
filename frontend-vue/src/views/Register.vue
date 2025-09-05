<template>
  <div class="register-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg border-0 rounded-4">
            <div class="card-header text-center py-4">
              <h3 class="mb-1 text-white">Create Your Account</h3>
              <p class="mb-0 text-white-50">Join UniAdmit to start your application</p>
            </div>
            <div class="card-body p-4">
              <!-- Form Instructions -->
              <div class="form-text mb-3 text-center">
                Fields marked with <span class="text-danger">*</span> are required
              </div>

              <!-- Alert for errors -->
              <div v-if="error" class="alert alert-danger" role="alert">
                {{ error }}
              </div>

              <form @submit.prevent="handleRegister">
                <!-- Personal Information -->
                <h5 class="mb-3 fw-semibold">Personal Information</h5>

                <div class="row">
                  <div class="col-md-12 mb-3">
                    <label for="name" class="form-label">
                      Full Name <span class="text-danger">*</span>
                    </label>
                    <input
                      type="text"
                      class="form-control"
                      id="name"
                      v-model="formData.name"
                      required
                      :disabled="loading"
                      placeholder="Enter your full name"
                    >
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="email" class="form-label">
                      Email Address <span class="text-danger">*</span>
                    </label>
                    <input
                      type="email"
                      class="form-control"
                      id="email"
                      v-model="formData.email"
                      required
                      :disabled="loading"
                      placeholder="Enter your email"
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="phone" class="form-label">Phone Number *</label>
                    <input
                      type="tel"
                      class="form-control"
                      id="phone"
                      v-model="formData.phone"
                      required
                      :disabled="loading"
                      placeholder="10-digit phone number"
                      pattern="[0-9]{10}"
                      maxlength="10"
                    >
                  </div>
                </div>

                <div class="mb-3">
                  <label for="password" class="form-label">Password *</label>
                  <div class="input-group">
                    <input
                      :type="showPassword ? 'text' : 'password'"
                      class="form-control"
                      id="password"
                      v-model="formData.password"
                      required
                      :disabled="loading"
                      placeholder="Enter your password"
                      minlength="6"
                    >
                    <button
                      type="button"
                      class="btn btn-outline-secondary"
                      @click="showPassword = !showPassword"
                      :disabled="loading"
                    >
                      <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                    </button>
                  </div>
                  <div class="form-text">Password must be at least 6 characters long</div>
                </div>

                <!-- Address Information -->
                <h5 class="mb-3 text-primary mt-4">
                  <i class="bi bi-geo-alt me-2"></i>
                  Address Information
                </h5>

                <div class="mb-3">
                  <label for="address" class="form-label">Street Address *</label>
                  <textarea
                    class="form-control"
                    id="address"
                    v-model="formData.address"
                    required
                    :disabled="loading"
                    placeholder="Enter your complete address"
                    rows="3"
                  ></textarea>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="country" class="form-label">Country *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="country"
                      v-model="formData.country"
                      required
                      :disabled="loading"
                      placeholder="Enter your country"
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="state" class="form-label">State/Province *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="state"
                      v-model="formData.state"
                      required
                      :disabled="loading"
                      placeholder="Enter your state/province"
                    >
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="district" class="form-label">District/City *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="district"
                      v-model="formData.district"
                      required
                      :disabled="loading"
                      placeholder="Enter your district/city"
                    >
                  </div>
                  <div class="col-md-6 mb-3">
                    <label for="pincode" class="form-label">PIN/ZIP Code *</label>
                    <input
                      type="text"
                      class="form-control"
                      id="pincode"
                      v-model="formData.pincode"
                      required
                      :disabled="loading"
                      placeholder="Enter PIN/ZIP code"
                      maxlength="10"
                    >
                  </div>
                </div>

                <div class="d-grid mt-4">
                  <button
                    type="submit"
                    class="btn btn-primary btn-lg"
                    :disabled="loading"
                  >
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    <i v-else class="bi bi-person-plus me-2"></i>
                    {{ loading ? 'Creating Account...' : 'Create Account' }}
                  </button>
                </div>
              </form>

              <hr class="my-4">

              <div class="text-center">
                <p class="mb-0">
                  Already have an account?
                  <router-link to="/login" class="text-decoration-none">
                    Login here
                  </router-link>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'Register',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const formData = ref({
      name: '',
      email: '',
      phone: '',
      password: '',
      address: '',
      country: '',
      state: '',
      district: '',
      pincode: ''
    })
    
    const showPassword = ref(false)
    const loading = ref(false)
    const error = ref('')
    
    const handleRegister = async () => {
      error.value = ''
      loading.value = true
      
      // Validate phone number
      if (!/^[0-9]{10}$/.test(formData.value.phone)) {
        error.value = 'Phone number must be exactly 10 digits'
        loading.value = false
        return
      }
      
      const result = await authStore.register(formData.value)
      
      if (result.success) {
        // Redirect to login with success message
        router.push({
          name: 'Login',
          query: { message: 'Registration successful! Please login with your credentials.' }
        })
      } else {
        error.value = result.error
      }
      
      loading.value = false
    }
    
    return {
      formData,
      showPassword,
      loading,
      error,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  padding: 2rem 0;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

.form-label {
  font-weight: 600;
  color: #495057;
}

.text-primary {
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 0.5rem;
}

.input-group .btn {
  border-left: none;
}

.form-control:focus + .btn,
.form-control:focus {
  border-color: #86b7fe;
}
</style>
