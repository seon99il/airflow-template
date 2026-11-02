from airflow.providers.docker.operators.docker import DockerOperator

TAG = "{{ ti.bundle_instance.version or 'dev' }}"


class PythonDockerOperator(DockerOperator):

    def __init__(self, *, file: str, func: str | None = None, image: str = "airflow-template/worker-python", **kwargs):
        if ":" in image.rsplit("/", 1)[-1]:
            raise ValueError(
                f"Image name '{image}' should not contain a tag. Use the 'TAG' variable to specify the tag.")
        module = file.removesuffix(".py").replace("/", ".")
        kwargs["command"] = (
            ["python", "-c", f"import {module}; {module}.{func}()"] if func else ["python", "-m", module]
        )
        kwargs.setdefault("auto_remove", "success")
        kwargs.setdefault("mount_tmp_dir", False)
        kwargs.setdefault("docker_url", "unix://var/run/docker.sock")
        super().__init__(image=f"{image}:{TAG}", **kwargs)
