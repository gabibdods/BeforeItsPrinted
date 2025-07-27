terraform {
  backend "local" {}
}
resource "null_resource" "deploy_compose" {
    provisioner "local-exec" {
        interpreter = ["/bin/bash", "-c"]
        command = <<-EOT
            sudo -u ${var.user} bash -lc "cd ${var.dir}";
            sudo -u ${var.user} docker compose down;
            sudo -u ${var.user} docker compose up -d --build;
            sudo -u ${var.user} docker ps;
        EOT
    }
    triggers = {
        always_run = timestamp()
    }
}