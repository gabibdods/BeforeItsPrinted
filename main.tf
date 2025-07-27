variable "dir" {
  type = string
}
variable "user" {
  type = string
}
resource "null_resource" "deploy_compose" {
  provisioner "local-exec" {
    interpreter = ["/bin/bash", "-xc"]
    command = <<-EOT
      sudo -u ${var.user} bash -lc 'cd "${var.dir}"'
      sudo -u ${var.user} bash -lc 'docker compose down'
      sudo -u ${var.user} bash -lc 'docker compose up -d --build'
    EOT
  }
  triggers = {
    always_run = timestamp()
  }
}