terraform {
  backend "local" {}
}
resource "null_resource" "deploy_compose" {
    provisioner "local-exec" {
        command = <<EOT
            echo "Starting SSH command...";
            ssh -vvv ${var.ssh_user}@${var.ssh_host} <<'EOF'
                set -e
                export POSTGRES_USER="${var.postgres_user}"
                export POSTGRES_PASSWORD="${var.postgres_pass}"
                export PORT="${var.port}"
                export TROP="${var.trop}"
                cd "${var.app_dir}"
                pwd
                git pull
                git status
                docker compose down
                docker ps
                docker compose up -d --build
                docker ps -a
            EOF
            echo "SSH command completed"
        EOT
        interpreter = ["bash", "-c"]
    }
    triggers = {
        always_run = timestamp()
    }
}