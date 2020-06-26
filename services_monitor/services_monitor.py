def __update_services_data(self):
        # Find all of the hamlet services
        result = subprocess.run(["systemctl", "list-units", "--type=service", "--no-pager", "|", "grep", "hamlet", "|", "cut", "-f", "1", "-d", "'.'"], stdout=subprocess.PIPE)
        all_services = result.stdout.decode('utf-8').split()
        # Verify each service is in the services table