# Ansible Best Practices Guide

> Comprehensive guide to writing maintainable, secure, and efficient Ansible automation.

## 📑 Table of Contents

- [Core Principles](#core-principles)
- [Project Structure](#project-structure)
- [Inventory Management](#inventory-management)
- [Playbook Design](#playbook-design)
- [Role Development](#role-development)
- [Variable Management](#variable-management)
- [Security Best Practices](#security-best-practices)
- [Testing and Validation](#testing-and-validation)
- [Performance Optimization](#performance-optimization)
- [Error Handling](#error-handling)
- [Documentation](#documentation)
- [CI/CD Integration](#cicd-integration)

---

## Core Principles

### 1. Idempotency

**Definition**: Running a playbook multiple times should produce the same result without unwanted side effects.

✅ **Good** (Idempotent):
```yaml
- name: Ensure nginx is installed
  ansible.builtin.apt:
    name: nginx
    state: present
```

❌ **Bad** (Not Idempotent):
```yaml
- name: Install nginx
  ansible.builtin.shell: apt-get install -y nginx
```

**Why**: The `apt` module checks if nginx is already installed. The `shell` command always executes, potentially causing errors or unnecessary operations.

### 2. Declarative Over Imperative

Describe **what** you want, not **how** to achieve it.

✅ **Good** (Declarative):
```yaml
- name: Ensure user exists
  ansible.builtin.user:
    name: appuser
    state: present
    groups: docker
    shell: /bin/bash
```

❌ **Bad** (Imperative):
```yaml
- name: Create user
  ansible.builtin.shell: |
    if ! id appuser > /dev/null 2>&1; then
      useradd -m -s /bin/bash appuser
      usermod -aG docker appuser
    fi
```

### 3. Use Modules, Not Commands

Always prefer built-in modules over `shell`, `command`, or `raw`.

**Module Hierarchy** (prefer top to bottom):
1. **Specific modules**: `apt`, `yum`, `systemd`, `docker_container`
2. **Generic modules**: `package`, `service`
3. **Command modules**: `command` (when no module exists)
4. **Shell modules**: `shell` (only when shell features needed)
5. **Raw modules**: `raw` (only for hosts without Python)

### 4. Keep Playbooks Simple

- One playbook = one purpose
- Use roles for complex logic
- Limit playbook to 100-150 lines
- Extract repeated code to roles/tasks

### 5. Follow DRY Principle

Don't Repeat Yourself - use:
- `include_tasks` / `import_tasks`
- Roles
- `loop` / `with_items`
- Task files
- Variable defaults

---

## Project Structure

### Recommended Layout

```
ansible/
├── ansible.cfg                   # Ansible configuration
├── requirements.txt              # Python dependencies (Ansible, collections)
├── requirements.yml              # Ansible Galaxy dependencies
│
├── inventory/                    # Inventory files
│   ├── production/
│   │   ├── hosts.yml            # Production inventory
│   │   └── group_vars/
│   │       ├── all.yml          # Variables for all hosts
│   │       ├── webservers.yml   # Variables for webserver group
│   │       └── databases.yml
│   ├── staging/
│   │   ├── hosts.yml
│   │   └── group_vars/
│   └── development/
│       ├── hosts.yml
│       └── group_vars/
│
├── group_vars/                   # Shared group variables
│   ├── all/
│   │   ├── vars.yml             # Non-sensitive variables
│   │   └── vault.yml            # Encrypted sensitive variables
│   ├── webservers.yml
│   └── databases.yml
│
├── host_vars/                    # Host-specific variables
│   ├── server01.example.com.yml
│   └── db01.example.com.yml
│
├── playbooks/                    # Playbooks organized by purpose
│   ├── site.yml                 # Master playbook
│   ├── webservers.yml           # Web server setup
│   ├── databases.yml            # Database setup
│   ├── deploy.yml               # Application deployment
│   ├── backup.yml               # Backup operations
│   └── maintenance/             # Maintenance playbooks
│       ├── restart-services.yml
│       ├── cleanup.yml
│       └── health-check.yml
│
├── roles/                        # Custom roles
│   ├── common/                  # Base configuration for all servers
│   │   ├── tasks/
│   │   │   └── main.yml
│   │   ├── handlers/
│   │   │   └── main.yml
│   │   ├── templates/
│   │   ├── files/
│   │   ├── vars/
│   │   │   └── main.yml
│   │   ├── defaults/
│   │   │   └── main.yml
│   │   ├── meta/
│   │   │   └── main.yml
│   │   ├── tests/
│   │   │   ├── inventory
│   │   │   └── test.yml
│   │   └── README.md
│   │
│   ├── nginx/                   # Nginx role
│   ├── docker/                  # Docker role
│   └── monitoring/              # Monitoring role
│
├── collections/                  # Local collections (if any)
│   └── requirements.yml
│
├── plugins/                      # Custom plugins
│   ├── filters/
│   ├── modules/
│   └── inventory/
│
├── scripts/                      # Helper scripts
│   ├── vault-encrypt.sh
│   ├── vault-decrypt.sh
│   └── ansible-lint-all.sh
│
└── docs/                         # Documentation
    ├── PLAYBOOK_GUIDE.md
    ├── ROLE_GUIDE.md
    └── TROUBLESHOOTING.md
```

### File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Playbooks | `verb-noun.yml` | `deploy-app.yml`, `restart-services.yml` |
| Roles | `noun` | `nginx`, `docker`, `postgresql` |
| Variables | `snake_case` | `app_port`, `db_password` |
| Inventory files | `environment/hosts.yml` | `production/hosts.yml` |
| Group vars | `group_name.yml` | `webservers.yml`, `databases.yml` |
| Host vars | `fqdn.yml` | `web01.example.com.yml` |

---

## Inventory Management

### Static Inventory

**INI Format** (simple, legacy):
```ini
[webservers]
web01.example.com ansible_host=192.168.1.10
web02.example.com ansible_host=192.168.1.11

[databases]
db01.example.com ansible_host=192.168.1.20

[webservers:vars]
ansible_user=ubuntu
ansible_python_interpreter=/usr/bin/python3
```

**YAML Format** (recommended, more flexible):
```yaml
all:
  children:
    webservers:
      hosts:
        web01.example.com:
          ansible_host: 192.168.1.10
          http_port: 80
        web02.example.com:
          ansible_host: 192.168.1.11
          http_port: 8080
      vars:
        ansible_user: ubuntu
        ansible_python_interpreter: /usr/bin/python3

    databases:
      hosts:
        db01.example.com:
          ansible_host: 192.168.1.20
      vars:
        ansible_user: postgres
```

### Dynamic Inventory

For cloud providers (AWS, GCP, Azure):

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - us-east-1
  - us-west-2
filters:
  tag:Environment: production
  instance-state-name: running
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.region
    prefix: region
compose:
  ansible_host: public_ip_address
```

**Usage**:
```bash
ansible-playbook -i inventory/aws_ec2.yml playbooks/site.yml
```

### Best Practices

1. **Organize by environment**: Separate production, staging, development
2. **Use group variables**: Avoid repeating vars in inventory
3. **Document inventory**: Add comments explaining non-obvious entries
4. **Test connectivity**: `ansible all -m ping -i inventory/production/hosts.yml`
5. **Use FQDN**: Prefer full domain names over IP addresses
6. **Keep credentials separate**: Use Ansible Vault for sensitive data

---

## Playbook Design

### Basic Structure

```yaml
---
- name: Deploy web application
  hosts: webservers
  become: true
  gather_facts: true

  vars:
    app_version: "1.2.3"
    app_port: 8080

  pre_tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

  roles:
    - common
    - nginx
    - application

  tasks:
    - name: Ensure application is running
      ansible.builtin.service:
        name: myapp
        state: started
        enabled: true

  post_tasks:
    - name: Verify application health
      ansible.builtin.uri:
        url: "http://localhost:{{ app_port }}/health"
        status_code: 200

  handlers:
    - name: restart nginx
      ansible.builtin.service:
        name: nginx
        state: restarted
```

### Task Organization

**Use descriptive names**:
```yaml
✅ Good:
- name: Install nginx web server version 1.18
  ansible.builtin.apt:
    name: nginx=1.18.*
    state: present

❌ Bad:
- name: Install package
  ansible.builtin.apt:
    name: nginx
    state: present
```

**Group related tasks**:
```yaml
- name: Setup PostgreSQL
  block:
    - name: Install PostgreSQL
      ansible.builtin.apt:
        name: postgresql
        state: present

    - name: Start PostgreSQL service
      ansible.builtin.service:
        name: postgresql
        state: started

    - name: Create database
      community.postgresql.postgresql_db:
        name: myapp
        state: present

  rescue:
    - name: Log error
      ansible.builtin.debug:
        msg: "PostgreSQL setup failed, cleaning up..."

    - name: Remove failed installation
      ansible.builtin.apt:
        name: postgresql
        state: absent

  always:
    - name: Cleanup temp files
      ansible.builtin.file:
        path: /tmp/pg_setup
        state: absent
```

### Conditionals

```yaml
# Simple condition
- name: Install Apache on Debian systems
  ansible.builtin.apt:
    name: apache2
    state: present
  when: ansible_os_family == "Debian"

# Multiple conditions (AND)
- name: Install package on Ubuntu 20.04
  ansible.builtin.apt:
    name: mypackage
    state: present
  when:
    - ansible_distribution == "Ubuntu"
    - ansible_distribution_version == "20.04"

# OR conditions
- name: Install web server
  ansible.builtin.package:
    name: "{{ item }}"
    state: present
  when: ansible_os_family == "Debian" or ansible_os_family == "RedHat"
  loop:
    - nginx

# Complex conditions
- name: Configure firewall
  ansible.builtin.firewalld:
    service: https
    permanent: true
    state: enabled
  when:
    - ansible_os_family == "RedHat"
    - ansible_distribution_major_version|int >= 7
    - firewall_enabled | default(true)
```

### Loops

```yaml
# Simple loop
- name: Install multiple packages
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - postgresql
    - redis

# Loop with dictionary
- name: Create multiple users
  ansible.builtin.user:
    name: "{{ item.name }}"
    state: present
    groups: "{{ item.groups }}"
  loop:
    - { name: 'alice', groups: 'admin,docker' }
    - { name: 'bob', groups: 'docker' }
    - { name: 'charlie', groups: 'users' }

# Loop with dict to list
- name: Create directories
  ansible.builtin.file:
    path: "{{ item.value.path }}"
    state: directory
    mode: "{{ item.value.mode }}"
  loop: "{{ directories | dict2items }}"
  vars:
    directories:
      app:
        path: /opt/app
        mode: '0755'
      logs:
        path: /var/log/app
        mode: '0750'

# Loop with until (retry logic)
- name: Wait for service to be ready
  ansible.builtin.uri:
    url: "http://localhost:8080/health"
    status_code: 200
  register: result
  until: result.status == 200
  retries: 10
  delay: 5
```

### Tags

```yaml
- name: Install packages
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - postgresql
  tags:
    - packages
    - install

- name: Configure nginx
  ansible.builtin.template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
  notify: restart nginx
  tags:
    - config
    - nginx

- name: Deploy application
  ansible.builtin.copy:
    src: app.jar
    dest: /opt/app/app.jar
  tags:
    - deploy
    - application
```

**Usage**:
```bash
# Run only tagged tasks
ansible-playbook site.yml --tags "config"

# Skip tagged tasks
ansible-playbook site.yml --skip-tags "deploy"

# Multiple tags
ansible-playbook site.yml --tags "install,config"
```

---

## Role Development

### Role Structure

```
roles/nginx/
├── README.md                 # Role documentation
├── defaults/
│   └── main.yml             # Default variables (lowest precedence)
├── vars/
│   └── main.yml             # Role variables (high precedence)
├── tasks/
│   ├── main.yml             # Main tasks entry point
│   ├── install.yml          # Installation tasks
│   ├── configure.yml        # Configuration tasks
│   └── firewall.yml         # Firewall configuration
├── handlers/
│   └── main.yml             # Handlers for service restarts
├── templates/
│   ├── nginx.conf.j2        # Jinja2 templates
│   └── site.conf.j2
├── files/
│   └── custom-error.html    # Static files
├── meta/
│   └── main.yml             # Role metadata and dependencies
└── tests/
    ├── inventory            # Test inventory
    └── test.yml             # Test playbook
```

### defaults/main.yml

```yaml
---
# Nginx version
nginx_version: "1.18.*"

# Port configuration
nginx_http_port: 80
nginx_https_port: 443

# SSL configuration
nginx_ssl_enabled: false
nginx_ssl_certificate: ""
nginx_ssl_certificate_key: ""

# Worker configuration
nginx_worker_processes: auto
nginx_worker_connections: 1024

# Logging
nginx_access_log: "/var/log/nginx/access.log"
nginx_error_log: "/var/log/nginx/error.log"

# Sites configuration
nginx_sites: []
#  - name: example.com
#    port: 80
#    root: /var/www/example.com
#    index: index.html
```

### tasks/main.yml

```yaml
---
- name: Include OS-specific variables
  ansible.builtin.include_vars: "{{ ansible_os_family }}.yml"

- name: Install nginx
  ansible.builtin.import_tasks: install.yml
  tags:
    - install

- name: Configure nginx
  ansible.builtin.import_tasks: configure.yml
  tags:
    - configure

- name: Setup firewall
  ansible.builtin.import_tasks: firewall.yml
  when: nginx_configure_firewall | default(true)
  tags:
    - firewall

- name: Ensure nginx is running
  ansible.builtin.service:
    name: nginx
    state: started
    enabled: true
```

### tasks/install.yml

```yaml
---
- name: Install nginx (Debian/Ubuntu)
  ansible.builtin.apt:
    name: "nginx={{ nginx_version }}"
    state: present
    update_cache: true
  when: ansible_os_family == "Debian"

- name: Install nginx (RedHat/CentOS)
  ansible.builtin.yum:
    name: nginx
    state: present
  when: ansible_os_family == "RedHat"

- name: Create nginx directories
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  loop:
    - /etc/nginx/sites-available
    - /etc/nginx/sites-enabled
    - /var/www
```

### templates/nginx.conf.j2

```jinja
user www-data;
worker_processes {{ nginx_worker_processes }};
pid /run/nginx.pid;

events {
    worker_connections {{ nginx_worker_connections }};
}

http {
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log {{ nginx_access_log }};
    error_log {{ nginx_error_log }};

    gzip on;

    include /etc/nginx/conf.d/*.conf;
    include /etc/nginx/sites-enabled/*;
}
```

### handlers/main.yml

```yaml
---
- name: restart nginx
  ansible.builtin.service:
    name: nginx
    state: restarted
  when: not ansible_check_mode

- name: reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded
  when: not ansible_check_mode

- name: validate nginx config
  ansible.builtin.command: nginx -t
  changed_when: false
```

### meta/main.yml

```yaml
---
galaxy_info:
  role_name: nginx
  author: Your Name
  description: Install and configure nginx web server
  company: Your Company
  license: MIT
  min_ansible_version: "2.10"

  platforms:
    - name: Ubuntu
      versions:
        - focal
        - jammy
    - name: Debian
      versions:
        - bullseye

  galaxy_tags:
    - web
    - nginx
    - webserver

dependencies: []
```

### README.md (Role Documentation)

````markdown
# Nginx Role

Install and configure nginx web server.

## Requirements

- Ansible 2.10+
- Supported OS: Ubuntu 20.04+, Debian 11+

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `nginx_version` | `1.18.*` | Nginx version to install |
| `nginx_http_port` | `80` | HTTP port |
| `nginx_https_port` | `443` | HTTPS port |
| `nginx_worker_processes` | `auto` | Number of worker processes |

See `defaults/main.yml` for all variables.

## Dependencies

None.

## Example Playbook

```yaml
- hosts: webservers
  roles:
    - role: nginx
      vars:
        nginx_http_port: 8080
        nginx_sites:
          - name: example.com
            port: 8080
            root: /var/www/example
```

## Testing

```bash
molecule test
```

## License

MIT

## Author

Your Name <your.email@example.com>
````

---

## Variable Management

### Variable Precedence

From lowest to highest priority:

1. `role defaults` (defaults/main.yml in role)
2. `inventory file` or `script group vars`
3. `inventory group_vars/all`
4. `playbook group_vars/all`
5. `inventory group_vars/*`
6. `playbook group_vars/*`
7. `inventory file` or `script host vars`
8. `inventory host_vars/*`
9. `playbook host_vars/*`
10. `host facts` / `cached set_facts`
11. `play vars`
12. `play vars_prompt`
13. `play vars_files`
14. `role vars` (vars/main.yml in role)
15. `block vars`
16. `task vars`
17. `include_vars`
18. `set_facts` / `registered vars`
19. `role (and include_role) params`
20. `include params`
21. `extra vars` (CLI `-e` flag) **HIGHEST**

### Variable Naming Conventions

```yaml
# ✅ Good: Descriptive, prefixed by role
nginx_worker_processes: 4
nginx_http_port: 80
app_version: "1.2.3"
db_max_connections: 100

# ❌ Bad: Too generic, conflicts likely
port: 80
version: "1.2.3"
max_connections: 100
```

### Organizing Variables

**group_vars/all/vars.yml** (Non-sensitive):
```yaml
---
# Common variables
ntp_servers:
  - 0.pool.ntp.org
  - 1.pool.ntp.org

timezone: "UTC"

# Package versions
docker_version: "20.10.*"
python_version: "3.10"
```

**group_vars/all/vault.yml** (Sensitive, encrypted):
```yaml
---
# Database credentials
vault_db_password: "super_secret_password"
vault_api_key: "api_key_123456"
vault_ssh_private_key: |
  -----BEGIN RSA PRIVATE KEY-----
  ...
  -----END RSA PRIVATE KEY-----
```

**Using vaulted variables in playbooks**:
```yaml
- name: Configure database
  community.postgresql.postgresql_db:
    name: myapp
    password: "{{ vault_db_password }}"
```

### Variable Files

```yaml
# playbook.yml
---
- name: Deploy application
  hosts: webservers
  vars_files:
    - vars/common.yml
    - vars/{{ ansible_distribution }}.yml
    - vars/{{ env }}.yml
```

---

## Security Best Practices

### 1. Use Ansible Vault

**Encrypt sensitive files**:
```bash
# Create new encrypted file
ansible-vault create group_vars/all/vault.yml

# Encrypt existing file
ansible-vault encrypt group_vars/all/secrets.yml

# Edit encrypted file
ansible-vault edit group_vars/all/vault.yml

# View encrypted file
ansible-vault view group_vars/all/vault.yml
```

**Vault password file**:
```bash
# Create password file (chmod 600)
echo "my_vault_password" > .secrets/.vault_pass
chmod 600 .secrets/.vault_pass

# Configure ansible.cfg
[defaults]
vault_password_file = .secrets/.vault_pass

# Or use environment variable
export ANSIBLE_VAULT_PASSWORD_FILE=.secrets/.vault_pass
```

### 2. Never Commit Secrets

**.gitignore**:
```gitignore
# Secrets
.secrets/
*.vault
*_vault.yml
vault_pass*
*.key
*.pem

# Temporary files
*.retry
*.log
```

### 3. Use Environment-Specific Vaults

```bash
ansible/
├── group_vars/
│   └── all/
│       ├── vault_production.yml
│       ├── vault_staging.yml
│       └── vault_development.yml
```

### 4. Limit Privilege Escalation

```yaml
# ✅ Good: Only escalate when needed
- name: Read log file
  ansible.builtin.command: cat /var/log/app.log
  # No become needed for reading logs

- name: Restart service
  ansible.builtin.service:
    name: nginx
    state: restarted
  become: true  # Only escalate here
```

### 5. Use SSH Keys, Not Passwords

**ansible.cfg**:
```ini
[defaults]
host_key_checking = False  # Only in development!
private_key_file = ~/.ssh/ansible_rsa

[privilege_escalation]
become = False
become_method = sudo
become_user = root
become_ask_pass = False
```

### 6. Validate Input

```yaml
- name: Validate port is numeric
  ansible.builtin.fail:
    msg: "Port must be numeric"
  when: app_port is not number

- name: Ensure required variables are set
  ansible.builtin.assert:
    that:
      - db_host is defined
      - db_password is defined
      - db_password | length > 8
    fail_msg: "Database configuration incomplete or password too short"
```

### 7. Use no_log for Sensitive Output

```yaml
- name: Set database password
  ansible.builtin.user:
    name: dbuser
    password: "{{ db_password | password_hash('sha512') }}"
  no_log: true  # Prevent password from appearing in logs

- name: Debug without exposing secrets
  ansible.builtin.debug:
    msg: "Database configured for host {{ db_host }}"
  # Don't include {{ db_password }} in debug output
```

---

## Testing and Validation

### 1. Syntax Check

```bash
# Check single playbook
ansible-playbook playbooks/site.yml --syntax-check

# Check role
ansible-playbook roles/nginx/tests/test.yml --syntax-check
```

### 2. Ansible Lint

Install:
```bash
pip install ansible-lint
```

Run:
```bash
# Lint all playbooks
ansible-lint playbooks/*.yml

# Lint specific file
ansible-lint playbooks/deploy.yml

# Lint roles
ansible-lint roles/nginx/
```

**Custom .ansible-lint configuration**:
```yaml
# .ansible-lint
skip_list:
  - '204'  # Lines should be no longer than 160 chars
  - '301'  # Commands should not change things if nothing needs doing

warn_list:
  - experimental
  - role-name

exclude_paths:
  - .github/
  - tests/
```

### 3. Dry Run (Check Mode)

```bash
# Run in check mode (no changes made)
ansible-playbook playbooks/site.yml --check

# With diff to see what would change
ansible-playbook playbooks/site.yml --check --diff
```

### 4. Molecule Testing

See [MOLECULE_TESTING_GUIDE.md](MOLECULE_TESTING_GUIDE.md) for comprehensive guide.

Quick example:
```bash
# Initialize molecule
cd roles/nginx
molecule init scenario -d docker

# Run full test suite
molecule test

# Individual steps
molecule create    # Create test instance
molecule converge  # Run playbook
molecule verify    # Run tests
molecule destroy   # Cleanup
```

### 5. Unit Testing with Python

```python
# tests/test_nginx_role.py
import pytest
import testinfra

@pytest.fixture()
def host(host):
    return host

def test_nginx_installed(host):
    nginx = host.package("nginx")
    assert nginx.is_installed

def test_nginx_running(host):
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_nginx_listening(host):
    socket = host.socket("tcp://0.0.0.0:80")
    assert socket.is_listening
```

Run:
```bash
pytest tests/ -v
```

---

## Performance Optimization

### 1. Gather Facts Selectively

```yaml
# Disable facts if not needed
- hosts: all
  gather_facts: false

# Or gather specific facts
- hosts: all
  gather_facts: true
  gather_subset:
    - '!all'
    - network
```

### 2. Use Pipelining

**ansible.cfg**:
```ini
[ssh_connection]
pipelining = True  # Reduces SSH operations
```

### 3. Enable Fact Caching

**ansible.cfg**:
```ini
[defaults]
fact_caching = jsonfile
fact_caching_connection = /tmp/ansible_fact_cache
fact_caching_timeout = 3600
```

### 4. Parallel Execution

```ini
[defaults]
forks = 20  # Increase from default 5
```

### 5. Optimize Loops

```yaml
# ❌ Slow: Individual package installs
- name: Install packages
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  loop:
    - nginx
    - postgresql
    - redis

# ✅ Fast: Install all at once
- name: Install packages
  ansible.builtin.apt:
    name:
      - nginx
      - postgresql
      - redis
    state: present
```

### 6. Use async for long-running tasks

```yaml
- name: Long running deployment
  ansible.builtin.shell: /opt/deploy-app.sh
  async: 300  # Run for up to 5 minutes
  poll: 0     # Don't wait (fire and forget)
  register: deploy_job

- name: Check deployment status
  ansible.builtin.async_status:
    jid: "{{ deploy_job.ansible_job_id }}"
  register: job_result
  until: job_result.finished
  retries: 30
  delay: 10
```

---

## Error Handling

### 1. Failed When Condition

```yaml
- name: Check if application is healthy
  ansible.builtin.uri:
    url: http://localhost:8080/health
  register: health_check
  failed_when:
    - health_check.status != 200
    - "'healthy' not in health_check.json.status"
```

### 2. Ignore Errors

```yaml
- name: Try to stop service (may not exist)
  ansible.builtin.service:
    name: old-app
    state: stopped
  ignore_errors: true

- name: Continue with installation
  ansible.builtin.apt:
    name: new-app
    state: present
```

### 3. Block/Rescue/Always

```yaml
- name: Deploy application with error handling
  block:
    - name: Stop application
      ansible.builtin.service:
        name: myapp
        state: stopped

    - name: Deploy new version
      ansible.builtin.copy:
        src: app-v2.jar
        dest: /opt/app/app.jar

    - name: Start application
      ansible.builtin.service:
        name: myapp
        state: started

  rescue:
    - name: Rollback to previous version
      ansible.builtin.copy:
        src: /opt/app/app.jar.backup
        dest: /opt/app/app.jar

    - name: Restart with old version
      ansible.builtin.service:
        name: myapp
        state: started

    - name: Send alert
      ansible.builtin.mail:
        to: ops@example.com
        subject: "Deployment failed, rolled back"

  always:
    - name: Cleanup temp files
      ansible.builtin.file:
        path: /tmp/deployment
        state: absent
```

### 4. Assertions

```yaml
- name: Verify prerequisites
  ansible.builtin.assert:
    that:
      - ansible_distribution == "Ubuntu"
      - ansible_distribution_major_version|int >= 20
      - ansible_memtotal_mb >= 2048
    fail_msg: "System does not meet minimum requirements"
    success_msg: "Prerequisites validated"
```

---

## Documentation

### Playbook Documentation

```yaml
---
# playbooks/deploy.yml
#
# Purpose: Deploy application to production
# Author: DevOps Team
# Last Updated: 2024-03-20
#
# Requirements:
#   - Ansible 2.10+
#   - Vault password file
#   - SSH access to targets
#
# Usage:
#   ansible-playbook playbooks/deploy.yml -e "app_version=1.2.3"
#
# Variables:
#   app_version: Application version to deploy (required)
#   skip_backup: Skip backup step (optional, default: false)

- name: Deploy Application
  hosts: webservers
  become: true
```

### Role README.md Template

````markdown
# Role Name

One-line description of the role.

## Requirements

- Ansible version
- Operating systems supported
- Dependencies

## Role Variables

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `var_name` | `default_value` | Yes | Description |

## Dependencies

List of role dependencies.

## Example Playbook

```yaml
- hosts: servers
  roles:
    - role: rolename
      vars:
        var_name: value
```

## Testing

How to test this role.

## License

License type.

## Author

Author information.
````

---

## CI/CD Integration

### GitHub Actions

**.github/workflows/ansible-ci.yml**:
```yaml
name: Ansible CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install ansible ansible-lint yamllint

      - name: Run ansible-lint
        run: ansible-lint playbooks/*.yml roles/*/

      - name: Run yamllint
        run: yamllint .

  syntax-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Syntax check playbooks
        run: |
          for playbook in playbooks/*.yml; do
            ansible-playbook "$playbook" --syntax-check
          done

  molecule:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        role: [nginx, docker, common]
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install Molecule
        run: pip install molecule molecule-docker ansible-lint

      - name: Run Molecule tests
        run: |
          cd roles/${{ matrix.role }}
          molecule test
```

### GitLab CI

**.gitlab-ci.yml**:
```yaml
stages:
  - lint
  - test
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip

lint:
  stage: lint
  image: python:3.10
  before_script:
    - pip install ansible ansible-lint yamllint
  script:
    - ansible-lint playbooks/*.yml
    - yamllint .

syntax-check:
  stage: lint
  image: python:3.10
  before_script:
    - pip install ansible
  script:
    - find playbooks -name "*.yml" -exec ansible-playbook {} --syntax-check \;

molecule-test:
  stage: test
  image: python:3.10
  services:
    - docker:dind
  before_script:
    - pip install molecule molecule-docker ansible-lint
  script:
    - cd roles/nginx
    - molecule test

deploy-staging:
  stage: deploy
  image: python:3.10
  only:
    - develop
  before_script:
    - pip install ansible
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
  script:
    - ansible-playbook -i inventory/staging/hosts.yml playbooks/deploy.yml

deploy-production:
  stage: deploy
  image: python:3.10
  only:
    - main
  when: manual
  before_script:
    - pip install ansible
    - mkdir -p ~/.ssh
    - echo "$SSH_PRIVATE_KEY" > ~/.ssh/id_rsa
    - chmod 600 ~/.ssh/id_rsa
  script:
    - ansible-playbook -i inventory/production/hosts.yml playbooks/deploy.yml
```

---

## Summary Checklist

### Before Writing

- [ ] Understand Ansible core principles (idempotency, declarative)
- [ ] Plan project structure
- [ ] Define inventory organization
- [ ] Identify required roles

### Writing Playbooks/Roles

- [ ] Use descriptive names for tasks
- [ ] Prefer modules over shell/command
- [ ] Add tags for selective execution
- [ ] Implement error handling (block/rescue/always)
- [ ] Use variables for configuration
- [ ] Encrypt sensitive data with Vault
- [ ] Add documentation/comments

### Testing

- [ ] Run syntax check
- [ ] Run ansible-lint
- [ ] Test in check mode (--check)
- [ ] Test on non-production environment
- [ ] Implement Molecule tests for roles
- [ ] Add CI/CD pipeline

### Security

- [ ] No hardcoded secrets
- [ ] Use Ansible Vault for sensitive data
- [ ] Vault password file in .gitignore
- [ ] Use no_log for sensitive tasks
- [ ] Minimize privilege escalation
- [ ] Validate input variables

### Documentation

- [ ] README.md for roles
- [ ] Comments in playbooks
- [ ] Document variables
- [ ] Provide usage examples
- [ ] Keep docs updated

---

## Additional Resources

- [Ansible Documentation](https://docs.ansible.com/)
- [Ansible Best Practices (Official)](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)
- [Ansible Lint Rules](https://ansible-lint.readthedocs.io/)
- [Ansible Galaxy](https://galaxy.ansible.com/)
- [Molecule Documentation](https://molecule.readthedocs.io/)
- [YAML Lint](https://yamllint.readthedocs.io/)

---

**Document Version**: 1.0.0
**Last Updated**: 2026-03-20
**Maintained By**: Enterprise Template Team
