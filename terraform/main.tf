terraform {
required_providers {
digitalocean = {
source = "digitalocean/digitalocean"
version = "~> 2.22"
}
}
}


provider "digitalocean" {
token = var.do_token
}


# SSH key resource: o conteúdo da chave pública será passado via variável
resource "digitalocean_ssh_key" "default" {
name = var.ssh_key_name
public_key = var.ssh_public_key
}


resource "digitalocean_droplet" "app" {
name = "projeto-docker-droplet"
region = var.region
size = var.size
image = var.image
ssh_keys = [digitalocean_ssh_key.default.fingerprint]
backups = false
ipv6 = false
monitoring = true
user_data = file("${path.module}/cloud-init.yaml")
tags = ["projeto-docker"]
}


# Optional Floating IP (not required but handy)
resource "digitalocean_floating_ip" "fip" {
droplet_id = digitalocean_droplet.app.id
region = var.region
}