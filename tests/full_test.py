import asyncio
import json
import os.path
import time

from pg_configurator.configurator import *
import subprocess
import unittest
import socket
import asyncpg

import sys
"""
sys.path.append('pg_configurator/common.py')
from pg_configurator.common import *
"""
#from pg_configurator.common import recordset_to_list_flat, exception_helper, ResultCode
#from pg_configurator.pg_configurator import PGConfigurator, run_pgc


passed_stages = []


class TestParams:
    test_db_user = 'postgres'         # default value
    test_db_user_password = 'mYy5RexGsZ'
    test_db_host = '127.0.0.1'
    test_db_port = '5432'
    test_db_name = 'test_db'
    test_scale = '10'
    test_threads = 4
    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

    containers = [
        ['pg_9_6', '9.6', 5480],
        ['pg_10', '10', 5481],
        ['pg_11', '11', 5482],
        ['pg_12', '12', 5483],
        ['pg_13', '13', 5484],
        ['pg_14', '14', 5485],
        ['pg_15', '15', 5486],
        ['pg_16', '16', 5487]
    ]

    pg_params = [
        {
            "name": "listen_addresses",
            "const": "'*'"
        }
    ]

    def __init__(self):
        if os.environ.get('TEST_DB_USER') is not None:
            self.test_db_user = os.environ["TEST_DB_USER"]
        if os.environ.get('PGPASSWORD') is not None:
            self.test_db_user_password = os.environ["TEST_DB_USER_PASSWORD"]
        if os.environ.get('TEST_DB_USER_PASSWORD') is not None:
            self.test_db_user_password = os.environ["TEST_DB_USER_PASSWORD"]
        if os.environ.get('TEST_DB_HOST') is not None:
            self.test_db_host = os.environ["TEST_DB_HOST"]
        if os.environ.get('TEST_DB_PORT') is not None:
            self.test_db_port = os.environ["TEST_DB_PORT"]
        if os.environ.get('TEST_SOURCE_DB') is not None:
            self.test_source_db = os.environ["TEST_SOURCE_DB"]
        if os.environ.get('TEST_SCALE') is not None:
            self.test_scale = os.environ["TEST_SCALE"]
        if os.environ.get('TEST_THREADS') is not None:
            self.test_threads = os.environ["TEST_THREADS"]
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)


params = TestParams()


