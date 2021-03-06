
provider "google" {
  credentials = "${var.GOOGLE_APPLICATION_CREDENTIALS_FILE}"
  project     = "${var.project}"
  region      = "${var.region}"
  
} 

provider "google-beta" {
  credentials = "${var.GOOGLE_APPLICATION_CREDENTIALS_FILE}"
  project     = "${var.project}"
  region      = "${var.region}"
  alias   = "gb"
  version = "~> 3.10"
} 