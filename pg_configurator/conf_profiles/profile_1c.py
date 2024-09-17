alg_set_1c = {
    "9.6": [
        {
            "name": "shared_preload_libraries",
            "const": "pg_stat_statements,pg_store_plans,auto_explain,plantuner,online_analyze",
            "to_unit": "as_is"
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
        {
            "name": "standard_conforming_strings",
            "const": "on"
        },
        {
            "name": "escape_string_warning",
            "const": "on"
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
        }
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
            "__parent": "16"
        }
    ]
}