class DBOperations:

    @staticmethod
    async def init_db(db_conn, db_name):
        try:
            await db_conn.execute(
                """
                SELECT pg_terminate_backend(pid)
                FROM pg_stat_activity
                WHERE pid <> pg_backend_pid()
                    AND datname = '%s'
                """ % db_name)

            print("""DROP DATABASE IF EXISTS %s and CREATE DATABASE""" % db_name)
            await db_conn.execute("""DROP DATABASE IF EXISTS %s""" % db_name)
            await db_conn.execute(
                """
                CREATE DATABASE %s
                    WITH
                    OWNER = %s
                    ENCODING = 'UTF8'
                    LC_COLLATE = 'en_US.UTF-8'
                    LC_CTYPE = 'en_US.UTF-8'
                    template = template0
                """ % (db_name, params.test_db_user))
        except:
            print(exception_helper(show_traceback=True))

    @staticmethod
    async def check_params(container, settings_list=None):
        data = None
        db_conn = None
        try:
            conn_params = {
                "host": params.test_db_host,
                "database": 'postgres',
                "port": container[2],
                "user": 'postgres',
                "password": params.test_db_user_password
            }
            db_conn = await asyncpg.connect(**conn_params)
            query = """
                SELECT
                    name,
                    setting AS value
                FROM pg_settings
                WHERE name in (
                    %s
                )
                ORDER BY name ASC
                """ % (
                    """
                        'autovacuum_work_mem',
                        'shared_buffers',
                        'work_mem',
                        'maintenance_work_mem'
                    """ if settings_list is None else ', '.join(["'" + v + "'" for v in settings_list])
                )
            print(query)
            data = recordset_to_list_flat(await db_conn.fetch(query))
            print(str(container) + " -> " + str(data))
        except:
            print(exception_helper(show_traceback=True))
        finally:
            if db_conn:
                await db_conn.close()
        return data

    @staticmethod
    async def check_extension_params(container, settings_list=None):
        data = []
        db_conn = None
        try:
            conn_params = {
                "host": params.test_db_host,
                "database": 'postgres',
                "port": container[2],
                "user": 'postgres',
                "password": params.test_db_user_password
            }
            db_conn = await asyncpg.connect(**conn_params)
            for v in settings_list:
                query = """show \"%s\"""" % v
                print(query)
                data.append([v, recordset_to_list_flat(await db_conn.fetch(query))[0][0]])
                print(str(container) + " -> " + str(data))
        except:
            print(exception_helper(show_traceback=True))
        finally:
            if db_conn:
                await db_conn.close()
        return data


    @staticmethod
    def run_command(cmd, print_output=True):
        print("=".join(['=' * 100]))
        print(str(' '.join(cmd)))
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if print_output:
            print(">>")
            if err.decode("utf-8") != "":
                print('ERROR:\n%s' % err.decode("utf-8"))
            for line in out.decode("utf-8").split("\n"):
                print('    ' + line)
        return out.decode("utf-8"), err.decode("utf-8")

    @staticmethod
    async def init_containers(do_docker_pull=False, containers=[]):
        init_containers_res = True

        containers_for_processing = params.containers
        if containers is not None and len(containers) > 0:
            containers_for_processing = containers

        for v in containers_for_processing:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', v[2]))
            sock.close()
            if result != 111:
                DBOperations.run_command(['docker', 'restart', v[0]])

            if result == 111:
                if do_docker_pull:
                    DBOperations.run_command(['docker', 'pull', 'postgres:%s' % v[1]])
                DBOperations.run_command(['docker', 'stop', v[0]])
                DBOperations.run_command(['docker', 'rm', '-f', v[0]])
                DBOperations.run_command(['docker',  'run',
                     '-p', '%s:5432' % str(v[2]),
                     '--name', v[0],
                     '-v', '%s:/tmp' % params.output_dir,
                     '-v', '%s.conf:/etc/postgresql/postgresql.conf' % os.path.join(params.output_dir, v[0]),
                     '-e', 'POSTGRES_PASSWORD=%s' % params.test_db_user_password,
                     '-e', 'POSTGRES_HOST_AUTH_METHOD=md5',
                     '-d', 'postgres:%s' % v[1],
                     '-c', "config_file=/etc/postgresql/postgresql.conf"
                ])
                print("=========> To connect use: docker exec -it %s bash" % v[0])

        time.sleep(3)

        for v in params.containers:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', v[2]))
            sock.close()
            if result != 0:
                print("=========> ERROR in: %s" % str(v))
                DBOperations.run_command(['docker', 'logs', v[0]])
                init_containers_res = False
            else:
                await DBOperations.check_params(v)

        passed_stages.append("init_env")
        return init_containers_res

    @staticmethod
    def clear_containers():
        for v in params.containers:
            DBOperations.run_command(['docker', 'stop', v[0]])
            DBOperations.run_command(['docker', 'rm', '-f', v[0]])
            # docker rm $(docker ps -a -f status=exited -q)
            # docker volume prune

    @staticmethod
    def get_pgbench_results(pgbench_output: str) -> dict:
        def get_val(str_v, t):
            for m in str_v:
                sub_str = pgbench_output[m.span()[0]:m.span()[1]]
                val = re.finditer(r"\d+((.|,)\d+)?", sub_str)
                for vv in val:
                    if t == 'float':
                        return float(sub_str[vv.span()[0]:vv.span()[1]])
                    if t == 'int':
                        return int(sub_str[vv.span()[0]:vv.span()[1]])

        return {
            "number of transactions actually processed": get_val(
                re.finditer(r"number\sof\stransactions\sactually\sprocessed\:\s\d+((.|,)\d+)?", pgbench_output),
                'int'
            ),
            "latency average": get_val(
                re.finditer(r"latency\saverage\s=\s\d+((.|,)\d+)?\sms", pgbench_output),
                'float'
            ),
            "initial connection time": get_val(
                re.finditer(r"initial\sconnection\stime\s=\s\d+((.|,)\d+)?\sms", pgbench_output),
                'float'
            ),
            "tps": get_val(
                re.finditer(r"tps\s=\s\d+((.|,)\d+)?", pgbench_output),
                'float'
            )
        }


