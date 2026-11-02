import os

from airflow.providers.docker.operators.docker import DockerOperator

from dataplatform.operators.domain import TAG

_PROFILE_ENV = {"DBT_HOST": "host", "DBT_PORT": "port", "DBT_USER": "login", "DBT_PASSWORD": "password",
                "DBT_DBNAME": "schema"}

_OL = "macros.OpenLineageProviderPlugin"


class DbtDockerOperator(DockerOperator):

    def __init__(self, *, project: str, conn_id: str, select: str | None = None,
                 image: str = "airflow-template/worker-dbt", **kwargs):
        if ":" in image.rsplit("/", 1)[-1]:
            raise ValueError(
                f"Image name '{image}' should not contain a tag. Use the 'TAG' variable to specify the tag.")
        kwargs["command"] = ["dbt-ol", "build", "--project-dir", project] + (
            ["--select", select] if select else []
        )
        kwargs["environment"] = {
            **{env: f"{{{{ conn.{conn_id}.{field} }}}}" for env, field in _PROFILE_ENV.items()},
            "OPENLINEAGE_URL": os.environ["OPENLINEAGE_URL"],
            "OPENLINEAGE_NAMESPACE": os.environ["OPENLINEAGE_NAMESPACE"],
            "OPENLINEAGE_PARENT_ID": f"{{{{ {_OL}.lineage_parent_id(task_instance) }}}}",
            "OPENLINEAGE_ROOT_PARENT_ID": f"{{{{ {_OL}.lineage_root_parent_id(task_instance) }}}}",
            **kwargs.get("environment", {}),
        }
        kwargs.setdefault("network_mode", "airflow-template_default")
        kwargs.setdefault("auto_remove", "success")
        kwargs.setdefault("mount_tmp_dir", False)
        kwargs.setdefault("docker_url", "unix://var/run/docker.sock")
        super().__init__(image=f"{image}:{TAG}", **kwargs)
