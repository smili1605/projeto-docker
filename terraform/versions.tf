terraform {
  required_version = ">= 1.5.0"

  backend "remote" {
    organization = "ProjetoDocker"

    workspaces {
      name = "projeto-docker"
    }
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}
