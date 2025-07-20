terraform {
  backend "local" {}
}
resource "null_resource" "deploy_compose" {
  provisioner "local-exec" {
    command = <<EOT
echo "Starting remote SSH..."
ssh -vvv -o StrictHostKeyChecking=no ${var.ssh_user}@${var.ssh_host} "cd ${var.app_dir} && echo 'In directory' && git pull && echo 'Git pulled' && docker compose up -d --build && echo 'Docker started'"
echo "SSH command completed"
EOT
    interpreter = ["PowerShell", "-Command"]
  }
  triggers = {
    always_run = timestamp()
  }
}
