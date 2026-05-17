# Ansible Playbook Templates

This directory contains ready-to-use Ansible playbooks for common infrastructure and application tasks.

## 📂 Available Templates

### Application Deployment
- **`deploy-app.yml`** - Zero-downtime application deployment with health checks and rollback
- **`rollback-app.yml`** - Rollback to previous application version

### Docker Operations
- **`docker-deploy.yml`** - Deploy Docker Compose stacks
- **`docker-cleanup.yml`** - Clean up Docker resources (images, containers, volumes)
- **`docker-health-check.yml`** - Verify Docker daemon and containers health

### Database Operations
- **`backup-database.yml`** - Backup PostgreSQL databases with rotation
- **`restore-database.yml`** - Restore database from backup

### Monitoring & Health
- **`health-check-system.yml`** - Comprehensive system health check
- **`collect-metrics.yml`** - Collect and report system metrics

### Maintenance
- **`system-update.yml`** - Update system ppackages with safe reboot handling
- **`cleanup-logs.yml`** - Clean up old log files

## 🚀 Quick Start

### 1. Copy Template

```bash
cp .github/templates/ansible/deploy-app.yml ansible/playbooks/
```

### 2. Customize Variables

Edit the vars section in the playbook:

```yaml
vars:
  app_name: "myapp"
  app_version: "1.0.0"
  app_path: "/opt/myapp"
```

### 3. Run Playbook

```bash
# Test first with --check
ansible-playbook -i inventory/production ansible/playbooks/deploy-app.yml --check

# Execute deployment
ansible-playbook -i inventory/production ansible/playbooks/deploy-app.yml
```

## 📋 Usage Guidelines

### Before Running

1. **Review variables** - Adjust all variables for your environment
2. **Test with --check** - Always dry-run first
3. **Limit scope** - Use `--limit` to test on subset of hosts
4. **Backup data** - Ensure backups exist before destructive operations

### Security

- Store sensitive variables in Ansible Vault
- Never commit credentials to version control
- Use environment-specific inventory files
- Review privilege escalation settings

### Best Practices

- Tag playbooks for selective execution
- Implement error handlers and rollback
- Add descriptive task names
- Use blocks for logical grouping
- Enable verbose output for debugging (`-vvv`)

## 🔧 Customization

### Adding vault Support

```yaml
vars:
  db_password: "{{ vault_db_password }}"
```

Then decrypt during execution:

```bash
ansible-playbook playbook.yml --ask-vault-pass
```

### Adding Notifications

Add handlers for Slack/email:

```yaml
handlers:
  - name: notify slack
    community.general.slack:
      token: "{{ slack_token }}"
      msg: "Deployment completed on {{ inventory_hostname }}"
```

### Error Handling

```yaml
tasks:
  - name: Deploy application
    block:
      - name: Deploy task
        # ... deploy logic
    rescue:
      - name: Rollback
        # ... rollback logic
    always:
      - name: Cleanup
        # ... cleanup logic
```

## 📚 Further Reading

- [`docs/ANSIBLE_BEST_PRACTICES.md`](../../../docs/ANSIBLE_BEST_PRACTICES.md) - Comprehensive Ansible best practices
- [`docs/MOLECULE_TESTING_GUIDE.md`](../../../docs/MOLECULE_TESTING_GUIDE.md) - Testing playbooks with Molecule
- [`docs/ANSIBLE_PLAYBOOK_TEMPLATES.md`](../../../docs/ANSIBLE_PLAYBOOK_TEMPLATES.md) - Detailed playbook examples

## ⚠️ Important Notes

- These templates are **starting points** - always customize for your needs
- Test thoroughly in non-production environments first
- Keep templates updated with your organization's standards
- Document any customizations made to templates

---

**Template Version**: 1.0.0
**Maintained By**: Enterprise Template Team