class BasicUnitTest:
    async def init_env(self):
        if "init_env" in passed_stages:
            return True
        # DBOperations.clear_containers()
        return await DBOperations.init_containers()


class UnitTest(unittest.IsolatedAsyncioTestCase, BasicUnitTest):
    def test_01_gen_conf(self):
        parser = PGConfigurator.get_arg_parser()
        for v in params.containers:
            args = parser.parse_args([
                '--output-file-name=%s.conf' % os.path.join(params.output_dir, v[0]),
                '--pg-version=%s' % v[1],
            ])
            self.assertTrue(run_pgc(args, params.pg_params))

    async def test_02_init(self):
        self.assertTrue(await self.init_env())

        for target_db in params.containers:
            conn_params = {
                "host": params.test_db_host,
                "database": 'postgres',
                "port": target_db[2],
                "user": 'postgres',
                "password": params.test_db_user_password
            }
            db_conn = await asyncpg.connect(**conn_params)
            await DBOperations.init_db(db_conn, "perf_db")
            await db_conn.close()

        passed_stages.append("test_02_init")

    async def test_03_run_pgbench(self):
        self.assertTrue("test_02_init" in passed_stages)

        # stop all containers
        for target_db in params.containers:
            DBOperations.run_command(['docker', 'stop', target_db[0]])

        def create_db_objs(target_db):
            return DBOperations.run_command([
                'psql', '-f', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'db_objs.sql'),
                '-U', 'postgres',
                '-h', '127.0.0.1',
                '-p', str(target_db[2]),
                '-d', 'perf_db'
            ], print_output=False)

        results = {}
        for target_db in params.containers:
            DBOperations.run_command(['docker', 'start', target_db[0]])
            time.sleep(3)
            os.environ['PGPASSWORD'] = params.test_db_user_password
            out, err = create_db_objs(target_db)
            if err is not None and (
                    err.find("the database system is starting up") > -1 or
                    err.find("server closed the connection unexpectedly") > -1
            ):
                time.sleep(3)
                create_db_objs(target_db)

            out, _ = DBOperations.run_command([
                'pgbench',
                '-c', '8',
                '-j', '4',
                '-T', '10',
                '-U', 'postgres',
                '-h', '127.0.0.1',
                '-p', str(target_db[2]),
                '-f', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'workload.sql'),
                'perf_db'
            ], print_output=False)

            results[target_db[0]] = DBOperations.get_pgbench_results(out)
            DBOperations.run_command(['docker', 'stop', target_db[0]])

        print(str(json.dumps(results, indent=4)))
        passed_stages.append("test_03_run_pgbench")


