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
      sudo -u ${var.user} cd "${var.dir}"
    EOT
  }
  triggers = {
    always_run = timestamp()
  }
}