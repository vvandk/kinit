import os
from win32com.client import gencache
import comtypes.client
from core.logger import logger


def ppt_to_pdf_1(ppt_path: str, pdf_path: str):
    """
    ppt 转 pdf，会弹出 office 软件
    :param ppt_path:
    :param pdf_path:
    :return:
    """
    # 创建PDF
    powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
    powerpoint.Visible = 1
    slide = powerpoint.Presentations.Open(ppt_path)
    # 保存PDF
    slide.SaveAs(pdf_path, 32)
    slide.Close()
    # 退出 office 软件
    powerpoint.Quit()


def ppt_to_pdf_2(ppt_path: str, pdf_path: str):
    """
    完美办法，PPT 转 PDF
    :param ppt_path:
    :param pdf_path:
    :return:
    """
    p = gencache.EnsureDispatch("PowerPoint.Application")
    try:
        ppt = p.Presentations.Open(ppt_path, False, False, False)
        ppt.ExportAsFixedFormat(pdf_path, 2, PrintRange=None)
        ppt.Close()
        p.Quit()
    except Exception as e:
        print(os.path.split(ppt_path)[1], "转化失败，失败原因%s" % e)
        logger.info(os.path.split(ppt_path)[1], "转化失败，失败原因%s" % e)
