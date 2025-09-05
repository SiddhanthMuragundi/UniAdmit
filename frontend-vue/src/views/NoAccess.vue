<template>
  <div class="no-access-page">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 text-center">
          <div class="card">
            <div class="card-body py-5">
              <div class="mb-4">
                <i class="bi bi-shield-x text-muted" style="font-size: 4rem;"></i>
              </div>
              <h3 class="mb-3">Access Denied</h3>
              <p class="text-muted mb-4">
                You don't have permission to access this page.
              </p>
              <router-link to="/dashboard" class="btn btn-primary">
                Go to Dashboard
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NoAccess'
}
</script>

<style scoped>
.no-access-page {
  background-color: #f8f9fa;
  min-height: 100vh;
  display: flex;
  align-items: center;
}
</style>
