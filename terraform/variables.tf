variable "gcp_region" {
  type    = string
  default = "europe-north1"
}

variable "project_id" {
  type      = string
  sensitive = true
}

variable "registry_server" {
  type    = string
  default = "docker.io"
}

variable "registry_image_server" {
  type = string
}

variable "registry_image_client" {
  type = string
}

variable "fingrid_api_key" {
  type      = string
  sensitive = true
}