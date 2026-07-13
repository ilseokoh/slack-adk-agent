
## Deploy to Cloud Run

### VPC setup
[Direct VPC Egress](https://docs.cloud.google.com/run/docs/configuring/vpc-direct-vpc)
 - create VPC and Subnet (asia-northeast1)
 - create Cloud NAT
 - Private Google Access on for the subnet

### Deployment options 

 - 배포 후 발생할 수 있는 현상 Cloud Run은 Request가 올 때 Instance를 만든다. 최소 인스턴스를 주지 않으면 Socket 연결을 실행할 Instance가 최초에 없어서 반응이 없는 것 같음 --> Cloud Run URL 을 접속하면 "Starting new instance. Reason: MANUAL_OR_CUSTOMER_MIN_INSTANCE - Instance started because of customer-configured min-instances or manual scaling." 로그를 볼 수 있다. 
 - --network=default --subnet=default --vpc-egress=all-traffic : Direct VPC Egress 설정 
 - 

```
gcloud run deploy slack-root-agent --allow-unauthenticated --region asia-northeast1 --env-vars-file=.env  --source=. --clear-base-image --no-deploy-health-check --network=default --subnet=default --vpc-egress=all-traffic --min-instances=1 --max-instances=2

Building using Dockerfile and deploying container to Cloud Run service [slack-root-agent] in project [kevin-ai-playground] region [asia-northeast1]
✓ Building and deploying... Done.                                                                                                                                                                       
  ✓ Validating configuration...                                                                                                                                                                         
  ✓ Uploading sources...                                                                                                                                                                                
  ✓ Building Container... Logs are available at [ https://console.cloud.google.com/cloud-build/builds;region=asia-northeast1/e8d611ed-070e-4364-8681-f50a37a62275?project=834471899683 ].               
  ✓ Creating Revision...                                                                                                                                                                                
  ✓ Routing traffic...                                                                                                                                                                                  
  ✓ Setting IAM Policy...                                                                                                                                                                               
Done.                                                                                                                                                                                                   
Service [slack-root-agent] revision [slack-root-agent-00003-78t] has been deployed and is serving 100 percent of traffic.
Service URL: https://slack-root-agent-834471899683.asia-northeast1.run.app
```