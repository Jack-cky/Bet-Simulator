from dagster import ConfigurableResource
from mlflow.deployments import get_deploy_client
from requests.exceptions import HTTPError


class DatabricksResource(ConfigurableResource):
    endpoint: str
    host: str
    token: str

    def get_client(self):
        return get_deploy_client("databricks")

    def endpoint_exists(self) -> bool:
        try:
            self.get_client().get_endpoint(self.endpoint)
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                return False
            raise
        return True

    def get_endpoint_readiness(self) -> bool:
        endpoint = self.get_client().get_endpoint(self.endpoint)
        state = endpoint["state"]
        status = False

        match state["ready"], state["config_update"]:
            case ("FAILED", _) | (_, "UPDATE_FAILED"):
                raise RuntimeError(
                    f"Serving endpoint is in a failed state: {state}"
                )
            case ("NOT_READY", _) | (_, "IN_PROGRESS"):
                status = False
            case ("READY", "NOT_UPDATING"):
                status = True

        return status

    def get_endpoint_config(self, model_uc: str, version: str) -> dict:
        return {
            "served_entities": [{
                "entity_name": model_uc,
                "entity_version": version,
                "workload_size": "Small",
                "workload_type": "CPU",
                "scale_to_zero_enabled": True,
            }],
        }

    def create_endpoint(self, model_uc: str, version: str) -> None:
        self.get_client().create_endpoint(config={
            "name": self.endpoint,
            "config": self.get_endpoint_config(model_uc, version),
        })

    def update_endpoint(self, model_uc: str, version: str) -> None:
        self.get_client().update_endpoint_config(
            endpoint=self.endpoint,
            config=self.get_endpoint_config(model_uc, version),
        )
