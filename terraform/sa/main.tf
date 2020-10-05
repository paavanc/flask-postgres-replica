
resource "google_service_account" "service_account"{
  account_id = "${var.cluser_name}-sm"
  display_name= var.sa_name_display_name
}

data "google_iam_policy" "workload-identity"{

  binding {
    role = "roles/iam.workloadIdentityUser"
    members = [
      "serviceAccount:${var.project}svc.id.goog[${var.name_space}/${var.k8_sa_account}]",
      "serviceAccount:${google_service_account.service_account.email}"
    ]
  }
  binding {
    role = "roles/secretmanager.secretAccessor"
    members = ["serviceAccount:${google_service_account.service_account.email}"]
  }
}
