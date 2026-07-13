
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


```python
import httpx
from a2a import client as a2a_client
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.auth import default
from google.auth.transport.requests import Request as AuthRequest

# 1. Google Cloud 인증을 위한 httpx.Auth 클래스 정의
class GoogleCloudAuth(httpx.Auth):
    """Auto-refreshing Google Cloud authentication for httpx."""
    def __init__(self):
        self.credentials, _ = default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

    def auth_flow(self, request):
        if not self.credentials.valid:
            self.credentials.refresh(AuthRequest())
        
        request.headers["Authorization"] = f"Bearer {self.credentials.token}"
        yield request


# 2. 인증이 적용된 커스텀 ClientFactory 생성
# A2A SDK의 ClientFactory는 기본적으로 HTTP 클라이언트 주입을 지원합니다.
class AuthenticatedA2AClientFactory(a2a_client.ClientFactory):
    def __init__(self, auth: httpx.Auth, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.auth = auth

    # 내부적으로 사용하는 httpx.AsyncClient에 인증 정보를 주입하도록 오버라이드
    async def _ensure_httpx_client(self):
        if not self._httpx_client:
            self._httpx_client = httpx.AsyncClient(auth=self.auth, timeout=60.0)
        return self._httpx_client


# 3. RemoteA2aAgent 생성 및 팩토리 적용
AGENT_CARD_URL = "https://asia-northeast1-aiplatform.googleapis.com/v1/projects/..."

# 커스텀 팩토리 인스턴스 생성
auth_factory = AuthenticatedA2AClientFactory(auth=GoogleCloudAuth())

remote_agent = RemoteA2aAgent(
    name="my_remote_agent",
    description="Handles requests by delegating to a deployed Vertex AI Agent.",
    agent_card=AGENT_CARD_URL,
    # deprecated된 httpx_client 대신 a2a_client_factory 사용
    a2a_client_factory=auth_factory,
)

```