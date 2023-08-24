#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2023/08/24 22:19
# @File           : excel_schema.py
# @IDE            : PyCharm
# @desc           :


from pydantic import BaseModel, Field


class AlignmentModel(BaseModel):
    horizontal: str = Field('center', description="水平对齐方式。可选值：'left'、'center'、'right'、'justify'、'distributed'")
    vertical: str = Field('center', description="垂直对齐方式。可选值：'top'、'center'、'bottom'、'justify'、'distributed'")
    textRotation: int = Field(0, description="文本旋转角度（以度为单位）。默认为 0。")
    wrapText: bool = Field(None, description="自动换行文本。设置为 True 时，如果文本内容超出单元格宽度，会自动换行显示。")
    shrinkToFit: bool = Field(
        None,
        description="缩小字体以适应单元格。设置为 True 时，如果文本内容超出单元格宽度，会自动缩小字体大小以适应。"
    )
    indent: int = Field(0, description="文本缩进级别。默认为 0。")
    relativeIndent: int = Field(0, description="相对缩进级别。默认为 0。")
    justifyLastLine: bool = Field(
        None,
        description="对齐换行文本的末尾行。设置为 True 时，如果设置了文本换行，末尾的行也会被对齐。"
    )
    readingOrder: int = Field(0, description="阅读顺序。默认为 0。")

    class Config:
        title = "对齐设置模型"
        description = "用于设置单元格内容的对齐样式。"


class FontModel(BaseModel):
    name: str = Field(None, description="字体名称")
    size: float = Field(None, description="字体大小（磅为单位）")
    bold: bool = Field(None, description="是否加粗")
    italic: bool = Field(None, description="是否斜体")
    underline: str = Field(None, description="下划线样式。可选值：'single'、'double'、'singleAccounting'、'doubleAccounting'")
    strikethrough: bool = Field(None, description="是否有删除线")
    outline: bool = Field(None, description="是否轮廓字体")
    shadow: bool = Field(None, description="是否阴影字体")
    condense: bool = Field(None, description="是否压缩字体")
    extend: bool = Field(None, description="是否扩展字体")
    vertAlign: str = Field(None, description="垂直对齐方式。可选值：'superscript'、'subscript'、'baseline'")
    color: dict = Field(None, description="字体颜色")
    scheme: str = Field(None, description="字体方案。可选值：'major'、'minor'")
    charset: int = Field(None, description="字符集编号")
    family: int = Field(None, description="字体族编号")

    class Config:
        title = "字体设置模型"
        description = "用于设置单元格内容的字体样式"


class PatternFillModel(BaseModel):
    start_color: str = Field(None, description="起始颜色（RGB 值或颜色名称）")
    end_color: str = Field(None, description="结束颜色（RGB 值或颜色名称）")
    fill_type: str = Field("solid", description="填充类型（'none'、'solid'、'darkDown' 等）")

    class Config:
        title = "填充模式设置模型"
        description = "单元格的填充模式设置"

