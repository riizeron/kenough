import os
import logging

from src.tools.create_process import run


logger = logging.getLogger(__name__)


def semgrep_cmd(src_path: str, cur_scan_rule_path: str, report_file: str, args: list[str]):
    cmd = [
        src_path,
        '--config', cur_scan_rule_path,
        '-o', report_file
    ]

    if args:
        cmd.extend(args)

    return cmd


async def semgrep_launch_async(
    scanner_path: str,
    src_path: str,
    cur_scan_rule_path: str,
    report_file: str,
    args=None,
    timeout=60,
):
    if args is None:
        args = []

    # os.makedirs(os.path.dirname(report_file), exist_ok=True)

    cmd = semgrep_cmd(src_path, cur_scan_rule_path, report_file, args)
    logger.info(f"SEMGREP_LAUNCH_ARGS: {cmd} | SEMGREP_SCANNER_PATH: {scanner_path}")
    return await run(scanner_path, cmd, timeout, logger)


# async def gl_launch(
#     scanner_path: str,
#     src_path: str,
#     report_file: str,
#     args: list[str] = [],
#     timeout=60,
# ):
#     os.makedirs(os.path.dirname(report_file), exist_ok=True)
#
#     cmd = gl_cmd(src_path, report_file, args)
#     logger.info(f"GL_LAUNCH_ARGS: {cmd}")
#     logger.info(f"GL_SCANNER_PATH: {scanner_path}")
#
#     try:
#         proc = create_process(scanner_path, cmd)
#         stdout, stderr = proc.stdout, proc.stderr
#         logger.info(stdout.decode())
#         if stderr:
#             logger.error(stderr.decode())
#     except Exception:
#         logger.info("Process error")
#     finally:
#         return proc.returncode if proc.returncode == 0 else 1337
