# Known Issues

## Issue: Databricks Free Edition Removes Resources After Inactivity
### Description
The Databricks Free Edition workspace is expected to keep its resources between weekly runs. However, it has been observed several times in recent weeks that after about a week of inactivity, the serving endpoint is removed and the notebook pipeline schedule is stopped. None of this is mentioned in the Free Edition documentation, and no notice was given, which is disappointing for a platform that is meant to host a long-running project.
### Affected Areas
- Model serving through the Databricks endpoint.
- The Simulator relies on the endpoint for predictions.
- The scheduled notebook pipeline on Databricks.
### Symptoms
- The serving endpoint no longer exists, and prediction requests from the Simulator fail.
- The notebook job schedule stops triggering, with no error or failed run recorded.
- Recreating the endpoint through the API fails with `400 Client Error: Cannot create or update model serving endpoints, please try again later.` until someone logs in to the workspace manually.
### Workarounds
- **Recreate Endpoint Manually**: Log in to Databricks, restart the paused workloads, then recreate the endpoint with the champion model.
- **Disable Deployment Step**: The deployment step is removed from the pipeline, which now loads the champion model offline, so a missing endpoint no longer fails the pipeline.
- **Warn Users**: The Simulator shows a warning when the prediction service is unavailable.
- **Resume Schedule**: The notebook schedule has to be resumed manually in the Jobs UI.
### Status
- The official [Free Edition limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations) only mention compute shutdowns for exceeding the usage quota and deletion of accounts that are inactive for a prolonged period. Neither explains resources disappearing after one idle week.
- On logging in after a week away, the workspace showed "Your workloads were paused while you were away", confirming the pause is deliberate. Still, this policy is not documented anywhere, and users only find out after their workloads have already stopped.
