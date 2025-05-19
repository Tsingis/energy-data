output "server_service_url" {
  value = google_cloud_run_service.server.status[0].url
}

output "client_service_url" {
  value = google_cloud_run_service.client.status[0].url
}

