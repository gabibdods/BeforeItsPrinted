terraform {
  backend "local" {}
}
resource "null_resource" "deploy_compose" {
    provisioner "local-exec" {
        command = <<EOT
        ssh ${var.ssh_user}@${var.ssh_host} 'set -e;
            export POSTGRES_USER="${var.postgres_user}";
            export POSTGRES_PASSWORD="${var.postgres_pass}";
            export PORT="${var.port}";
            export TROP="${var.trop}";
            cd "${var.app_dir}" &&
            git pull &&
            docker compose down &&
            docker compose up -d --build'
        EOT
        interpreter = ["PowerShell", "-Command"]
    }
    triggers = {
        always_run = timestamp()
    }
}