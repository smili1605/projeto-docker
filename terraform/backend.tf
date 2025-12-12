terraform {
  backend "remote" {
    hostname = "app.terraform.io"
    organization = "ProjetoDocker"

    workspaces {
      name = "projeto-docker"
    }
  }
}
