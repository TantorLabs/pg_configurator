platform_common_alg_set = {
    "9.6": [
        # ----------------------------------------------------------------------------------
        # Extensions
        {
            "name": "shared_preload_libraries",
            "const": "'pg_stat_statements,pg_store_plans,auto_explain'"
        },
        # The online_analyze module provides a set of features that immediately
        # update statistics after INSERT, UPDATE, DELETE, or SELECT INTO operations for the affected tables.
        {
            "name": "online_analyze.enable",
            "const":  "'on'",
        },
        {
            "name": "online_analyze.verbose",
            "const": "off"
        },
        {
            "name": "online_analyze.scale_factor",
            "alg": "round(float(calc_scale_factor_scale(0.0007, 0.1)),4)",
            "to_unit": "as_is"
        },
        {
            "name": "online_analyze.threshold",
            "alg": "int(calc_system_scores_scale(500, 10000))",
            "to_unit": "as_is"
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
        # The auto_explain module provides a means for logging execution plans of slow statements automatically,
        # without having to run EXPLAIN by hand.
        {
            "name": "auto_explain.log_min_duration",
            "alg":  """\
                '3s' if duty_db == DutyDB.FINANCIAL else \
                '5s' if duty_db in [DutyDB.MIXED] else \
                '30s' """,
            "to_unit": "as_is"
        },
        {
            "name": "auto_explain.log_analyze",
            "const": "true"
        },
        {
            "name": "auto_explain.log_verbose",
            "const": "true"
        },
        {
            "name": "auto_explain.log_buffers",
            "const": "true"
        },
        {
            "name": "auto_explain.log_format",
            "const": "text"
        },
        {
            "name": "auto_explain.log_nested_statements",
            "const": "true"
        },
        # The pg_stat_statements module provides a means for tracking planning
        # and execution statistics of all SQL statements executed by a server.
        {
            "name": "pg_stat_statements.max",
            "alg":  """\
                '3000' if duty_db == DutyDB.FINANCIAL else \
                '5000' if duty_db == DutyDB.MIXED else \
                '7000' """,
            "to_unit": "as_is"
        },
        {
            "name": "pg_stat_statements.track",
            "const": "top"
        },
        # Store execution plans like pg_stat_statements does for queries.
        {
            "name": "pg_store_plans.max",
            "alg":  """\
                '6000' if duty_db == DutyDB.FINANCIAL else \
                '10000' if duty_db == DutyDB.MIXED else \
                '15000' """,
            "to_unit": "as_is"
        },
        {
            "name": "pg_store_plans.track",
            "const": "top"
        },
        {
            "name": "pg_store_plans.max_plan_length",
            "alg":  """\
                '3000' if duty_db == DutyDB.FINANCIAL else \
                '5000' if duty_db == DutyDB.MIXED else \
                '10000' """,
            "to_unit": "as_is"
        },
        {
            "name": "pg_store_plans.plan_format",
            "const": "raw"
        },
        {
            "name": "pg_store_plans.min_duration",
            "alg":  """\
                '100' if duty_db == DutyDB.FINANCIAL else \
                '300' if duty_db == DutyDB.MIXED else \
                '3000' """,
            "to_unit": "as_is"
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
        # Logging
        {
            "name": "log_rotation_age",
            "const": "1d"
        },
        {
            "name": "log_rotation_size",
            "const": "100MB"
        },
        {
            "name": "log_min_messages",
            "const": "warning"
        },
        {
            "name": "log_min_error_statement",
            "const": "error"
        },
        {
            "name": "log_min_duration_statement",
            "alg":  """\
                '3s' if duty_db == DutyDB.FINANCIAL else \
                '5s' if duty_db == DutyDB.MIXED else \
                '30s' """,
            "to_unit": "as_is"
        },
       {
           "name": "log_duration",
           "const": "off"
       },
       {
            "name": "log_line_prefix",
            "const": "%m [%p:%v] [%d] %r %a "
        },
        {
            "name": "log_lock_waits",
            "const": "on"
        },
        {
            "name": "log_statement",
            "const": "'ddl'"
        },
        {
            "name": "log_temp_files",
            "const": "0"
        },
        {
            "name": "log_checkpoints",
            "const": "on"
        },
        {
            "name": "log_autovacuum_min_duration",
            "const": "5s"
        },
        # For the pg-monitor to work correctly, this parameter must be in this locale
        {
            "name": "lc_messages",
            "const": "en_US.UTF-8"
        },
        # ----------------------------------------------------------------------------------
        # Statistic collection
        # ----------------------------------------------------------------------------------
        {
            "name": "track_activities",
            "const": "on"
        },
        {
            "name": "track_counts",
            "const": "on"
        },
        {
            "name": "track_io_timing",
            "const": "on"
        },
        {
            "name": "track_functions",
            "const": "pl"
        },
        {
            "name": "track_activity_query_size",
            "alg":  """\
                1024 if duty_db == DutyDB.FINANCIAL else \
                2048 if duty_db == DutyDB.MIXED else \
                4096""",
            "to_unit": "as_is"
        },
        # ----------------------------------------------------------------------------------
        # Version and platform compatibility
        # ----------------------------------------------------------------------------------
        {
            "name": "escape_string_warning",
            "const":  "on"
        },
        {
            "name": "standard_conforming_strings",
            "const":  "on"
        },
        # ----------------------------------------------------------------------------------
        # Connection and authentication
        # ----------------------------------------------------------------------------------
        {
            "name": "row_security",
            "const":  "on"
        },
        {
            "name": "ssl",
            "const":  "off"
        },
    ],
    "10": [
        {
            "__parent": "9.6"
        }
    ],
    "11": [
        {
            "__parent": "10"
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
        },
        {
            "name": "track_wal_io_timing",
            "const": "on"
        },
        {
            "name": "log_recovery_conflict_waits",
            "alg": "'on' if replication_enabled else 'off'",
            "to_unit": "as_is"
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
    "18": [
        {
            "__parent": "17"
        }
    ],
}