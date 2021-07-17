provider "google" {
  project = var.gcp_project
  region  = "us-east1"
  zone    = "us-east1-b"
}

resource "google_pubsub_topic" "topic" {
  name = var.topic_name
}

resource "google_storage_bucket" "bucket" {
  name = var.bucket_name
}


resource "google_storage_bucket_object" "archive" {
  name   = "twitter-app-function.zip"
  bucket = google_storage_bucket.bucket.name
  source = "function.zip"
}

resource "google_cloudfunctions_function" "function" {
  name                  = var.lambda_name
  description           = "reads in pub_sub and does the data cleaning and stores to firestore"
  available_memory_mb   = 128
  runtime               = "python38"
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  environment_variables = {
    "ES_HOST_URL" = var.ES_HOST_URL
  }
  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.topic.name
  }

  timeout     = 80
  entry_point = "handle_request"

}

resource "google_container_cluster" "primary" {
  name        = var.name
  project     = var.gcp_project
  description = "Twitter Cluster"
  location    = var.location

  remove_default_node_pool = true
  initial_node_count       = var.initial_node_count

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "${var.name}-node-pool"
  project    = var.gcp_project
  location   = var.location
  cluster    = google_container_cluster.primary.name
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = var.machine_type

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}
