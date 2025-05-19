resource "google_cloud_run_service" "server" {
  name     = "energy-data-server"
  location = var.gcp_region

  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/minScale" = "0"
        "autoscaling.knative.dev/maxScale" = "1"
      }
    }

    spec {
      container_concurrency = 10

      containers {
        image = "${var.registry_server}/${var.registry_image_server}"

        ports {
          container_port = 8000
        }

        resources {
          limits = {
            cpu    = "1000m"
            memory = "500Mi"
          }
        }

        env {
          name  = "ENVIRONMENT"
          value = "prod"
        }

        env {
          name  = "ALLOWED_ORIGIN"
          value = google_cloud_run_service.client.status[0].url
        }

        env {
          name  = "CACHE_TTL"
          value = "300"
        }

        env {
          name  = "RATE_LIMIT"
          value = "10/minute"
        }

        env {
          name  = "FINGRID_API_KEY"
          value = var.fingrid_api_key
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public_server" {
  service  = google_cloud_run_service.server.name
  location = var.gcp_region
  role     = "roles/run.invoker"
  member   = "allUsers"
}