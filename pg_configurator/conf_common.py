common_alg_set = {
    "9.6": [
        # ----------------------------------------------------------------------------------
        # Extensions
        {
            "name": "shared_preload_libraries",
            "alg": """\
                'pg_stat_statements,pg_store_plans,auto_explain,plantuner,online_analyze' if duty_db == DutyDB.ERP1C else \
                'pg_stat_statements,auto_explain' """,
            "to_unit": "as_is"
        },
        # The auto_explain module provides a means for logging execution plans of slow statements automatically,
        # without having to run EXPLAIN by hand.
        {
            "name": "auto_explain.log_min_duration",
            "alg":  """\
                '3s' if duty_db == DutyDB.FINANCIAL else \
                '5s' if duty_db in [DutyDB.MIXED, DutyDB.ERP1C] else \
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
        # ----------------------------------------------------------------------------------
        # Logging
        {
            "name": "logging_collector",
            "const": "on"
        },
        {
            "name": "log_truncate_on_rotation",
            "const": "on"
        },
        {
            "name": "log_rotation_age",
            "const": "1d"
        },
        {
            "name": "log_destination",
            "const": "'csvlog'"
        },
        {
            "name": "log_directory",
            "const": "'pg_log'"
        },
        {
            "name": "log_filename",
            "const": "'postgresql-%Y-%m-%d_%H%M%S.log'"
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
        # Controls information prefixed to each log line for pg-monitor.
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
            "alg":  """\
                'off' if duty_db == DutyDB.ERP1C else \
                'on'""",
            "to_unit": "as_is"
        },
        {
            "name": "standard_conforming_strings",
            "alg":  """\
                'off' if duty_db == DutyDB.ERP1C else \
                'on'""",
            "to_unit": "as_is"                
        },
        # ----------------------------------------------------------------------------------
        # Connection and authentication
        # ----------------------------------------------------------------------------------
        {
            "name": "row_security",
            "alg":  """\
                'off' if duty_db == DutyDB.ERP1C else \
                'on'""",
            "to_unit": "as_is"  
        },
        {
            "name": "ssl",
            "const":  "off"  
        }
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
    ]
}
