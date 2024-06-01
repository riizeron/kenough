import logging
import jinja2

import yaml


from jinja2 import Environment, FileSystemLoader


class Templator:
    def __init__(self, config):
        self.logger = logging.getLogger("orch" +__name__)

        self.running = None

        self.job_config = config['job']

        env = Environment(loader = FileSystemLoader(config['templates_path']), trim_blocks=True, lstrip_blocks=True)
        self.job_template = env.get_template('job.j2')
        self.logger.debug(f"GET JOB JINJA2 TEMPLATE")


    def render(self, task_id, task_config) -> dict:
        self.logger.info(f"Task {task_id} | Get task")
        self.logger.debug(f"Task {task_id} | Task config: {task_config}")
        task_config.update({'job': self.job_config})


        rendered = self.job_template.render(task_config)
        self.logger.debug(f"Task {task_id} | Rendered job:\n{rendered}")
        job_dict = yaml.safe_load(rendered)

        return job_dict



