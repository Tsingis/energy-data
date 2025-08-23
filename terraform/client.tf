resource "google_cloud_run_service" "client" {
  name     = "energy-data-client"
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
        image = "${var.registry_server}/${var.project_id}/${var.registry_repository}/${var.registry_image_client}"

        ports {
          container_port = 3000
        }

        resources {
          limits = {
            cpu    = "1000m"
            memory = "500Mi"
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "public_client" {
  service  = google_cloud_run_service.client.name
  location = var.gcp_region
  role     = "roles/run.invoker"
  member   = "allUsers"
}