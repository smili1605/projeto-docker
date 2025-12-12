terraform {
  cloud {
    organization = "ProjetoDocker"

    workspaces {
      name = "projeto-docker"
    }
  }

  # ADIÇÃO PROBLEMÁTICA: Versão incompatível
  required_version = ">= 99.0.0"  # <-- Isso vai causar erro!
}

