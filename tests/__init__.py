from dotenv import load_dotenv
from core.client import PyCanadaPost
import os

load_dotenv()

environment = "SANDBOX"

customer_number = int(os.getenv("CUSTOMER_NUMBER"))
api_key = os.getenv(f"API_KEY_{environment}")
contract_id = int(os.getenv("CONTRACT_ID"))

client = PyCanadaPost(
    customer_number=customer_number,
    api_key=api_key,
    contract_id=contract_id,
)