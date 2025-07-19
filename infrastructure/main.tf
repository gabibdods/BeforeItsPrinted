resource "null_resource" "deploy_compose" {
	provisioner "local_exec" {
		command = <<EOT
ssh ${var.ssh_user}@{var.ssh_host} <<'REMOTE'
	cd ${var.app_dir} &&
	git pull &&
	docker-compose -f infrastructure/docker-compose.yaml up -d --build
REMOTE
EOT
	}
}