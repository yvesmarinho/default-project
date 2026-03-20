# Ansible Playbook Templates

> Ready-to-use Ansible playbook templates for common infrastructure tasks.

## 📑 Table of Contents

- [Docker Management](#docker-management)
- [Database Operations](#database-operations)
- [Application Deployment](#application-deployment)
- [Backup and Restore](#backup-and-restore)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [Maintenance Operations](#maintenance-operations)
- [Security Operations](#security-operations)
- [Network Configuration](#network-configuration)

---

## Docker Management

### Docker Installation

```yaml
---
- name: Install Docker on Ubuntu/Debian
  hosts: docker_hosts
  become: true
  gather_facts: true
  
  vars:
    docker_version: "5:24.0.*"
    docker_compose_version: "2.21.0"
  
  tasks:
    - name: Install required packages
      ansible.builtin.apt:
        name:
          - apt-transport-https
          - ca-certificates
          - curl
          - gnupg
          - lsb-release
        state: present
        update_cache: true
    
    - name: Create keyrings directory
      ansible.builtin.file:
        path: /etc/apt/keyrings
        state: directory
        mode: '0755'
    
    - name: Add Docker GPG key
      ansible.builtin.get_url:
        url: https://download.docker.com/linux/ubuntu/gpg
        dest: /etc/apt/keyrings/docker.asc
        mode: '0644'
    
    - name: Add Docker repository
      ansible.builtin.apt_repository:
        repo: "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu {{ ansible_distribution_release }} stable"
        state: present
        filename: docker
    
    - name: Install Docker Engine
      ansible.builtin.apt:
        name:
          - "docker-ce={{ docker_version }}"
          - "docker-ce-cli={{ docker_version }}"
          - containerd.io
          - docker-buildx-plugin
          - docker-compose-plugin
        state: present
        update_cache: true
    
    - name: Ensure Docker service is running
      ansible.builtin.service:
        name: docker
        state: started
        enabled: true
    
    - name: Add users to docker group
      ansible.builtin.user:
        name: "{{ item }}"
        groups: docker
        append: true
      loop:
        - ubuntu
        - admin
      when: item in ansible_facts.getent_passwd
    
    - name: Verify Docker installation
      ansible.builtin.command: docker --version
      register: docker_version_output
      changed_when: false
    
    - name: Display Docker version
      ansible.builtin.debug:
        var: docker_version_output.stdout
```

### Docker Compose Deployment

```yaml
---
- name: Deploy Docker Compose Stack
  hosts: docker_hosts
  become: true
  gather_facts: true
  
  vars:
    compose_project_name: "myapp"
    compose_project_dir: "/opt/{{ compose_project_name }}"
    compose_files:
      - docker-compose.yml
      - docker-compose.override.yml
  
  tasks:
    - name: Create project directory
      ansible.builtin.file:
        path: "{{ compose_project_dir }}"
        state: directory
        mode: '0755'
    
    - name: Copy docker-compose files
      ansible.builtin.copy:
        src: "{{ item }}"
        dest: "{{ compose_project_dir }}/{{ item }}"
        mode: '0644'
      loop: "{{ compose_files }}"
      notify: restart docker compose
    
    - name: Copy environment file
      ansible.builtin.template:
        src: .env.j2
        dest: "{{ compose_project_dir }}/.env"
        mode: '0600'
      notify: restart docker compose
      no_log: true
    
    - name: Pull latest images
      community.docker.docker_compose:
        project_src: "{{ compose_project_dir }}"
        pull: true
      register: pull_result
    
    - name: Start Docker Compose stack
      community.docker.docker_compose:
        project_src: "{{ compose_project_dir }}"
        project_name: "{{ compose_project_name }}"
        state: present
      register: compose_result
    
    - name: Wait for services to be healthy
      ansible.builtin.wait_for:
        port: "{{ item.port }}"
        delay: 5
        timeout: 60
      loop:
        - { service: "web", port: 80 }
        - { service: "api", port: 8080 }
      when: item.service in compose_result.services
  
  handlers:
    - name: restart docker compose
      community.docker.docker_compose:
        project_src: "{{ compose_project_dir }}"
        restarted: true
```

### Docker Cleanup

```yaml
---
- name: Docker Cleanup and Optimization
  hosts: docker_hosts
  become: true
  gather_facts: true
  
  vars:
    remove_unused_images: true
    remove_unused_volumes: false  # DANGER: Set to true carefully!
    remove_unused_networks: true
    prune_until: "24h"  # Remove images older than 24h
  
  tasks:
    - name: Get Docker disk usage before cleanup
      ansible.builtin.command: docker system df
      register: disk_before
      changed_when: false
    
    - name: Display disk usage before cleanup
      ansible.builtin.debug:
        var: disk_before.stdout_lines
    
    - name: Stop and remove exited containers
      ansible.builtin.shell: |
        docker ps -aq -f status=exited | xargs -r docker rm
      register: removed_containers
      changed_when: removed_containers.stdout != ""
    
    - name: Remove dangling images
      ansible.builtin.command: docker image prune -f
      when: remove_unused_images
      register: removed_images
      changed_when: "'Total reclaimed space' in removed_images.stdout"
    
    - name: Remove old images
      ansible.builtin.command: "docker image prune -af --filter until={{ prune_until }}"
      when: remove_unused_images
      register: pruned_images
      changed_when: "'Total reclaimed space' in pruned_images.stdout"
    
    - name: Remove unused networks
      ansible.builtin.command: docker network prune -f
      when: remove_unused_networks
      register: removed_networks
      changed_when: "'Total reclaimed space' in removed_networks.stdout"
    
    - name: Remove unused volumes (DANGEROUS!)
      ansible.builtin.command: docker volume prune -f
      when: remove_unused_volumes
      register: removed_volumes
      changed_when: "'Total reclaimed space' in removed_volumes.stdout"
    
    - name: Get Docker disk usage after cleanup
      ansible.builtin.command: docker system df
      register: disk_after
      changed_when: false
    
    - name: Display disk usage after cleanup
      ansible.builtin.debug:
        var: disk_after.stdout_lines
    
    - name: Cleanup summary
      ansible.builtin.debug:
        msg:
          - "Containers removed: {{ removed_containers.stdout_lines | default([]) | length }}"
          - "Images cleaned: {{ 'Yes' if removed_images.changed else 'No' }}"
          - "Networks removed: {{ 'Yes' if removed_networks.changed else 'No' }}"
          - "Volumes removed: {{ 'Yes' if removed_volumes.changed else 'No' }}"
```

### Docker Health Check

```yaml
---
- name: Docker Health Check
  hosts: docker_hosts
  become: true
  gather_facts: true
  
  tasks:
    - name: Check Docker service status
      ansible.builtin.service:
        name: docker
        state: started
      check_mode: true
      register: docker_service
    
    - name: Verify Docker daemon is responsive
      ansible.builtin.command: docker info
      register: docker_info
      changed_when: false
      failed_when: docker_info.rc != 0
    
    - name: Get running containers
      ansible.builtin.command: docker ps --format "{{.Names}}"
      register: running_containers
      changed_when: false
    
    - name: Check container health status
      ansible.builtin.command: "docker inspect --format='{{{{.State.Health.Status}}}}' {{ item }}"
      loop: "{{ running_containers.stdout_lines }}"
      register: container_health
      changed_when: false
      failed_when: false
    
    - name: Report unhealthy containers
      ansible.builtin.debug:
        msg: "Container {{ item.item }} is {{ item.stdout }}"
      loop: "{{ container_health.results }}"
      when: item.stdout != "healthy" and item.stdout != ""
    
    - name: Check Docker disk usage
      ansible.builtin.command: docker system df
      register: disk_usage
      changed_when: false
    
    - name: Display disk usage
      ansible.builtin.debug:
        var: disk_usage.stdout_lines
    
    - name: Get Docker version
      ansible.builtin.command: docker version --format '{{.Server.Version}}'
      register: docker_version
      changed_when: false
    
    - name: Health check summary
      ansible.builtin.debug:
        msg:
          - "Docker service: {{ 'Running' if docker_service.status.ActiveState == 'active' else 'Not running' }}"
          - "Docker version: {{ docker_version.stdout }}"
          - "Running containers: {{ running_containers.stdout_lines | length }}"
          - "Unhealthy containers: {{ container_health.results | selectattr('stdout', 'defined') | selectattr('stdout', '!=', 'healthy') | list | length }}"
```

---

## Database Operations

### PostgreSQL Backup

```yaml
---
- name: Backup PostgreSQL Databases
  hosts: database_servers
  become: true
  become_user: postgres
  gather_facts: true
  
  vars:
    backup_dir: "/opt/backups/postgresql"
    backup_retention_days: 7
    databases:
      - production_db
      - staging_db
      - analytics_db
  
  tasks:
    - name: Create backup directory
      ansible.builtin.file:
        path: "{{ backup_dir }}"
        state: directory
        mode: '0700'
        owner: postgres
        group: postgres
      become_user: root
    
    - name: Generate timestamp
      ansible.builtin.set_fact:
        backup_timestamp: "{{ ansible_date_time.iso8601_basic_short }}"
    
    - name: Backup databases
      community.postgresql.postgresql_db:
        name: "{{ item }}"
        state: dump
        target: "{{ backup_dir }}/{{ item }}_{{ backup_timestamp }}.sql.gz"
        target_opts: "-Fc"
      loop: "{{ databases }}"
      register: backup_result
    
    - name: Verify backup files exist
      ansible.builtin.stat:
        path: "{{ backup_dir }}/{{ item }}_{{ backup_timestamp }}.sql.gz"
      loop: "{{ databases }}"
      register: backup_files
    
    - name: Report backup sizes
      ansible.builtin.debug:
        msg: "{{ item.item }}: {{ (item.stat.size / 1024 / 1024) | round(2) }} MB"
      loop: "{{ backup_files.results }}"
      when: item.stat.exists
    
    - name: Find old backups
      ansible.builtin.find:
        paths: "{{ backup_dir }}"
        age: "{{ backup_retention_days }}d"
        patterns: "*.sql.gz"
      register: old_backups
    
    - name: Remove old backups
      ansible.builtin.file:
        path: "{{ item.path }}"
        state: absent
      loop: "{{ old_backups.files }}"
      when: old_backups.matched > 0
    
    - name: Backup summary
      ansible.builtin.debug:
        msg:
          - "Databases backed up: {{ databases | length }}"
          - "Backup location: {{ backup_dir }}"
          - "Old backups removed: {{ old_backups.matched }}"
```

### PostgreSQL Restore

```yaml
---
- name: Restore PostgreSQL Database
  hosts: database_servers
  become: true
  become_user: postgres
  gather_facts: true
  
  vars:
    backup_file: "/opt/backups/postgresql/production_db_20240320.sql.gz"
    target_database: "production_db"
    drop_existing: false  # DANGER: Set to true to drop existing database
  
  tasks:
    - name: Verify backup file exists
      ansible.builtin.stat:
        path: "{{ backup_file }}"
      register: backup_stat
      failed_when: not backup_stat.stat.exists
    
    - name: Stop application connections
      community.postgresql.postgresql_query:
        db: postgres
        query: |
          SELECT pg_terminate_backend(pid)
          FROM pg_stat_activity
          WHERE datname = '{{ target_database }}'
            AND pid <> pg_backend_pid();
      when: drop_existing
    
    - name: Drop existing database
      community.postgresql.postgresql_db:
        name: "{{ target_database }}"
        state: absent
      when: drop_existing
    
    - name: Create database
      community.postgresql.postgresql_db:
        name: "{{ target_database }}"
        state: present
    
    - name: Restore database from backup
      community.postgresql.postgresql_db:
        name: "{{ target_database }}"
        state: restore
        target: "{{ backup_file }}"
      register: restore_result
    
    - name: Verify database exists
      community.postgresql.postgresql_query:
        db: "{{ target_database }}"
        query: "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
      register: table_count
    
    - name: Restore summary
      ansible.builtin.debug:
        msg:
          - "Database: {{ target_database }}"
          - "Backup file: {{ backup_file }}"
          - "File size: {{ (backup_stat.stat.size / 1024 / 1024) | round(2) }} MB"
          - "Tables restored: {{ table_count.query_result[0].count }}"
```

### MySQL Database Management

```yaml
---
- name: MySQL Database Management
  hosts: mysql_servers
  become: true
  gather_facts: true
  
  vars:
    mysql_root_password: "{{ vault_mysql_root_password }}"
    databases:
      - name: app_production
        encoding: utf8mb4
        collation: utf8mb4_unicode_ci
      - name: app_staging
        encoding: utf8mb4
        collation: utf8mb4_unicode_ci
    users:
      - name: app_user
        password: "{{ vault_app_db_password }}"
        priv: "app_production.*:ALL/app_staging.*:ALL"
        host: "10.0.%.%"
  
  tasks:
    - name: Install MySQL packages
      ansible.builtin.apt:
        name:
          - mysql-server
          - python3-pymysql
        state: present
        update_cache: true
    
    - name: Ensure MySQL is running
      ansible.builtin.service:
        name: mysql
        state: started
        enabled: true
    
    - name: Create databases
      community.mysql.mysql_db:
        name: "{{ item.name }}"
        encoding: "{{ item.encoding }}"
        collation: "{{ item.collation }}"
        login_unix_socket: /var/run/mysqld/mysqld.sock
        state: present
      loop: "{{ databases }}"
      no_log: true
    
    - name: Create database users
      community.mysql.mysql_user:
        name: "{{ item.name }}"
        password: "{{ item.password }}"
        priv: "{{ item.priv }}"
        host: "{{ item.host }}"
        login_unix_socket: /var/run/mysqld/mysqld.sock
        state: present
      loop: "{{ users }}"
      no_log: true
    
    - name: Configure MySQL tuning
      ansible.builtin.lineinfile:
        path: /etc/mysql/mysql.conf.d/mysqld.cnf
        regexp: "{{ item.regexp }}"
        line: "{{ item.line }}"
        state: present
      loop:
        - { regexp: '^max_connections', line: 'max_connections = 200' }
        - { regexp: '^innodb_buffer_pool_size', line: 'innodb_buffer_pool_size = 1G' }
        - { regexp: '^innodb_log_file_size', line: 'innodb_log_file_size = 256M' }
      notify: restart mysql
  
  handlers:
    - name: restart mysql
      ansible.builtin.service:
        name: mysql
        state: restarted
```

---

## Application Deployment

### Zero-Downtime Deployment

```yaml
---
- name: Zero-Downtime Application Deployment
  hosts: app_servers
  become: true
  serial: 1  # Deploy one server at a time
  gather_facts: true
  
  vars:
    app_name: "myapp"
    app_version: "{{ deployment_version | default('latest') }}"
    app_path: "/opt/{{ app_name }}"
    health_check_url: "http://localhost:8080/health"
    health_check_retries: 10
    health_check_delay: 5
  
  tasks:
    - name: Remove server from load balancer
      ansible.builtin.uri:
        url: "http://loadbalancer:9000/api/servers/{{ inventory_hostname }}/disable"
        method: POST
        status_code: 200
      delegate_to: localhost
      register: lb_remove
    
    - name: Wait for active connections to drain
      ansible.builtin.pause:
        seconds: 30
    
    - name: Stop application
      ansible.builtin.systemd:
        name: "{{ app_name }}"
        state: stopped
    
    - name: Backup current version
      ansible.builtin.copy:
        src: "{{ app_path }}/{{ app_name }}.jar"
        dest: "{{ app_path }}/{{ app_name }}.jar.backup"
        remote_src: true
      ignore_errors: true
    
    - name: Deploy new version
      ansible.builtin.get_url:
        url: "https://artifacts.company.com/{{ app_name }}/{{ app_version }}/{{ app_name }}.jar"
        dest: "{{ app_path }}/{{ app_name }}.jar"
        mode: '0644'
        timeout: 300
    
    - name: Start application
      ansible.builtin.systemd:
        name: "{{ app_name }}"
        state: started
    
    - name: Wait for application to be healthy
      ansible.builtin.uri:
        url: "{{ health_check_url }}"
        status_code: 200
      register: health_check
      until: health_check.status == 200
      retries: "{{ health_check_retries }}"
      delay: "{{ health_check_delay }}"
    
    - name: Add server back to load balancer
      ansible.builtin.uri:
        url: "http://loadbalancer:9000/api/servers/{{ inventory_hostname }}/enable"
        method: POST
        status_code: 200
      delegate_to: localhost
    
    - name: Verify deployment
      ansible.builtin.uri:
        url: "{{ health_check_url }}"
        return_content: true
      register: version_check
    
    - name: Display deployed version
      ansible.builtin.debug:
        msg: "Deployed version: {{ version_check.json.version }}"
  
  rescue:
    - name: Rollback to previous version
      ansible.builtin.copy:
        src: "{{ app_path }}/{{ app_name }}.jar.backup"
        dest: "{{ app_path }}/{{ app_name }}.jar"
        remote_src: true
    
    - name: Restart with previous version
      ansible.builtin.systemd:
        name: "{{ app_name }}"
        state: restarted
    
    - name: Fail deployment
      ansible.builtin.fail:
        msg: "Deployment failed, rolled back to previous version"
```

### Blue-Green Deployment

```yaml
---
- name: Blue-Green Deployment
  hosts: app_servers
  become: true
  gather_facts: true
  
  vars:
    app_name: "myapp"
    current_color: "{{ deployment_current_color }}"  # 'blue' or 'green'
    new_color: "{{ 'green' if current_color == 'blue' else 'blue' }}"
    app_version: "{{ deployment_version }}"
  
  tasks:
    - name: Deploy to inactive environment
      block:
        - name: Stop {{ new_color }} environment
          community.docker.docker_compose:
            project_src: "/opt/{{ app_name }}/{{ new_color }}"
            state: absent
        
        - name: Update {{ new_color }} environment files
          ansible.builtin.template:
            src: "docker-compose.{{ new_color }}.yml.j2"
            dest: "/opt/{{ app_name }}/{{ new_color }}/docker-compose.yml"
          vars:
            deploy_version: "{{ app_version }}"
        
        - name: Start {{ new_color }} environment
          community.docker.docker_compose:
            project_src: "/opt/{{ app_name }}/{{ new_color }}"
            pull: true
            state: present
        
        - name: Health check {{ new_color }} environment
          ansible.builtin.uri:
            url: "http://localhost:8{{ '0' if new_color == 'blue' else '1' }}80/health"
            status_code: 200
          register: health_check
          until: health_check.status == 200
          retries: 10
          delay: 5
        
        - name: Run smoke tests on {{ new_color }}
          ansible.builtin.command: "pytest /opt/{{ app_name }}/tests/smoke/"
          environment:
            APP_URL: "http://localhost:8{{ '0' if new_color == 'blue' else '1' }}80"
          register: smoke_tests
        
        - name: Switch load balancer to {{ new_color }}
          ansible.builtin.template:
            src: nginx-upstream.j2
            dest: /etc/nginx/conf.d/upstream.conf
          vars:
            active_color: "{{ new_color }}"
          notify: reload nginx
        
        - name: Wait for traffic to switch
          ansible.builtin.pause:
            seconds: 10
        
        - name: Stop {{ current_color }} environment
          community.docker.docker_compose:
            project_src: "/opt/{{ app_name }}/{{ current_color }}"
            state: stopped
        
        - name: Update deployment state
          ansible.builtin.copy:
            content: "{{ new_color }}"
            dest: /opt/{{ app_name }}/current_deployment
      
      rescue:
        - name: Rollback to {{ current_color }}
          ansible.builtin.template:
            src: nginx-upstream.j2
            dest: /etc/nginx/conf.d/upstream.conf
          vars:
            active_color: "{{ current_color }}"
          notify: reload nginx
        
        - name: Fail deployment
          ansible.builtin.fail:
            msg: "Blue-green deployment failed, rolled back to {{ current_color }}"
  
  handlers:
    - name: reload nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

---

## Backup and Restore

### Comprehensive System Backup

```yaml
---
- name: Comprehensive System Backup
  hosts: all
  become: true
  gather_facts: true
  
  vars:
    backup_root: "/mnt/backups"
    backup_timestamp: "{{ ansible_date_time.iso8601_basic_short }}"
    backup_paths:
      - /etc
      - /opt
      - /var/www
      - /home
    exclude_patterns:
      - "*.log"
      - "*.cache"
      - "*/node_modules/*"
      - "*/venv/*"
      - "*/__pycache__/*"
  
  tasks:
    - name: Create backup directory
      ansible.builtin.file:
        path: "{{ backup_root }}/{{ ansible_hostname }}/{{ backup_timestamp }}"
        state: directory
        mode: '0750'
    
    - name: Backup filesystem
      ansible.builtin.archive:
        path: "{{ backup_paths }}"
        dest: "{{ backup_root }}/{{ ansible_hostname }}/{{ backup_timestamp }}/filesystem.tar.gz"
        exclude_path: "{{ exclude_patterns }}"
        format: gz
      register: filesystem_backup
    
    - name: Backup package list (Debian/Ubuntu)
      ansible.builtin.shell: dpkg --get-selections > packages.list
      args:
        chdir: "{{ backup_root }}/{{ ansible_hostname }}/{{ backup_timestamp }}"
      when: ansible_os_family == "Debian"
    
    - name: Backup crontabs
      ansible.builtin.shell: |
        for user in $(cut -f1 -d: /etc/passwd); do
          crontab -u $user -l > crontab-$user 2>/dev/null || true
        done
      args:
        chdir: "{{ backup_root }}/{{ ansible_hostname }}/{{ backup_timestamp }}"
    
    - name: Backup systemd services
      ansible.builtin.copy:
        src: /etc/systemd/system/
        dest: "{{ backup_root }}/{{ ansible_hostname }}/{{ backup_timestamp }}/systemd/"
        remote_src: true
    
    - name: Generate backup manifest
      ansible.builtin.copy:
        content: |
          Backup Manifest
          ===============
          
          Hostname: {{ ansible_hostname }}
          IP Address: {{ ansible_default_ipv4.address }}
          OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          Backup Date: {{ ansible_date_time.iso8601 }}
          
          Backup Size: {{ (filesystem_backup.archived | default([]) | length) }}
          
          Paths Backed Up:
          {{ backup_paths | to_nice_yaml }}
        dest: "{{ backup_root }}/{{ ansible_hostname }}/{{ backup_timestamp }}/manifest.txt"
    
    - name: Backup summary
      ansible.builtin.debug:
        msg:
          - "Backup completed: {{ backup_root }}/{{ ansible_hostname }}/{{ backup_timestamp }}"
          - "Filesystem backup size: {{ (filesystem_backup.size / 1024 / 1024) | round(2) }} MB"
```

---

## Monitoring and Health Checks

### Comprehensive Health Check

```yaml
---
- name: System Health Check
  hosts: all
  become: true
  gather_facts: true
  
  vars:
    disk_warning_threshold: 80
    disk_critical_threshold: 90
    memory_warning_threshold: 80
    cpu_warning_threshold: 70
    required_services:
      - docker
      - nginx
      - postgresql
  
  tasks:
    - name: Check disk usage
      ansible.builtin.shell: df -h / | awk 'NR==2 {print $5}' | sed 's/%//'
      register: disk_usage
      changed_when: false
    
    - name: Check memory usage
      ansible.builtin.shell: free | awk '/Mem:/ {printf "%.0f", $3/$2 * 100}'
      register: memory_usage
      changed_when: false
    
    - name: Check CPU load
      ansible.builtin.shell: uptime | awk '{print $(NF-2)}' | sed 's/,//'
      register: cpu_load
      changed_when: false
    
    - name: Check required services
      ansible.builtin.service:
        name: "{{ item }}"
        state: started
      check_mode: true
      loop: "{{ required_services }}"
      register: service_check
      ignore_errors: true
    
    - name: Check Docker containers
      ansible.builtin.command: docker ps --format "{{.Names}}\t{{.Status}}"
      register: docker_containers
      changed_when: false
      when: "'docker' in required_services"
    
    - name: Identify unhealthy containers
      ansible.builtin.shell: |
        docker ps --format '{{.Names}}' | while read container; do
          health=$(docker inspect --format='{{.State.Health.Status}}' $container 2>/dev/null || echo "no-healthcheck")
          if [ "$health" = "unhealthy" ]; then
            echo "$container"
          fi
        done
      register: unhealthy_containers
      changed_when: false
      when: "'docker' in required_services"
    
    - name: Check network connectivity
      ansible.builtin.uri:
        url: "{{ item }}"
        timeout: 5
      loop:
        - https://google.com
        - https://github.com
      register: network_check
      ignore_errors: true
    
    - name: Check SSL certificates expiry
      ansible.builtin.shell: |
        echo | openssl s_client -connect {{ ansible_fqdn }}:443 2>/dev/null | \
        openssl x509 -noout -enddate | cut -d= -f2
      register: ssl_expiry
      ignore_errors: true
      when: "'nginx' in required_services"
    
    - name: Generate health report
      ansible.builtin.set_fact:
        health_report:
          hostname: "{{ ansible_hostname }}"
          timestamp: "{{ ansible_date_time.iso8601 }}"
          disk_usage: "{{ disk_usage.stdout }}%"
          memory_usage: "{{ memory_usage.stdout }}%"
          cpu_load: "{{ cpu_load.stdout }}"
          services:
            running: "{{ service_check.results | selectattr('status.ActiveState', 'equalto', 'active') | list | length }}"
            total: "{{ required_services | length }}"
          docker:
            containers: "{{ docker_containers.stdout_lines | default([]) | length }}"
            unhealthy: "{{ unhealthy_containers.stdout_lines | default([]) }}"
          network: "{{ 'OK' if network_check.results | selectattr('status', 'equalto', 200) | list | length == 2 else 'DEGRADED' }}"
    
    - name: Display health report
      ansible.builtin.debug:
        var: health_report
    
    - name: Alert on critical disk usage
      ansible.builtin.fail:
        msg: "CRITICAL: Disk usage is {{ disk_usage.stdout }}%"
      when: disk_usage.stdout | int >= disk_critical_threshold
    
    - name: Warn on high disk usage
      ansible.builtin.debug:
        msg: "WARNING: Disk usage is {{ disk_usage.stdout }}%"
      when: disk_usage.stdout | int >= disk_warning_threshold
```

---

## Maintenance Operations

### System Update and Reboot

```yaml
---
- name: System Update and Reboot
  hosts: all
  become: true
  serial: "25%"  # Update 25% of hosts at a time
  gather_facts: true
  
  vars:
    reboot_required: false
    update_cache_valid_time: 3600
  
  tasks:
    - name: Update apt cache (Debian/Ubuntu)
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: "{{ update_cache_valid_time }}"
      when: ansible_os_family == "Debian"
    
    - name: Upgrade all packages
      ansible.builtin.apt:
        upgrade: dist
        autoremove: true
        autoclean: true
      when: ansible_os_family == "Debian"
      register: upgrade_result
    
    - name: Check if reboot required
      ansible.builtin.stat:
        path: /var/run/reboot-required
      register: reboot_required_file
      when: ansible_os_family == "Debian"
    
    - name: Set reboot fact
      ansible.builtin.set_fact:
        reboot_required: "{{ reboot_required_file.stat.exists }}"
      when: ansible_os_family == "Debian"
    
    - name: Reboot if required
      block:
        - name: Remove from load balancer
          ansible.builtin.uri:
            url: "http://loadbalancer:9000/api/servers/{{ inventory_hostname }}/disable"
            method: POST
          delegate_to: localhost
          ignore_errors: true
        
        - name: Wait for connections to drain
          ansible.builtin.pause:
            seconds: 30
        
        - name: Reboot server
          ansible.builtin.reboot:
            reboot_timeout: 600
            post_reboot_delay: 30
        
        - name: Wait for server to be back online
          ansible.builtin.wait_for_connection:
            timeout: 300
        
        - name: Verify services after reboot
          ansible.builtin.systemd:
            name: "{{ item }}"
            state: started
          loop:
            - docker
            - nginx
        
        - name: Add back to load balancer
          ansible.builtin.uri:
            url: "http://loadbalancer:9000/api/servers/{{ inventory_hostname }}/enable"
            method: POST
          delegate_to: localhost
          ignore_errors: true
      
      when: reboot_required
    
    - name: Update summary
      ansible.builtin.debug:
        msg:
          - "Packages upgraded: {{ upgrade_result.changed }}"
          - "Reboot required: {{ reboot_required }}"
          - "Kernel version: {{ ansible_kernel }}"
```

---

## Security Operations

### Security Hardening

```yaml
---
- name: Security Hardening
  hosts: all
  become: true
  gather_facts: true
  
  tasks:
    - name: Update all packages
      ansible.builtin.apt:
        upgrade: dist
        update_cache: true
      when: ansible_os_family == "Debian"
    
    - name: Install security packages
      ansible.builtin.apt:
        name:
          - fail2ban
          - ufw
          - unattended-upgrades
          - apt-listchanges
        state: present
    
    - name: Configure automatic security updates
      ansible.builtin.copy:
        dest: /etc/apt/apt.conf.d/50unattended-upgrades
        content: |
          Unattended-Upgrade::Allowed-Origins {
              "${distro_id}:${distro_codename}-security";
          };
          Unattended-Upgrade::Automatic-Reboot "false";
        mode: '0644'
    
    - name: Configure UFW defaults
      community.general.ufw:
        direction: "{{ item.direction }}"
        policy: "{{ item.policy }}"
      loop:
        - { direction: 'incoming', policy: 'deny' }
        - { direction: 'outgoing', policy: 'allow' }
    
    - name: Allow SSH
      community.general.ufw:
        rule: limit
        port: '22'
        proto: tcp
    
    - name: Allow HTTP/HTTPS
      community.general.ufw:
        rule: allow
        port: "{{ item }}"
        proto: tcp
      loop:
        - '80'
        - '443'
    
    - name: Enable UFW
      community.general.ufw:
        state: enabled
    
    - name: Configure fail2ban for SSH
      ansible.builtin.copy:
        dest: /etc/fail2ban/jail.local
        content: |
          [sshd]
          enabled = true
          port = 22
          filter = sshd
          logpath = /var/log/auth.log
          maxretry = 3
          bantime = 3600
        mode: '0644'
      notify: restart fail2ban
    
    - name: Disable root SSH login
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^PermitRootLogin'
        line: 'PermitRootLogin no'
        state: present
      notify: restart sshd
    
    - name: Disable password authentication
      ansible.builtin.lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^PasswordAuthentication'
        line: 'PasswordAuthentication no'
        state: present
      notify: restart sshd
    
    - name: Set file permissions on sensitive files
      ansible.builtin.file:
        path: "{{ item }}"
        mode: '0600'
      loop:
        - /etc/ssh/sshd_config
        - /etc/sudoers
    
    - name: Remove unused packages
      ansible.builtin.apt:
       autoremove: true
        purge: true
  
  handlers:
    - name: restart sshd
      ansible.builtin.service:
        name: sshd
        state: restarted
    
    - name: restart fail2ban
      ansible.builtin.service:
        name: fail2ban
        state: restarted
```

---

## Summary

These playbook templates provide:

- ✅ **Production-ready patterns**
- ✅ **Error handling and rollback**
- ✅ **Security best practices**
- ✅ **Detailed logging and reporting**
- ✅ **Zero-downtime deployment strategies**

### Usage

1. Copy the relevant playbook template
2. Adjust variables for your environment
3. Test in development first
4. Run with `--check` before applying
5. Always have a rollback plan

### Customization Tips

- Replace hardcoded values with variables
- Add environment-specific variable files
- Implement proper secret management with Ansible Vault
- Add notification handlers (email, Slack, PagerDuty)
- Include pre and post-task hooks for custom logic

---

**Document Version**: 1.0.0  
**Last Updated**: 2026-03-20  
**Maintained By**: Enterprise Template Team