class UnitTestProfiles(unittest.IsolatedAsyncioTestCase, BasicUnitTest):

    async def test_01_profiles(self):
        return
        parser = PGConfigurator.get_arg_parser()
        results = {}
        for v in params.containers:
            if v[0] in ('pg_14', 'pg_15'):
                args = parser.parse_args([
                    '--output-file-name=%s.conf' % os.path.join(params.output_dir, v[0]),
                    '--conf-profiles=ext_perf,profile_1c',
                    '--pg-version=%s' % v[1],
                ])
                results[v[0]] = run_pgc(args, params.pg_params).result_data
                print(str(json.dumps(results, indent=4)))
                DBOperations.run_command(['docker', 'stop', v[0]])
                _, err = DBOperations.run_command(['docker', 'start', v[0]])
                if err.find("No such container") > -1:
                    await DBOperations.init_containers(containers=[v])
                time.sleep(3)
                DBOperations.run_command(['docker', 'logs', v[0]])
                params_values = await DBOperations.check_params(v, [
                    'from_collapse_limit',
                    'join_collapse_limit'
                ])
                self.assertTrue(params_values is not None)
                for p in [
                    ['from_collapse_limit', '20'],
                    ['join_collapse_limit', '20']
                ]:
                    self.assertTrue(p in params_values)
                DBOperations.run_command(['docker', 'stop', v[0]])


    async def test_02_profiles_1c(self):
        parser = PGConfigurator.get_arg_parser()
        results = {}
        for v in params.containers:
            if v[0] in ('pg_14', 'pg_15'):
                args = parser.parse_args([
                    '--output-file-name=%s.conf' % os.path.join(params.output_dir, v[0]),
                    '--conf-profiles=ext_perf,profile_1c',
                    '--pg-version=%s' % v[1],
                ])
                results[v[0]] = run_pgc(args, params.pg_params).result_data
                print(str(json.dumps(results, indent=4)))
                DBOperations.run_command(['docker', 'stop', v[0]])
                _, err = DBOperations.run_command(['docker', 'start', v[0]])
                if err.find("No such container") > -1:
                    await DBOperations.init_containers(containers=[v])
                time.sleep(3)
                DBOperations.run_command(['docker', 'logs', v[0]])
                params_values = await DBOperations.check_extension_params(v, [
                    'online_analyze.enable',
                    'online_analyze.table_type',
                    'online_analyze.verbose',
                    'online_analyze.threshold',
                    'online_analyze.scale_factor',
                    'online_analyze.local_tracking',
                    'online_analyze.min_interval'
                ])
                self.assertTrue(params_values is not None)
                for p in [
                    ['online_analyze.enable', 'off'],
                    ['online_analyze.table_type', 'temporary'],
                    ['online_analyze.verbose', 'off'],
                    ['online_analyze.threshold', '500'],
                    ['online_analyze.scale_factor', '0.1'],
                    ['online_analyze.local_tracking', 'on'],
                    ['online_analyze.min_interval', '10000']
                ]:
                    if p[0] == 'online_analyze.min_interval':
                        x = 1
                    self.assertTrue(p in params_values)
                DBOperations.run_command(['docker', 'stop', v[0]])


    async def test_03_profiles_1c(self):
        parser = PGConfigurator.get_arg_parser()
        results = {}
        ver = "15"
        testname = self._testMethodName
        outputfile = '%s/%s-%s.conf' % (params.output_dir, testname, ver)
        args = parser.parse_args([
            '--output-file-name=%s' % outputfile,
            '--conf-profiles=ext_perf,profile_1c',
            '--pg-version=15',
            '--db-cpu=8', 
            '--db-ram=2048Mi',
            '--db-disk-type=SAS',
            '--db-duty=erp1c'
        ])
        results[ver] = run_pgc(args, params.pg_params).result_data
        print(str(json.dumps(results, indent=4)))
        self.assertTrue(results[ver] == json.loads("""
                {
                    "autovacuum": "on",
                    "autovacuum_analyze_scale_factor": "0.0018",
                    "autovacuum_analyze_threshold": "608",
                    "autovacuum_freeze_max_age": "500000000",
                    "autovacuum_max_workers": "4",
                    "autovacuum_multixact_freeze_max_age": "800000000",
                    "autovacuum_naptime": "20s",
                    "autovacuum_vacuum_cost_delay": "2ms",
                    "autovacuum_vacuum_cost_limit": "2068",
                    "autovacuum_vacuum_insert_scale_factor": "0.01",
                    "autovacuum_vacuum_insert_threshold": "1217",
                    "autovacuum_vacuum_scale_factor": "0.0033",
                    "autovacuum_vacuum_threshold": "1217",
                    "autovacuum_work_mem": "16MB",
                    "bgwriter_delay": "51ms",
                    "bgwriter_lru_maxpages": "1388",
                    "bgwriter_lru_multiplier": "7.0",
                    "checkpoint_completion_target": "0.9",
                    "checkpoint_timeout": "15min",
                    "client_connection_check_interval": "30s",
                    "commit_delay": "528",
                    "commit_siblings": "11",
                    "cpu_operator_cost": "0.001",
                    "default_statistics_target": "100",
                    "default_toast_compression": "lz4",
                    "effective_cache_size": "220MB",
                    "effective_io_concurrency": "4",
                    "enable_async_append": "on",
                    "escape_string_warning": "on",
                    "from_collapse_limit": "20",
                    "fsync": "on",
                    "full_page_writes": "on",
                    "hash_mem_multiplier": "8.0",
                    "hot_standby": "on",
                    "hot_standby_feedback": "on",
                    "huge_pages": "try",
                    "idle_in_transaction_session_timeout": "86400000",
                    "join_collapse_limit": "20",
                    "jit": "off",
                    "listen_addresses": "'*'",
                    "logical_decoding_work_mem": "156MB",
                    "maintenance_io_concurrency": "4",
                    "maintenance_work_mem": "17MB",
                    "max_connections": "1000",
                    "max_files_per_process": "3217",
                    "max_locks_per_transaction": "110",
                    "max_logical_replication_workers": "6",
                    "max_parallel_maintenance_workers": "4",
                    "max_parallel_workers": "5",
                    "max_parallel_workers_per_gather": "2",
                    "max_pred_locks_per_transaction": "110",
                    "max_replication_slots": "10",
                    "max_standby_streaming_delay": "-1",
                    "max_sync_workers_per_subscription": "4",
                    "max_wal_senders": "2",
                    "max_wal_size": "1764MB",
                    "max_worker_processes": "8",
                    "min_wal_size": "694MB",
                    "old_snapshot_threshold": "4320",
                    "online_analyze.enable": "off",
                    "online_analyze.local_tracking": "on",
                    "online_analyze.min_interval": "10000",
                    "online_analyze.scale_factor": "0.1",
                    "online_analyze.table_type": "temporary",
                    "online_analyze.threshold": "500",
                    "online_analyze.verbose": "off",
                    "pg_store_plans.log_analyze": "on",
                    "pg_store_plans.log_buffers": "on",
                    "pg_store_plans.max": "15000",
                    "pg_store_plans.max_plan_length": "15000",
                    "pg_store_plans.min_duration": "3000",
                    "pg_store_plans.plan_format": "raw",
                    "pg_store_plans.track": "top",
                    "plantuner.fix_empty_table": "on",
                    "random_page_cost": "2.5",
                    "seq_page_cost": "1",
                    "shared_buffers": "1111MB",
                    "standard_conforming_strings": "on",
                    "statement_timeout": "86400000",
                    "superuser_reserved_connections": "4",
                    "synchronous_commit": "None",
                    "temp_buffers": "1000kB",
                    "vacuum_cost_delay": "10ms",
                    "vacuum_cost_limit": "8000",
                    "wal_buffers": "18MB",
                    "wal_compression": "lz4",
                    "wal_keep_size": "1200MB",
                    "wal_level": "logical",
                    "wal_log_hints": "on",
                    "wal_receiver_status_interval": "10s",
                    "wal_receiver_timeout": "300s",
                    "wal_sender_timeout": "300s",
                    "wal_writer_delay": "255ms",
                    "wal_writer_flush_after": "1764kB",
                    "work_mem": "10000kB"
                }
             """)
        )

        # Generated by the Tantor-Platform
        # self.assertTrue(results[ver] == json.loads("""
        #     {
        #         "15": {
        #             "autovacuum": "on",
        #             "autovacuum_analyze_scale_factor": "0.0007",
        #             "autovacuum_analyze_threshold": "608",
        #             "autovacuum_freeze_max_age": "500000000",
        #             "autovacuum_max_workers": "4",
        #             "autovacuum_multixact_freeze_max_age": "800000000",
        #             "autovacuum_naptime": "20s",
        #             "autovacuum_vacuum_cost_delay": "2ms",
        #             "autovacuum_vacuum_cost_limit": "2068",
        #             "autovacuum_vacuum_insert_scale_factor": "0.01",
        #             "autovacuum_vacuum_insert_threshold": "1217",
        #             "autovacuum_vacuum_scale_factor": "0.001",
        #             "autovacuum_vacuum_threshold": "1217",
        #             "autovacuum_work_mem": "42MB",
        #             "bgwriter_delay": "51ms",
        #             "bgwriter_lru_maxpages": "505",
        #             "bgwriter_lru_multiplier": "4",
        #             "checkpoint_completion_target": "0.9",
        #             "checkpoint_timeout": "15min",
        #             "checkpoint_warning": "3min",
        #             "client_connection_check_interval": "30s",
        #             "commit_delay": "528",
        #             "commit_siblings": "11",
        #             "cpu_operator_cost": "0",
        #             "default_statistics_target": "100",
        #             "default_toast_compression": "lz4",
        #             "effective_cache_size": "934MB",
        #             "effective_io_concurrency": "4",
        #             "enable_async_append": "on",
        #             "from_collapse_limit": "10",
        #             "fsync": "on",
        #             "full_page_writes": "on",
        #             "hash_mem_multiplier": "8.0",
        #             "hot_standby": "on",
        #             "hot_standby_feedback": "on",
        #             "huge_pages": "try",
        #             "idle_in_transaction_session_timeout": "86400000",
        #             "join_collapse_limit": "10",
        #             "logical_decoding_work_mem": "64MB",
        #             "maintenance_io_concurrency": "4",
        #             "maintenance_work_mem": "43MB",
        #             "max_connections": "1000",
        #             "max_files_per_process": "3217",
        #             "max_locks_per_transaction": "110",
        #             "max_logical_replication_workers": "6",
        #             "max_parallel_maintenance_workers": "4",
        #             "max_parallel_workers": "4",
        #             "max_parallel_workers_per_gather": "0",
        #             "max_pred_locks_per_transaction": "110",
        #             "max_replication_slots": "10",
        #             "max_standby_streaming_delay": "-1",
        #             "max_sync_workers_per_subscription": "4",
        #             "max_wal_senders": "2",
        #             "max_wal_size": "1764MB",
        #             "max_worker_processes": "8",
        #             "min_wal_size": "694MB",
        #             "old_snapshot_threshold": "4320",
        #             "random_page_cost": "2.5",
        #             "seq_page_cost": "1",
        #             "shared_buffers": "396MB",
        #             "statement_timeout": "86400000",
        #             "superuser_reserved_connections": "4",
        #             "synchronous_commit": "off",
        #             "temp_buffers": "1000kB",
        #             "vacuum_cost_delay": "10ms",
        #             "vacuum_cost_limit": "8000",
        #             "wal_buffers": "18MB",
        #             "wal_compression": "lz4",
        #             "wal_keep_size": "1200MB",
        #             "wal_level": "replica",
        #             "wal_log_hints": "on",
        #             "wal_receiver_status_interval": "10s",
        #             "wal_receiver_timeout": "300s",
        #             "wal_sender_timeout": "300s",
        #             "wal_writer_delay": "255ms",
        #             "wal_writer_flush_after": "1764kB",
        #           "geqo": "on",
        #           "geqo_threshold": "12",
        #             "work_mem": "10000kB"
        #         }
        #     }
        #     """)
        # )


