
resource "google_service_account" "service_account"{
  account_id = "${var.cluster_name}-sm"
  display_name= var.sa_name_display_name
}

data "google_iam_policy" "workload-identity-sa"{

  binding {
    role = "roles/iam.workloadIdentityUser"
    members = [
      "serviceAccount:${var.project}.svc.id.goog[${var.name_space}/${var.k8_sa_account}"],
    ]
  }
}

data "google_iam_policy" "workload-identity-project"{

  binding {
    role = "roles/secretmanager.secretAccessor"
    members = [
      "serviceAccount:${google_service_account.service_account.email}"],
    ]
  }
}

resource "google_service_account_iam_policy" "workload-identity-iam"{
  service_account_id = google_service_account.service_account.name
  policy_data = data.google_iam_policy.workload-identity-sa.policy_data
}

resource "google_project_iam_policy" "project-main"{
  project = var.project
  policy_data  = data.google_iam_policy.workload-identity-project.policy_data
}
