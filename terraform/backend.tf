terraform {
  cloud {
    organization = "ProjetoDocker"

    workspaces {
      name = "projeto-docker"
    }
  }

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.22"
    }
  }
}
