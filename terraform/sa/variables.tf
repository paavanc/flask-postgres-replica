

variable "GOOGLE_APPLICATION_CREDENTIALS_FILE" {}

variable "terraform_bucket" {}

variable "name_space" {
  description = "k8 namespace for workflow identity"
  type        = string
}

variable "k8_sa_account" {
  description = "k8 sa account gcp account is tied too"
  type        = string
}
variable "region" {
  description = "The region for subnetworks in the network"
  type        = string
}

variable "project" {
  description = "The project ID for the network"
  type        = string
}

variable "cluster_name" {
  description = "The name of the cluster"
  type        = string
}

variable "sa_name_display_name" {
  description = "The name of the sa account"
  type        = string
}
