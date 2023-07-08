from boto3 import Session

from ..models import *


class LambdaClient:
    @property
    def client(self):
        return Session().client("lambda", region_name="us-east-1")
    
    def create_function(self, function: Function):
        response = self.client.create_function(**function.dict(exclude_none=True))
        url = self.client.create_function_url_congig(
            FunctionName=response["FunctionName"],
            AuthType="NONE",
            Cors={
                  "AllowOrigins": ["*"],
                "AllowMethods": ["*"],
                "AllowHeaders": ["*"],
                "AllowCredentials": True,
                "ExposeHeaders": ["*"],
                "MaxAge": 86400
            }
        )
        self.client.add_permission(
            FunctionName=response["FunctionName"],
            StatementId=str(uuid4()),
             Action="lambda:InvokeFunctionUrl",
            Principal="*",
            FunctionUrlAuthType="NONE"
        )
        return url["FunctionUrl"]
    
    def update_function(self, function: Function):
        return self.client.update_function_configuration(**function.dict(exclude_none=True))

    def delete_function(self, function: Function):
        return self.client.delete_function(FunctionName=function.name)