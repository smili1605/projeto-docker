variable "do_token" {
  type = string
}

variable "ssh_public_key" {
  type = string
}

variable "ssh_key_name" {
  type    = string
  default = "projeto-docker-key"
}

variable "region" {
  type    = string
  default = "sfo2"
}

variable "size" {
  type    = string
  default = "s-1vcpu-2gb" # 1vCPU / 2GB RAM
}

variable "image" {
  type    = string
  default = "ubuntu-22-04-x64"
}
