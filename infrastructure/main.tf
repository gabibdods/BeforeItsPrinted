variable "ssh_user" {}
variable "ssh_host" {}

resource "null_resource" "deploy_compose" {
	provisioner "local_exec" {
		command = <<EOT
			ssh ${var.ssh_user}@${ssh_host}
				cd /home/${var.ssh_user}/app &&
				git pull &&
				docker-compose -f infra/docker-compose.yaml up -d --build
			'
		EOT
	}
}