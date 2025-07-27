terraform {
  backend "local" {}
}
resource "null_resource" "deploy_compose" {
    provisioner "local-exec" {
        interpreter = ["/bin/bash", "-c"]
        inline = [
            "cd \"${var.app_dir}\"",
            "docker compose down",
            "docker compose up -d --build",
            "docker ps",
        ]
    }
    triggers = {
        always_run = timestamp()
    }
}