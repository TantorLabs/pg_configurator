import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class TestExclude(unittest.TestCase):
    parameters = {"min_wal_size", "max_wal_size", "log_destination"}

    def generate(self, output_format, *extra_args):
        result = subprocess.run(
            [sys.executable, "-m", "pg_configurator",
             "--db-cpu=8", "--db-ram=16Gi", "--pg-version=16",
             "--common-conf", "--output-format=" + output_format, *extra_args],
            check=True, capture_output=True, text=True,
            cwd=Path(__file__).resolve().parents[1],
        )
        # The CLI currently prints algorithm preparation messages before its output.
        return "\n".join(
            line for line in result.stdout.splitlines()
            if not line.startswith("Called prepare_alg_set for ")
        )

    def parse(self, output_format, output):
        if output_format == "conf":
            return dict(
                line.split(" = ", 1) for line in output.splitlines()
                if line and not line.lstrip().startswith("#")
            )
        data = json.loads(output)
        return data["postgresql"]["parameters"] if output_format == "patroni-json" else data

    def test_exclusions_preserve_other_recommendations_in_all_formats(self):
        for output_format in ("conf", "json", "patroni-json"):
            baseline = self.parse(output_format, self.generate(output_format))
            self.assertTrue(self.parameters <= baseline.keys())
            expected = {k: v for k, v in baseline.items() if k not in self.parameters}
            for flag in ("--exclude", "-exlude"):
                with self.subTest(output_format=output_format, flag=flag):
                    output = self.generate(
                        output_format,
                        flag + "=min_wal_size, max_wal_size,log_destination",
                    )
                    self.assertEqual(self.parse(output_format, output), expected)

    def test_empty_and_unknown_names_leave_recommendations_unchanged(self):
        baseline = json.loads(self.generate("json"))
        for names in ("", " , , ", "unknown_parameter", " , unknown_parameter, "):
            with self.subTest(names=names):
                self.assertEqual(
                    json.loads(self.generate("json", "--exclude=" + names)), baseline,
                )

    def test_duplicates_and_empty_entries(self):
        baseline = json.loads(self.generate("json"))
        del baseline["min_wal_size"]
        output = self.generate("json", "--exclude= , min_wal_size,min_wal_size, ,")
        self.assertEqual(json.loads(output), baseline)

    def test_exclusions_are_written_to_patroni_file(self):
        baseline = json.loads(self.generate("patroni-json"))
        for name in self.parameters:
            del baseline["postgresql"]["parameters"][name]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "postgresql.json"
            self.generate(
                "patroni-json", "--exclude=" + ",".join(sorted(self.parameters)),
                "--output-file-name=" + str(path),
            )
            self.assertEqual(json.loads(path.read_text()), baseline)


if __name__ == "__main__":
    unittest.main()
