alg_set_1c = {
    "9.6": [
        {
            "name": "shared_preload_libraries",
            "const": "'pg_stat_statements,pg_store_plans,auto_explain,plantuner,online_analyze'",
            "to_unit": "as_is"
        },
        {
            "name": "autovacuum_naptime",
            "const": "20s"
        },
        {
            "name": "autovacuum_vacuum_cost_delay",
            "const": "2ms"
        },
        {
            "name": "auto_explain.log_min_duration",
            "const": "5s"
        },
        {
            "name": "from_collapse_limit",
            "const": "20"
        },
        {
            "name": "join_collapse_limit",
            "const": "20"
        },
        # ----------------------------------------------------------------------------------
        # Version and platform compatibility
        # ----------------------------------------------------------------------------------
        {
            "name": "escape_string_warning",
            "const": "off"			
        },
        {
            "name": "standard_conforming_strings",
            "const": "off"
        },
        # ----------------------------------------------------------------------------------
        # Resource Consumption
        {
            "name": "max_connections",
            "alg": "1000"
        },
        {
            "name": "max_files_per_process",
            "alg": "int(calc_cpu_scale(2000, 30000))",
            "to_unit": "as_is"
        },
        {
            "name": "temp_buffers",
            "alg":  "max(((total_ram_in_bytes * client_mem_part) / max_connections) * 0.5, 1024 * 1000)"
            # where: if 1C then temp_buffers per session 50% of work_mem
        },
        # ----------------------------------------------------------------------------------
        # Write Ahead Log
        {
            "name": "wal_level",
            "const": "replica"
        },
        {
            "name": "full_page_writes",
			"const": "on"
        },
        # ----------------------------------------------------------------------------------
        # Replication
        # Primary
        {
            "name": "max_wal_senders",
            "alg": """\
                2 if replication_enabled else \
                0""",
            "to_unit": "as_is"
        },
        # ----------------------------------------------------------------------------------
        # Checkpointer
        {
            "name": "checkpoint_timeout",
            "const": "15min"
        },
        {
            "name": "commit_delay",  # microseconds
            "alg": "int(calc_system_scores_scale(500, 3000))",
            "to_unit": "as_is"
        },
        # ----------------------------------------------------------------------------------
        # Background Writer
        {
            "name": "bgwriter_lru_multiplier",                      # some cushion against spikes in demand
            "const": "4"
        },
        # ----------------------------------------------------------------------------------
        # Query Planning
        {
            "name": "cpu_operator_cost",
            "const": "0.001"
        },
        {
            "name": "default_statistics_target",
            "const": "100"
        },
        # ----------------------------------------------------------------------------------
        # Asynchronous Behavior
        {
            "name": "max_parallel_workers_per_gather",
            "const": "0"			
        },
		
        # The online_analyze module provides a set of features that immediately
        # update statistics after INSERT, UPDATE, DELETE, or SELECT INTO operations for the affected tables.
        {
            "name": "online_analyze.enable",
            "const": "off"
        },
        {
            "name": "online_analyze.verbose",
            "const": "off"
        },
        {
            "name": "online_analyze.scale_factor",
            "const": "0.1"
        },
        {
            "name": "online_analyze.threshold",
            "const": "500"
        },
        {
            "name": "online_analyze.local_tracking",
            "const": "on"
        },
        {
            "name": "online_analyze.min_interval",
            "const": "10000"
        },
        {
            "name": "online_analyze.table_type",
            "const": "temporary"
        },
        # Store execution plans like pg_stat_statements does for queries.
        {
            "name": "pg_store_plans.max",
            "const": "15000",
        },
        {
            "name": "pg_store_plans.track",
            "const": "top"
        },
        {
            "name": "pg_store_plans.max_plan_length",
            "const": "15000",
        },
        {
            "name": "pg_store_plans.plan_format",
            "const": "raw"
        },
        {
            "name": "pg_store_plans.min_duration",
            "const": "3000",
        },
        {
            "name": "pg_store_plans.log_analyze",
            "const": "on"
        },
        {
            "name": "pg_store_plans.log_buffers",
            "const": "on"
        },
        # plantuner is a contribution module for PostgreSQL, which enable planner hints.
        {
            "name": "plantuner.fix_empty_table",
            "const": "on"
        },
        # ----------------------------------------------------------------------------------
        # Connection and authentication
        # ----------------------------------------------------------------------------------
        {
            "name": "row_security",
            "const": "off"
        },
        {
            "name": "ssl",
            "const":  "off"  
        }
    ],
    "10": [
        {
            "__parent": "9.6"
        },
        {
            "name": "max_parallel_workers",
            "alg": "calc_cpu_scale(4, 24)"
        },
    ],
    "11": [
        {
            "__parent": "10"
        },
        {
            "name": "jit",
            "const": "off"
        }
    ],
    "12": [
        {
            "__parent": "11"
        }
    ],
    "13": [
        {
            "__parent": "12"
        }
    ],
    "14": [
        {
            "__parent": "13"
        }
    ],
    "15": [
        {
            "__parent": "14"
        }
    ],
    "16": [
        {
            "__parent": "15"
        }
    ],
    "17": [
        {
            "__parent": "16"
        }
    ],
}
