from pg_configurator.configurator import run_pgc


def _cli_entrypoint() -> None:
    run_pgc()


if __name__ == "__main__":
    _cli_entrypoint()
