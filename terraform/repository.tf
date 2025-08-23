resource "google_artifact_registry_repository" "server_repo" {
  project       = var.project_id
  location      = var.gcp_region
  repository_id = var.registry_repository
  format        = "DOCKER"
  description   = "Docker images"

  vulnerability_scanning_config {
    enablement_config = "DISABLED"
  }

  cleanup_policies {
    id     = "keep most recent"
    action = "KEEP"
    most_recent_versions {
      keep_count = 1
    }
  }
}