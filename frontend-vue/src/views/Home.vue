<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section py-5">
      <div class="container">
        <div class="row align-items-center min-vh-70">
          <div class="col-lg-6">
            <div class="hero-content">
              <h1 class="display-4 fw-bold text-dark mb-4">
                <span class="text-primary">Uni</span>Admit
              </h1>
              <p class="lead text-muted mb-4 pe-lg-4">
                Streamlined university admission management system. 
                Your gateway to higher education made simple.
              </p>
              <div class="d-flex gap-3 flex-wrap">
                <router-link v-if="!authStore.isAuthenticated" to="/register" 
                  class="btn btn-primary btn-lg px-4 py-3 shadow-sm">
                  Start Your Journey
                </router-link>
                <router-link v-if="!authStore.isAuthenticated" to="/login" 
                  class="btn btn-outline-primary btn-lg px-4 py-3">
                  Sign In
                </router-link>
                <router-link v-if="authStore.isAuthenticated" to="/dashboard" 
                  class="btn btn-primary btn-lg px-4 py-3 shadow-sm">
                  Dashboard
                </router-link>
              </div>
            </div>
          </div>
          <div class="col-lg-6">
            <div class="hero-image text-center">
              <div class="illustration-box p-5">
                <div class="icon-container mb-4">
                  <div class="university-icon text-primary">
                    <svg width="120" height="120" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 3L1 9L12 15L21 12.09V17H23V9M5 13.18V17.18L12 21L19 17.18V13.18L12 17L5 13.18Z"/>
                    </svg>
                  </div>
                </div>
                <h5 class="text-muted fw-normal">Academic Excellence Portal</h5>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-5">
      <div class="container">
        <div class="row text-center mb-5">
          <div class="col-lg-8 mx-auto">
            <h2 class="h2 fw-bold text-dark mb-3">Why Choose UniAdmit</h2>
            <p class="text-muted">Built for modern university admission processes</p>
          </div>
        </div>
        
        <div class="row g-4">
          <div class="col-md-4">
            <div class="feature-card card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="feature-icon mb-3">
                  <div class="icon-circle bg-light text-primary">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>
                    </svg>
                  </div>
                </div>
                <h5 class="fw-semibold mb-3">Intuitive Process</h5>
                <p class="text-muted small">
                  User-friendly interface designed for seamless application submission and tracking.
                </p>
              </div>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="feature-card card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="feature-icon mb-3">
                  <div class="icon-circle bg-light text-primary">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z"/>
                    </svg>
                  </div>
                </div>
                <h5 class="fw-semibold mb-3">Secure Platform</h5>
                <p class="text-muted small">
                  Your personal information and documents are protected with enterprise-grade security.
                </p>
              </div>
            </div>
          </div>
          
          <div class="col-md-4">
            <div class="feature-card card h-100 border-0 shadow-sm">
              <div class="card-body text-center p-4">
                <div class="feature-icon mb-3">
                  <div class="icon-circle bg-light text-primary">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/>
                    </svg>
                  </div>
                </div>
                <h5 class="fw-semibold mb-3">Real-time Updates</h5>
                <p class="text-muted small">
                  Stay informed with instant notifications about your application status and progress.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How it Works Section -->
    <section class="py-5">
      <div class="container">
        <div class="row text-center mb-5">
          <div class="col-lg-8 mx-auto">
            <h2 class="h2 fw-bold text-dark mb-3">Application Process</h2>
            <p class="text-muted">Simple steps to apply</p>
          </div>
        </div>
        
        <div class="row g-4">
          <div class="col-lg-3 col-md-6">
            <div class="text-center">
              <div class="mb-3">
                <span class="badge bg-primary rounded-circle p-3">1</span>
              </div>
              <h6 class="fw-semibold mb-2">Register</h6>
              <p class="text-muted small">Create your account</p>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6">
            <div class="text-center">
              <div class="mb-3">
                <span class="badge bg-primary rounded-circle p-3">2</span>
              </div>
              <h6 class="fw-semibold mb-2">Apply</h6>
              <p class="text-muted small">Fill application form</p>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6">
            <div class="text-center">
              <div class="mb-3">
                <span class="badge bg-primary rounded-circle p-3">3</span>
              </div>
              <h6 class="fw-semibold mb-2">Submit</h6>
              <p class="text-muted small">Upload documents</p>
            </div>
          </div>
          
          <div class="col-lg-3 col-md-6">
            <div class="text-center">
              <div class="mb-3">
                <span class="badge bg-primary rounded-circle p-3">4</span>
              </div>
              <h6 class="fw-semibold mb-2">Track</h6>
              <p class="text-muted small">Monitor status</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-5 bg-light" v-if="!authStore.isAuthenticated">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-lg-8 text-center">
            <div class="cta-content">
              <h3 class="h3 fw-bold text-dark mb-3">Begin Your Academic Journey</h3>
              <p class="text-muted mb-4 px-lg-5">
                Join thousands of students who have successfully navigated their university 
                applications through our platform.
              </p>
              <div class="cta-buttons">
                <router-link to="/register" class="btn btn-primary btn-lg px-5 me-3 shadow-sm">
                  Get Started Today
                </router-link>
                <router-link to="/login" class="btn btn-outline-primary btn-lg px-4">
                  Already Registered?
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'
import { onMounted } from 'vue'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    
    onMounted(() => {
      // Initialize auth store
      authStore.init()
    })
    
    return {
      authStore
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
  padding: 80px 0;
}

.min-vh-70 {
  min-height: 70vh;
}

.hero-content {
  padding: 2rem 0;
}

.illustration-box {
  padding: 3rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 1rem;
  border: 1px solid #e9ecef;
}

.icon-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.university-icon {
  opacity: 0.9;
  filter: drop-shadow(0 4px 8px rgba(37, 99, 235, 0.1));
}

.feature-card {
  transition: all 0.3s ease;
  border: 1px solid #f1f3f4;
  background: #ffffff;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  border-color: #e9ecef;
}

.icon-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #e9ecef;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-buttons .btn {
  margin-bottom: 1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  border: none;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%);
  transform: translateY(-1px);
}

.btn-outline-primary {
  border: 2px solid #2563eb;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .hero-section {
    padding: 60px 0;
  }
  
  .hero-content {
    padding: 1rem 0;
  }
  
  .illustration-box {
    padding: 2rem;
    margin-top: 2rem;
  }
  
  .university-icon svg {
    width: 80px;
    height: 80px;
  }
  
  .cta-buttons .btn {
    width: 100%;
    margin-bottom: 0.75rem;
  }
}
</style>
