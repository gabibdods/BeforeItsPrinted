terraform {
  backend "local" {}
}
resource "null_resource" "deploy_compose" {
  provisioner "local-exec" {
    command = "ssh -o StrictHostKeyChecking=no ${var.ssh_user}@${var.ssh_host} \"cd ${var.app_dir} && git pull && docker-compose -f infrastructure/docker-compose.yaml up -d --build\""
  }
  triggers = {
    always_run = timestamp()
  }
}
