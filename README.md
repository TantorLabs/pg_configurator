# Installation
```bash
apt install -y python3-pip
pip3 install -r requirements.txt
```

# Usage

```bash
git clone https://github.com/O2eg/pg_configurator
cd pg_configurator

# Show help
python3 pg_configurator.py -h

# Minimal usage
python3 pg_configurator.py \
        --db-cpu=40 \
        --db-ram=128Gi \
        --db-disk-type=SSD \
        --db-duty=mixed \
        --pg-version=9.6

# Customized usage
python3 pg_configurator.py \
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