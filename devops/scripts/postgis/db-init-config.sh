#!/bin/bash

set -e
CONF_LOCKFILE_DIR=/var/lib/postgresql/data
SETUP_LOCKFILE="${CONF_LOCKFILE_DIR}/.postgresql.conf.lock"

if [ -f "${SETUP_LOCKFILE}" ]; then
	return 0
fi

# Based on https://docs.timescale.com/self-hosted/latest/configuration/timescaledb-tune/
# Alternatively use https://pgtune.leopard.in.ua
# Adjust as needed before running the DB Setup
cat > "${CONF_LOCKFILE_DIR}"/postgis.conf <<EOF
shared_buffers = 1004320kB
effective_cache_size = 2942MB
maintenance_work_mem = 502160kB
work_mem = 2510kB
max_worker_processes = 27
max_parallel_workers_per_gather = 4
max_parallel_workers = 8
wal_buffers = 16MB
min_wal_size = 512MB
default_statistics_target = 100
random_page_cost = 1.1
checkpoint_completion_target = 0.9
max_connections = 50
max_locks_per_transaction = 64
autovacuum_max_workers = 10
autovacuum_naptime = 10
effective_io_concurrency = 256
EOF


echo "include 'postgis.conf'" >> "/var/lib/postgresql/data/postgresql.conf"

# Put lock file to make sure conf was not reinitialized
touch "${SETUP_LOCKFILE}"