import runpy

if __name__ == "__main__":
    runpy.run_module(
        mod_name="source.frameworks_and_drivers.database",
        run_name="__main__",
    )
    runpy.run_module(
        mod_name="source.frameworks_and_drivers.web",
        run_name="__main__",
    )
