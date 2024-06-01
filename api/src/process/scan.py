import os
import shutil
import logging
import json

from src.git.git_client import GitClient
from src.dataclasses.task import Task

import src.configs.config as config
from src.configs.tool_config import ToolConfig

from src.tools.semgrep.cmd import semgrep_launch_async

logger = logging.getLogger(__name__)


class Scan:

    def __init__(self, task: Task, git_client: GitClient):
        self.task = task

        self.work_dir = os.path.join(config.tmp_path, str(task.task_id))
        self.path_to_zip = os.path.join(self.work_dir, str(task.task_id) + ".zip")
        self.git_client = git_client

        self.report_path = os.path.join(self.work_dir, task.task_id)
        self.cur_scan_rule_path = os.path.join(config.tmp_path, f"rules_{self.task.task_id}")

        os.makedirs(self.work_dir, exist_ok=True)
        logger.info(
            f"New scan created and will be in {self.work_dir}\t"
            f"languages: {self.task.languages}\t"
            f"taskId: {self.task.task_id}\t"
            f"repo: {self.task.repo}"
        )

    def download_sources(self):
        logger.info(f"Start downloading sources to - {self.work_dir}")
        self.git_client.checkout(self.task.repo, self.path_to_zip)

    def unzip(self, archive_format="zip"):
        logger.info("Unzipping...")
        shutil.unpack_archive(
            filename=self.path_to_zip, extract_dir=self.work_dir, format=archive_format
        )
        logger.info(f"Deleting archive - {self.path_to_zip}")
        os.remove(self.path_to_zip)
        self.git_client.init(self.work_dir)

    def clean_folder(self):
        try:
            shutil.rmtree(self.work_dir)
            shutil.rmtree(self.cur_scan_rule_path)
        except Exception as e:
            logger.error(f"Error with deleting {self.work_dir}. {e}")

    async def semgrep_scan(self, tool: ToolConfig) -> dict | None:
        logger.info(f"Semgrep Rule Path - {tool.rule_path}")
        available_rules = os.listdir(tool.rule_path)
        os.makedirs(self.cur_scan_rule_path, exist_ok=True)

        task_langs = list(map(str.lower, self.task.languages))
        logger.info(f"{available_rules=}")
        logger.info(f"{task_langs=}")

        for rule in available_rules:
            if rule.lower() in task_langs:
                path = os.path.join(tool.rule_path, rule)

                if rule == '.semgrepignore':
                    continue
                elif os.path.isdir(path):
                    shutil.copytree(path, os.path.join(self.cur_scan_rule_path, rule))
                else:
                    shutil.copy(path, self.cur_scan_rule_path)

        logger.info(f"APPLIED RULES: {os.listdir(self.cur_scan_rule_path)}")

        code = await semgrep_launch_async(
            scanner_path=tool.bin,
            src_path=self.work_dir,
            cur_scan_rule_path=self.cur_scan_rule_path,
            report_file=self.report_path,
            args=tool.args,
            timeout=tool.timeout
        )

        if code != 0:
            logger.error("Semgrep Scan Failed!")
            return None
        else:
            logger.info("Semgrep Scan Finished!")
            with open(self.report_path) as f:
                report = json.load(f)

        return report
