terraform {
  cloud {
    organization = "ProjetoDocker"

    workspaces {
      name = "projeto-docker"
    }
  }
}
