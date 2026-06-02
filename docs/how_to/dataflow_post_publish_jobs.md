# Dataflow post-publish jobs (ApplyChanges / Refresh)

After `updateDefinition`, Gen2 dataflows may need **ApplyChanges** (publish) before they are runnable. Optional **Refresh** runs the dataflow.

Enable on `FabricWorkspace` (opt-in, default off):

```python
from azure.identity import AzureCliCredential
from fabric_cicd import FabricWorkspace, publish_all_items

workspace = FabricWorkspace(
    workspace_id="your-workspace-id",
    repository_directory="/path/to/data-ops-fabric",
    environment="PROD",
    item_type_in_scope=["Dataflow"],
    token_credential=AzureCliCredential(),  # az login first
    apply_dataflow_changes=True,
    refresh_dataflows=True,
)
publish_all_items(workspace)
```

| Parameter | API |
|-----------|-----|
| `apply_dataflow_changes=True` | `POST .../items/{id}/jobs/instances?jobType=ApplyChanges` |
| `refresh_dataflows=True` | `POST .../items/{id}/jobs/instances?jobType=Refresh` |

Runs after each published dataflow, in dependency order. ApplyChanges runs before Refresh when both are set.

**Auth:** `refresh_dataflows` needs a **delegated user** (SPN often returns `SPNBasedRefreshNotAllowed`). Use a **non-MFA automation account** and `AzureCliCredential()` after:

```bash
az login \
  --tenant "$AZURE_TENANT_ID" \
  --username "$FABRIC_AUTOMATION_UPN" \
  --password "$FABRIC_AUTOMATION_PASSWORD"
```

MFA-enabled users fail password login (`AADSTS50076`). Store passwords in CI secrets only.

**Parameterization:** Lakehouse/workspace IDs still come from `parameter.yml` (`find_replace`); post-publish flags only control background jobs.
