terraform {
  required_providers {
    github = {
      source = "integrations/github"
      version = "6.7.0"
    }
  }

  backend "s3" {
    bucket = "terraform-github.com-tarik02-ha-template-media-player"
    region = "us-east-1"
    key    = "tfstate"
    use_lockfile = true
    endpoints = {
      s3 = "https://s3.tarik02.me"
    }
    skip_credentials_validation = true
    skip_requesting_account_id  = true
  }
}
