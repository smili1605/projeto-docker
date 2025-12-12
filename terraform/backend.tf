terraform {
  backend "remote" {
    organization = "ProjetoDocker"

    workspaces {
      name = "projeto-docker"
    }
  }
}
