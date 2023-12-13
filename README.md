# Preparing Development Environment
Use the following instructions to quickly bring up a simple development environment on Debian-based distributions:
```bash
apt-get -y install git python3-setuptools python3-venv
git clone https://github.com/TantorLabs/pg_configurator.git && cd pg_configurator
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

For testing it is necessary to additionally install Docker
```bash
apt-get update
apt-get -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
apt-get update
apt-get -y install docker-ce docker-ce-cli containerd.io
systemctl start docker
```

and PostgreSQL client package
```bash
apt-get -y remove postgresql\*
install -d /usr/share/postgresql-common/pgdg
curl -fo /usr/share/postgresql-common/pgdg/apt.postgresql.org.asc https://www.postgresql.org/media/keys/ACCC4CF8.asc
echo "deb [signed-by=/usr/share/postgresql-common/pgdg/apt.postgresql.org.asc] https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
apt-get update
apt-get -y install postgresql-client-15
```

# Packaging the Project
To create a source distribution run:
```bash
python3 setup.py sdist
```
This will generate an archive in the *dist* directory, so you can then upload it to a private PyPI repository if you need.

# Installing the Package
Use `pip` utility to install the package:
```bash
pip3 install dist/pg_configurator-22.10.17.tar.gz
```

# Usage
`pip` with create an entrypoint script during the installation, so you should be able to start by simply issuing `pg_configurtor` command from your shell:
```bash
# Show help
pg_configurator -h

# Minimal usage
pg_configurator \
        --db-cpu=40 \
        --db-ram=128Gi \
        --db-disk-type=SSD \
        --db-duty=mixed \
        --pg-version=9.6

# Customized usage
pg_configurator \
        --db-cpu=40 \
        --db-ram=128Gi \
        --db-disk-type=SSD \
        --db-duty=mixed \
        --replication-enabled=True \
        --pg-version=9.6 \
        --min-conns=200 \
        --max-conns=500 \
        --shared-buffers-part=0.3 \
        --client-mem-part=0.6 \
        --maintenance-mem-part=0.1
```
