output "droplet_ip" {
  description = "IP público do Droplet"
  value       = digitalocean_droplet.app.ipv4_address
}

output "droplet_id" {
  description = "ID do droplet"
  value       = digitalocean_droplet.app.id
}

output "floating_ip" {
  description = "Floating IP (se alocado)"
  value       = try(digitalocean_floating_ip.fip.ip, "")
}
