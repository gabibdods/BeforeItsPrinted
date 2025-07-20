terraform {
    backend "local" {}
}
resource "null_resource" "deploy_compose" {
    provisioner "local-exec" {
        command = "ssh ${var.ssh_user}@${var.ssh_host} 'set -e; export PORT=${var.port}; export TROP=${var.trop}; cd ${var.app_dir} && git pull && docker compose up -d --build'"
        interpreter = ["PowerShell", "-Command"]
    }
    triggers = {
        always_run = timestamp()
    }
}