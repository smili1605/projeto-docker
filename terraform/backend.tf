terraform {
  cloud {
    organization = "ProjetoDocker"

    workspaces {
      name = "projeto-docker"
    }
  }
  
  required_version = ">= 1.5.0, < 2.0.0"
}