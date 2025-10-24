provider "github" {
}

resource "github_repository" "this" {
  name       = "ha-template-media-player"
  visibility = "private"

  has_downloads = true
  has_issues    = true
  has_projects  = true

  allow_auto_merge    = true
  allow_update_branch = true

  allow_merge_commit   = true
  merge_commit_title   = "PR_TITLE"
  merge_commit_message = "BLANK"

  allow_squash_merge          = true
  squash_merge_commit_title   = "PR_TITLE"
  squash_merge_commit_message = "BLANK"

  allow_rebase_merge = false

  delete_branch_on_merge = true
}

resource "github_branch" "master" {
  repository = github_repository.this.name
  branch     = "master"
}

resource "github_branch_default" "this" {
  repository = github_repository.this.name
  branch     = github_branch.master.branch
}

resource "github_repository_ruleset" "master" {
  name       = "master"
  repository = github_repository.this.name

  target      = "branch"
  enforcement = "active"

  conditions {
    ref_name {
      include = [
        "refs/heads/${github_branch.master.branch}",
      ]
      exclude = []
    }
  }

  rules {
    creation                = true
    deletion                = true
    required_linear_history = false
    non_fast_forward        = true

    pull_request {
    }

    required_status_checks {
      required_check {
        context        = "lint"
        integration_id = var.github_actions_app_id
      }

      required_check {
        context        = "validate"
        integration_id = var.github_actions_app_id
      }
    }
  }
}
