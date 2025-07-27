terraform {
  backend "local" {}
}
resource "null_resource" "deploy_compose" {
    provisioner "local-exec" {
        interpreter = ["/bin/bash", "-c"]
        command = <<-EOT
            echo user=>${var.user}<=
            sudo -u ${var.user} bash -lc '
                cd "${var.dir}" &&
                docker compose down &&
                docker compose up -d --build &&
                docker ps
            '
        EOT
    }
    triggers = {
        always_run = timestamp()
    }
}