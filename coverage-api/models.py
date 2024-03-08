from pydantic import BaseModel


class CoverageRequest(BaseModel):
    member_id: str
    member_dob: str
    payer_id: str


class CoverageRawModel(BaseModel):
    customer_id: str
    member_id: str
    member_dob: str
    payer_id: str
    response_copay: int | None
    response_coinsurance: int | None
    response_deductible: int | None
    response_oop_max: int | None
    ch_response_copay: int | None
    ch_response_coinsurance: int | None
    ch_response_deductible: int | None
    ch_response_oop_max: int | None
    overriden: bool
