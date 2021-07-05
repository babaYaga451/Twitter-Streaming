provider "google" {
  project = var.gcp_project
  region  = "us-central1"
  zone    = "us-central1-c"
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

  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.topic.name
  }

  timeout     = 80
  entry_point = "handle_request"

}