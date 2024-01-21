from typing import Any
from pydantic import BaseModel, Field


class SchemaField(BaseModel):
    name: str = Field(..., title="字段名称")
    field_type: str = Field(..., title="字段类型")
    nullable: bool = Field(False, title="是否可以为空")
    default: Any = Field(None, title="默认值")
    title: str | None = Field(None, title="字段描述")
    max_length: int | None = Field(None, title="最大长度")
