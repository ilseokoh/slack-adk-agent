
## Deploy to Cloud Run

```
gcloud run deploy slack-root-agent --allow-unauthenticated --region asia-northeast1 --env-vars-file=.env  --source=. --clear-base-image --no-deploy-health-check

Building using Dockerfile and deploying container to Cloud Run service [slack-root-agent] in project [kevin-ai-playground] region [asia-northeast1]
✓ Building and deploying new service... Done.
  ✓ Validating configuration...
  ✓ Uploading sources...
  ✓ Building Container... Logs are available at [ https://console.cloud.google.com/cloud-build/builds;region=asia-north
  east1/3b70da97-9f7c-4dda-99fa-e244f117f019?project=83441239233 ].
  ✓ Creating Revision...
  ✓ Routing traffic...
  ✓ Setting IAM Policy...
Done.
Service [slack-root-agent] revision [slack-root-agent-00001-rwh] has been deployed and is serving 100 percent of traffic.
Service URL: https://slack-root-agent-83441239233.asia-northeast1.run.app
```