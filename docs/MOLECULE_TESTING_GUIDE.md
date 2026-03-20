# Molecule Testing Guide

> comprehensive guide to testing Ansible roles with Molecule framework.

## 📑 Table of Contents

- [What is Molecule](#what-is-molecule)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Testing Workflow](#testing-workflow)
- [Writing Tests](#writing-tests)
- [Drivers](#drivers)
- [Scenarios](#scenarios)
- [CI/CD Integration](#cicd-integration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## What is Molecule

**Molecule** is a testing framework for Ansible roles that helps you:

- **Automate testing**: Run tests automatically on every change
- **Multiple platforms**: Test across different OSes and versions
- **Multiple drivers**: Use Docker, Vagrant, EC2, GCE, etc.
- **Lint integration**: Includes ansible-lint, yamllint
- **Verification**: Test infrastructure with Testinfra or other tools
- **CI/CD ready**: Easily integrate with GitHub Actions, GitLab CI, Jenkins

### Why Use Molecule?

| Without Molecule | With Molecule |
|------------------|---------------|
| Manual VM setup | Automated instance creation |
| Manual role execution | Automated convergence |
| Manual verification | Automated tests |
| Inconsistent testing | Reproducible tests |
| Slow feedback | Fast feedback loop |

---

## Installation

### Requirements

- Python 3.8+
- Docker (for docker driver)
- Ansible 2.10+

### Install Molecule

```bash
# Basic installation
pip install molecule

# With Docker driver (recommended)
pip install molecule molecule-docker

# With Vagrant driver
pip install molecule molecule-vagrant

# With all dependencies
pip install molecule molecule-docker ansible-lint yamllint pytest testinfra
```

### Verify Installation

```bash
molecule --version
# molecule 5.0.0 using python 3.10

molecule drivers
# docker
# podman
```

---

## Quick Start

### 1. Initialize a New Role with Molecule

```bash
# Create role with molecule
molecule init role my_role --driver-name docker

# Or add molecule to existing role
cd roles/existing_role
molecule init scenario --driver-name docker
```

### 2. Directory Structure Created

```
roles/my_role/
├── defaults/
│   └── main.yml
├── files/
├── handlers/
│   └── main.yml
├── meta/
│   └── main.yml
├── molecule/
│   └── default/             # Default scenario
│       ├── molecule.yml     # Molecule configuration
│       ├── converge.yml     # Playbook to test role
│       ├── verify.yml       # Verification playbook (optional)
│       └── prepare.yml      # Preparation playbook (optional)
├── tasks/
│   └── main.yml
├── templates/
├── tests/
│   └── test_default.py     # Testinfra tests
└── vars/
    └── main.yml
```

### 3. Run Tests

```bash
cd roles/my_role

# Run full test sequence
molecule test

# Or step by step
molecule create      # Create test instance
molecule converge    # Run playbook
molecule verify      # Run tests
molecule destroy     # Cleanup
```

---

## Project Structure

### molecule/default/molecule.yml

Main configuration file for Molecule:

```yaml
---
# Dependency manager (galaxy, git, shell)
dependency:
  name: galaxy
  options:
    requirements-file: requirements.yml

# Ansible driver
driver:
  name: docker

# Platforms to test
platforms:
  - name: ubuntu2004
    image: geerlingguy/docker-ubuntu2004-ansible:latest
    pre_build_image: true
    privileged: true
    command: /lib/systemd/systemd
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
    tmpfs:
      - /run
      - /tmp
  
  - name: debian11
    image: geerlingguy/docker-debian11-ansible:latest
    pre_build_image: true
    privileged: true
    command: /lib/systemd/systemd

# Provisioner configuration
provisioner:
  name: ansible
  config_options:
    defaults:
      interpreter_python: auto_silent
      callback_whitelist: profile_tasks, timer, yaml
    ssh_connection:
      pipelining: true
  inventory:
    host_vars:
      ubuntu2004:
        ansible_user: root
      debian11:
        ansible_user: root
  playbooks:
    converge: converge.yml
    verify: verify.yml
    prepare: prepare.yml

# Verifier (testinfra, ansible, goss, etc.)
verifier:
  name: testinfra
  directory: tests/
  options:
    v: 1

# Linters to run
lint: |
  set -e
  yamllint .
  ansible-lint .

# Test sequence
scenario:
  name: default
  test_sequence:
    - dependency
    - lint
    - cleanup
    - destroy
    - syntax
    - create
    - prepare
    - converge
    - idempotence
    - side_effect
    - verify
    - cleanup
    - destroy
```

### molecule/default/converge.yml

Playbook that runs your role:

```yaml
---
- name: Converge
  hosts: all
  become: true
  
  roles:
    - role: my_role
      vars:
        my_role_enable_service: true
        my_role_port: 8080
```

### molecule/default/prepare.yml

Setup prerequisites before running the role:

```yaml
---
- name: Prepare
  hosts: all
  become: true
  
  tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
      when: ansible_os_family == "Debian"
    
    - name: Install dependencies
      ansible.builtin.package:
        name:
          - curl
          - ca-certificates
        state: present
    
    - name: Create test user
      ansible.builtin.user:
        name: testuser
        state: present
```

### molecule/default/verify.yml

Ansible-based verification (alternative to Testinfra):

```yaml
---
- name: Verify
  hosts: all
  become: true
  gather_facts: true
  
  tasks:
    - name: Check if service is running
      ansible.builtin.service:
        name: myapp
        state: started
      check_mode: true
      register: service_status
    
    - name: Verify service is running
      ansible.builtin.assert:
        that:
          - service_status.status.ActiveState == "active"
        fail_msg: "Service is not running"
    
    - name: Check if port is listening
      ansible.builtin.wait_for:
        port: 8080
        timeout: 5
```

### tests/test_default.py

Testinfra verification tests:

```python
"""
Molecule tests for my_role.

These tests verify that the role configures the system correctly.
"""
import os
import pytest
import testinfra.utils.ansible_runner

# Get hosts from Molecule inventory
testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_package_installed(host):
    """Verify that the package is installed."""
    pkg = host.package("myapp")
    assert pkg.is_installed
    assert pkg.version.startswith("1.2")


def test_service_running(host):
    """Verify that the service is running and enabled."""
    svc = host.service("myapp")
    assert svc.is_running
    assert svc.is_enabled


def test_service_listening(host):
    """Verify that the service is listening on the correct port."""
    socket = host.socket("tcp://0.0.0.0:8080")
    assert socket.is_listening


def test_config_file_exists(host):
    """Verify that config file exists with correct permissions."""
    config = host.file("/etc/myapp/config.yml")
    assert config.exists
    assert config.is_file
    assert config.user == "root"
    assert config.group == "root"
    assert config.mode == 0o644


def test_config_file_content(host):
    """Verify config file contains expected values."""
    config = host.file("/etc/myapp/config.yml")
    assert config.contains("port: 8080")
    assert config.contains("enabled: true")


@pytest.mark.parametrize("user", [
    "appuser",
    "admin",
])
def test_users_exist(host, user):
    """Verify that required users exist."""
    u = host.user(user)
    assert u.exists


def test_firewall_rule(host):
    """Verify firewall allows port 8080."""
    # This is OS-specific
    if host.system_info.distribution in ['ubuntu', 'debian']:
        ufw = host.run("ufw status")
        assert "8080/tcp" in ufw.stdout or ufw.rc != 0
```

---

## Configuration

### Platform Configuration

#### Ubuntu  

```yaml
platforms:
  - name: ubuntu2004
    image: geerlingguy/docker-ubuntu2004-ansible:latest
    pre_build_image: true
    privileged: true
    command: /lib/systemd/systemd
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
```

#### CentOS/Rocky Linux

```yaml
platforms:
  - name: centos8
    image: geerlingguy/docker-centos8-ansible:latest
    pre_build_image: true
    privileged: true
    command: /usr/sbin/init
    volumes:
      - /sys/fs/cgroup:/sys/fs/cgroup:ro
```

#### Alpine

```yaml
platforms:
  - name: alpine
    image: alpine:3.17
    pre_build_image: false
    dockerfile: ../Dockerfile.j2
    privileged: false
```

### Multiple Platform Matrix

```yaml
platforms:
  - name: ubuntu2004
    image: geerlingguy/docker-ubuntu2004-ansible:latest
    pre_build_image: true
  
  - name: ubuntu2204
    image: geerlingguy/docker-ubuntu2204-ansible:latest
    pre_build_image: true
  
  - name: debian11
    image: geerlingguy/docker-debian11-ansible:latest
    pre_build_image: true
  
  - name: centos8
    image: geerlingguy/docker-centos8-ansible:latest
    pre_build_image: true
  
  - name: rockylinux8
    image: geerlingguy/docker-rockylinux8-ansible:latest
    pre_build_image: true
```

### Custom Dockerfile

Create `molecule/default/Dockerfile.j2`:

```dockerfile
FROM {{ item.image }}

RUN if [ -f /usr/bin/apt-get ]; then \
        apt-get update && \
        apt-get install -y python3 python3-apt sudo bash ca-certificates && \
        apt-get clean; \
    elif [ -f /usr/bin/dnf ]; then \
        dnf install -y python3 sudo bash && \
        dnf clean all; \
    elif [ -f /usr/bin/yum ]; then \
        yum install -y python3 sudo bash && \
        yum clean all; \
    fi

CMD ["/bin/bash"]
```

Reference in molecule.yml:

```yaml
platforms:
  - name: custom
    image: ubuntu:22.04
    dockerfile: Dockerfile.j2
    pre_build_image: false
```

---

## Testing Workflow

### Complete Test Sequence

```bash
# Full test cycle (recommended)
molecule test
```

**Steps executed**:
1. `dependency` - Install role dependencies
2. `lint` - Run yamllint, ansible-lint
3. `cleanup` - Cleanup leftover instances
4. `destroy` - Destroy existing instances
5. `syntax` - Check playbook syntax
6. `create` - Create test instances
7. `prepare` - Run preparation playbook
8. `converge` - Run role playbook
9. `idempotence` - Run converge again (should have no changes)
10. `side_effect` - Run side effect playbook (if exists)
11. `verify` - Run verification tests
12. `cleanup` - Cleanup test instances
13. `destroy` - Destroy test instances

### Manual Step-by-Step Testing

```bash
# Create instances
molecule create

# Run playbook
molecule converge

# Run tests
molecule verify

# Login to instance for debugging
molecule login

# Check idempotence
molecule idempotence

# Destroy instances
molecule destroy
```

### Development Workflow

```bash
# Keep instance running while developing
molecule create
molecule converge

# Make changes to role
vim tasks/main.yml

# Re-run only convergence
molecule converge

# Verify changes
molecule verify

# Cleanup when done
molecule destroy
```

### Specific Platform Testing

```bash
# Test only Ubuntu
molecule test --platform-name ubuntu2004

# Create multiple platforms but test one
molecule create
molecule converge --platform-name ubuntu2004
molecule verify --platform-name ubuntu2004
```

---

## Writing Tests

### Testinfra Examples

#### File Tests

```python
def test_nginx_config(host):
    """Test nginx configuration."""
    config = host.file("/etc/nginx/nginx.conf")
    
    # File exists
    assert config.exists
    assert config.is_file
    
    # Permissions
    assert config.user == "root"
    assert config.group == "root"
    assert config.mode == 0o644
    
    # Content
    assert config.contains("worker_processes")
    assert not config.contains("error_log /tmp")
    
    # Size
    assert config.size > 100


def test_directory_structure(host):
    """Test directory structure."""
    dirs = [
        "/etc/nginx/sites-available",
        "/etc/nginx/sites-enabled",
        "/var/log/nginx",
    ]
    
    for directory in dirs:
        d = host.file(directory)
        assert d.exists
        assert d.is_directory
        assert d.mode == 0o755
```

#### Package Tests

```python
def test_packages_installed(host):
    """Test required packages are installed."""
    packages = ["nginx", "openssl", "ca-certificates"]
    
    for package in packages:
        pkg = host.package(package)
        assert pkg.is_installed


def test_package_version(host):
    """Test package version."""
    nginx = host.package("nginx")
    assert nginx.is_installed
    assert nginx.version.startswith("1.18")
```

#### Service Tests

```python
def test_nginx_service(host):
    """Test nginx service status."""
    nginx = host.service("nginx")
    
    # Running and enabled
    assert nginx.is_running
    assert nginx.is_enabled
    
    # Systemd specific
    if host.system_info.distribution in ['ubuntu', 'debian']:
        assert nginx.is_masked is False


def test_service_restart(host):
    """Test service can be restarted."""
    # Get PID before restart
    before = host.process.get(comm="nginx")[0]
    
    # Restart service
    host.run("systemctl restart nginx")
    
    # Wait a moment
    import time
    time.sleep(2)
    
    # Get PID after restart
    after = host.process.get(comm="nginx")[0]
    
    # PID should be different
    assert before.pid != after.pid
```

#### Socket Tests

```python
def test_nginx_listening(host):
    """Test nginx is listening on port 80."""
    socket = host.socket("tcp://0.0.0.0:80")
    assert socket.is_listening


def test_multiple_ports(host):
    """Test service listening on multiple ports."""
    ports = [80, 443, 8080]
    
    for port in ports:
        socket = host.socket(f"tcp://0.0.0.0:{port}")
        assert socket.is_listening
```

#### Process Tests

```python
def test_nginx_process(host):
    """Test nginx process is running."""
    processes = host.process.filter(comm="nginx")
    assert len(processes) >= 1
    
    # Master process
    master = [p for p in processes if p.user == "root"]
    assert len(master) == 1


def test_process_count(host):
    """Test correct number of worker processes."""
    workers = host.process.filter(comm="nginx", user="www-data")
    assert len(workers) >= 2  # At least 2 workers
```

#### Command Tests

```python
def test_nginx_version(host):
    """Test nginx version output."""
    cmd = host.run("nginx -v")
    assert cmd.rc == 0
    assert "nginx/1.18" in cmd.stderr


def test_command_output(host):
    """Test command produces expected output."""
    cmd = host.run("curl -s http://localhost/health")
    assert cmd.rc == 0
    assert "healthy" in cmd.stdout
    assert cmd.stdout.strip() == '{"status": "healthy"}'
```

#### User Tests

```python
def test_nginx_user(host):
    """Test nginx user exists."""
    user = host.user("www-data")
    
    assert user.exists
    assert user.shell == "/usr/sbin/nologin"
    assert "www-data" in user.groups
```

#### System Info Tests

```python
def test_os_family(host):
    """Test role only runs on Debian-based systems."""
    assert host.system_info.distribution in ['ubuntu', 'debian']
    assert host.system_info.release >= "20.04"


def test_architecture(host):
    """Test system architecture."""
    assert host.system_info.arch in ['x86_64', 'aarch64']
```

#### Parameterized Tests

```python
@pytest.mark.parametrize("name,port", [
    ("web", 80),
    ("api", 8080),
    ("metrics", 9090),
])
def test_services_listening(host, name, port):
    """Test multiple services are listening."""
    socket = host.socket(f"tcp://0.0.0.0:{port}")
    assert socket.is_listening


@pytest.mark.parametrize("path", [
    "/etc/nginx/nginx.conf",
    "/etc/nginx/sites-available/default",
    "/etc/nginx/conf.d/ssl.conf",
])
def test_config_files(host, path):
    """Test multiple config files exist."""
    f = host.file(path)
    assert f.exists
    assert f.is_file
```

### Ansible Verify Playbook

Alternative to Testinfra - use Ansible assertions:

```yaml
---
- name: Verify nginx installation
  hosts: all
  become: true
  gather_facts: true
  
  tasks:
    - name: Get nginx version
      ansible.builtin.command: nginx -v
      register: nginx_version
      changed_when: false
    
    - name: Verify nginx version
      ansible.builtin.assert:
        that:
          - "'nginx/1.18' in nginx_version.stderr"
        fail_msg: "Wrong nginx version installed"
    
    - name: Check nginx service
      ansible.builtin.service:
        name: nginx
        state: started
      check_mode: true
      register: nginx_service
    
    - name: Verify service is running
      ansible.builtin.assert:
        that:
          - nginx_service.status.ActiveState == "active"
          - nginx_service.status.SubState == "running"
    
    - name: Test HTTP response
      ansible.builtin.uri:
        url: http://localhost/
        status_code: 200
      register: http_response
    
    - name: Verify HTTP response
      ansible.builtin.assert:
        that:
          - http_response.status == 200
          - "'nginx' in http_response.content"
```

---

## Drivers

### Docker Driver (Recommended)

**Advantages**:
- Fast instance creation (<5 seconds)
- No overhead
- Easy to use
- Great for CI/CD

**Limitations**:
- No full systemd support (workarounds exist)
- Limited networking scenarios

**Configuration**:
```yaml
driver:
  name: docker
```

### Podman Driver

Similar to Docker but uses Podman:

```yaml
driver:
  name: podman
```

**Installation**:
```bash
pip install molecule-podman
```

### Vagrant Driver

**Advantages**:
- Full VM experience
- True systemd support
- Multiple providers (VirtualBox, VMware, Libvirt)

**Limitations**:
- Slow instance creation (minutes)
- Resource intensive

**Installation**:
```bash
pip install molecule-vagrant
```

**Configuration**:
```yaml
driver:
  name: vagrant
  provider:
    name: virtualbox

platforms:
  - name: ubuntu
    box: ubuntu/focal64
    memory: 2048
    cpus: 2
```

### Cloud Drivers

#### EC2 Driver

```bash
pip install molecule-ec2
```

```yaml
driver:
  name: ec2

platforms:
  - name: ubuntu
    image: ami-0c55b159cbfafe1f0
    instance_type: t2.micro
    region: us-east-1
    vpc_subnet_id: subnet-xxxxx
```

#### GCE Driver

```bash
pip install molecule-gce
```

```yaml
driver:
  name: gce

platforms:
  - name: ubuntu
    machine_type: n1-standard-1
    image: ubuntu-2004-lts
    zone: us-central1-a
```

---

## Scenarios

### Multiple Scenarios

Test different configurations:

```bash
molecule/
├── default/              # Standard installation
│   └── molecule.yml
├── with-ssl/             # SSL enabled
│   └── molecule.yml
├── cluster/              # Multi-node setup
│   └── molecule.yml
└── upgrade/              # Upgrade scenario
    └── molecule.yml
```

**Create scenario**:
```bash
molecule init scenario with-ssl --driver-name docker
```

**Run specific scenario**:
```bash
molecule test --scenario-name with-ssl
```

### Scenario Examples

#### Default Scenario

Basic role testing:

```yaml
# molecule/default/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance
    image: ubuntu:22.04
provisioner:
  name: ansible
verifier:
  name: testinfra
```

#### SSL Scenario

```yaml
# molecule/with-ssl/molecule.yml
---
dependency:
  name: galaxy
driver:
  name: docker
platforms:
  - name: instance-ssl
    image: ubuntu:22.04
provisioner:
  name: ansible
  inventory:
    host_vars:
      instance-ssl:
        nginx_ssl_enabled: true
        nginx_ssl_cert: /etc/ssl/cert.pem
verifier:
  name: testinfra
```

```yaml
# molecule/with-ssl/converge.yml
---
- name: Converge with SSL
  hosts: all
  become: true
  
  pre_tasks:
    - name: Generate self-signed certificate
      ansible.builtin.command:
        cmd: >
          openssl req -x509 -nodes -days 365 -newkey rsa:2048
          -keyout /etc/ssl/private/nginx.key
          -out /etc/ssl/certs/nginx.crt
          -subj "/CN=localhost"
      args:
        creates: /etc/ssl/certs/nginx.crt
  
  roles:
    - role: nginx
```

#### Cluster Scenario

```yaml
# molecule/cluster/molecule.yml
---
platforms:
  - name: node1
    image: ubuntu:22.04
    groups:
      - cluster
  - name: node2
    image: ubuntu:22.04
    groups:
      - cluster
  - name: node3
    image: ubuntu:22.04
    groups:
      - cluster

provisioner:
  name: ansible
  inventory:
    host_vars:
      node1:
        cluster_role: master
      node2:
        cluster_role: worker
      node3:
        cluster_role: worker
```

---

## CI/CD Integration

### GitHub Actions

```.github/workflows/molecule.yml
name: Molecule CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  molecule:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        scenario:
          - default
          - with-ssl
        platform:
          - ubuntu2004
          - ubuntu2204
          - debian11
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install molecule molecule-docker ansible-lint yamllint pytest testinfra
      
      - name: Run Molecule
        run: |
          molecule test --scenario-name ${{ matrix.scenario }}
        env:
          MOLECULE_PLATFORM: ${{ matrix.platform }}
```

### GitLab CI

```.gitlab-ci.yml
stages:
  - test

molecule:
  stage: test
  image: python:3.10
  services:
    - docker:dind
  variables:
    DOCKER_HOST: tcp://docker:2375
  before_script:
    - pip install molecule molecule-docker ansible-lint yamllint pytest testinfra
  script:
    - molecule test
  parallel:
    matrix:
      - SCENARIO: [default, with-ssl]
        PLATFORM: [ubuntu2004, debian11]
  script:
    - molecule test --scenario-name $SCENARIO
```

---

## Best Practices

### 1. Use Pre-built Images

✅ **Good**:
```yaml
platforms:
  - name: ubuntu
    image: geerlingguy/docker-ubuntu2204-ansible:latest
    pre_build_image: true
```

❌ **Avoid** (slow):
```yaml
platforms:
  - name: ubuntu
    image: ubuntu:22.04
    dockerfile: Dockerfile.j2
    pre_build_image: false  # Builds every time
```

### 2. Test Idempotence

Always include idempotence check:

```yaml
scenario:
  test_sequence:
    - converge
    - idempotence  # Ensures no changes on second run
    - verify
```

### 3. Organize Tests by Component

```python
# tests/test_installation.py
def test_package_installed(host):
    pass

# tests/test_configuration.py
def test_config_files(host):
    pass

# tests/test_service.py
def test_service_running(host):
    pass
```

### 4. Use Fixtures for Common Setup

```python
# tests/conftest.py
import pytest

@pytest.fixture()
def nginx_config(host):
    """Return nginx config file object."""
    return host.file("/etc/nginx/nginx.conf")

# tests/test_config.py
def test_config_exists(nginx_config):
    assert nginx_config.exists
```

### 5. Keep Scenarios Focused

Each scenario should test one specific configuration or feature.

### 6. Document Scenarios

```yaml
# molecule/with-ssl/molecule.yml
---
# SSL-enabled scenario
# Tests nginx with SSL configuration
# Generates self-signed certificates for testing

dependency:
  name: galaxy
# ...
```

### 7. Use Markers for Long Tests

```python
@pytest.mark.slow
def test_long_running_operation(host):
    # ... long test ...
    pass
```

Run:
```bash
# Skip slow tests in CI
pytest -m "not slow"

# Run only slow tests locally
pytest -m slow
```

---

## Troubleshooting

### Common Issues

#### "Cannot connect to Docker daemon"

**Problem**: Docker not running or not accessible

**Solution**:
```bash
# Start Docker
sudo systemctl start docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

#### "Failed to import test module"

**Problem**: Testinfra can't find test files

**Solution**:
```bash
# Install testinfra
pip install testinfra

# Verify verifier configuration in molecule.yml
verifier:
  name: testinfra
  directory: tests/
```

#### "Platform instance already exists"

**Problem**: Previous test run didn't cleanup

**Solution**:
```bash
# Force cleanup
molecule destroy

# Or remove manually
docker rm -f $(docker ps -aq --filter "name=molecule")
```

#### "Idempotence test failed"

**Problem**: Tasks making changes on second run

**Solution**:
- Add `changed_when: false` to command/shell tasks
- Use proper modules instead of shell commands
- Check file templates for dynamic content (timestamps)

Example fix:
```yaml
# ❌ Not idempotent
- name: Install package
  shell: apt-get install -y nginx

# ✅ Idempotent
- name: Install package
  apt:
    name: nginx
    state: present
```

#### "Tests pass locally but fail in CI"

**Causes**:
- Platform differences (architecture, OS version)
- Network access issues
- Timing issues

**Solutions**:
```python
# Add retries for network operations
def test_health_endpoint(host):
    for i in range(5):
        try:
            result = host.run("curl -s http://localhost/health")
            if result.rc == 0:
                break
            time.sleep(2)
        except:
            if i == 4:  # Last retry
                raise
    assert "healthy" in result.stdout
```

---

## Summary

Molecule provides comprehensive testing for Ansible roles:

✅ **Use Molecule when**:
- Developing new roles
- Testing across multiple platforms
- Ensuring idempotence
- Implementing CI/CD for roles
- Working in teams

⚙️ **Key Components**:
1. **molecule.yml** - Configuration
2. **converge.yml** - Role execution
3. **verify.yml** or **tests/** - Verification
4. **prepare.yml** - Setup prerequisites

🔄 **Workflow**:
```bash
# Development
molecule create -> converge -> verify -> destroy

# CI/CD
molecule test  # Full sequence
```

📚 **Further Reading**:
- [Molecule Documentation](https://molecule.readthedocs.io/)
- [Testinfra Documentation](https://testinfra.readthedocs.io/)
- [Jeff Geerling's Molecule Guide](https://www.jeffgeerling.com/blog/testing-your-ansible-roles-molecule)

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-03-20  
**Maintained By**: Enterprise Template Team
