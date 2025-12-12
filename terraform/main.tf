provider "digitalocean" {
  token = var.do_token
}

resource "digitalocean_ssh_key" "default" {
  name       = var.ssh_key_name
  public_key = var.ssh_public_key
}

resource "digitalocean_droplet" "app" {
  name       = "projeto-docker-droplet"
  region     = var.region
  size       = var.size
  image      = var.image

  ssh_keys   = [digitalocean_ssh_key.default.fingerprint]

  backups    = false
  ipv6       = false
  monitoring = true

  user_data = file("${path.module}/cloud-init.yaml")

  tags = ["projeto-docker"]
}

resource "digitalocean_floating_ip" "fip" {
  droplet_id = digitalocean_droplet.app.id
  region     = var.region
}
