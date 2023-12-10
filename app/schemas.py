from pydantic import BaseModel


class URLBase(BaseModel):
    target_url: str


class URL(URLBase):
    is_active: bool
    clicks: int
    key: str

    class Config:
        orm_mode = True


class URLInfo(URL):
    url: str


class URLAdminInfo(URLInfo):
    secret_key: str
    admin_url: str