class UnitTestHistory(unittest.IsolatedAsyncioTestCase, BasicUnitTest):
    async def test_01_history_params(self):
        parser = PGConfigurator.get_arg_parser()
        args = parser.parse_args([
            '--settings-history=15,9.6',
            '--debug'
        ])
        res = run_pgc(args)
        self.assertTrue(res.result_code == ResultCode.DONE)
        args = parser.parse_args([
            '--specific-setting-history=max_parallel_maintenance_workers',
            '--debug'
        ])
        res = run_pgc(args)
        self.assertTrue(res.result_code == ResultCode.DONE)
        self.assertTrue(res.result_data == json.loads("""
            [
                {
                    "9.6": {
                        "setting": "not exists",
                        "value": "",
                        "boot_val": "",
                        "unit": ""
                    }
                },
                {
                    "10": {
                        "setting": "not exists",
                        "value": "",
                        "boot_val": "",
                        "unit": ""
                    }
                },
                {
                    "11": {
                        "setting": "max_parallel_maintenance_workers",
                        "value": "2",
                        "boot_val": "2",
                        "unit": ""
                    }
                },
                {
                    "12": {
                        "setting": "max_parallel_maintenance_workers",
                        "value": "2",
                        "boot_val": "2",
                        "unit": ""
                    }
                },
                {
                    "13": {
                        "setting": "max_parallel_maintenance_workers",
                        "value": "2",
                        "boot_val": "2",
                        "unit": ""
                    }
                },
                {
                    "14": {
                        "setting": "max_parallel_maintenance_workers",
                        "value": "2",
                        "boot_val": "2",
                        "unit": ""
                    }
                },
                {
                    "15": {
                        "setting": "max_parallel_maintenance_workers",
                        "value": "2",
                        "boot_val": "2",
                        "unit": ""
                    }
                },
                {
                    "16": {
                        "setting": "max_parallel_maintenance_workers",
                        "value": "2",
                        "boot_val": "2",
                        "unit": ""
                    }
                }
            ]
            """)
        )


if __name__ == '__main__':
    unittest.main()
    #unittest.main(exit=False)
