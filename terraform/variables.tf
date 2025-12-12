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
  default = "nyc3"
}

variable "size" {
  type    = string
  default = "s-1vcpu-2gb"
}

variable "image" {
  type    = string
  default = "ubuntu-22-04-x64"
}
