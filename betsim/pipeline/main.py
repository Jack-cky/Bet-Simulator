import sys

from .definitions import defs
from .partitions import partition_week

__all__ = ["defs"]


def run_pipeline(partition_key: str | None = None) -> bool:
    job = defs.get_job_def("betsim_weekly_pipeline")
    partition_key = partition_key or partition_week.get_last_partition_key()

    result = job.execute_in_process(
        partition_key=partition_key,
        raise_on_error=False,
    )
    return result.success


if __name__ == "__main__":
    sys.exit(0 if run_pipeline(*sys.argv[1:2]) else 1)
