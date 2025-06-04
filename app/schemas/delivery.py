from pydantic import BaseModel

class DeliveryAgentRegister(BaseModel):
    agent_phone: str