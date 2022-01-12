#  -*- coding: utf-8 -*-
#    Created on 07/01/2022 15:51:23
#    @author: ErwingForero 
# 


from ctypes import Array
import os
from typing import Any
import pandas as pd
import vaex as vx
from vaex.execution import Executor
import xlwings as xw
import time 
from . import constants as const

def waitBookDisable(mybook):
    """Wait until the book is closed

    Args:
        mybook (String): path of the excel book
    """
    while isIterable(xw.books):
        time.sleep(1)
        for book in xw.books:
            if book.fullname == mybook:
                book.save()
        book.app.quit()

def isIterable(posibleList):
    """Validate if element is iterable

    Args:
        posibleList (Any): posible iterable element

    Returns:
        bool: if element is iterable
    """
    try:
        if isinstance(posibleList, (tuple, list)) or hasattr(posibleList, "__iter__"):
            _ = posibleList[0]
            return True

        return False
    except Exception as e:
        return False

def RunMacro(excel_file: str, name_macro: str, _args=None) -> 'any':
    """Run Macro of excel book

    Args:
        excel_file (str): path of excel book
        name_macro (str): name of macro
        _args ([type], optional): other args of macro. Defaults to None.

    Raises:
        Exception: Excel Book not found or valid

    Returns:
        Any: Macro result
    """
    result = None
    waitBookDisable(excel_file)
    book_mmto = xw.Book(excel_file)
    if book_mmto is None:
        raise Exception(f"El libro no se encuentra o no se puede abrir")
    
    result = book_mmto.macro(name_macro)(*_args) if _args is not None else book_mmto.macro(name_macro)()
    
    book_mmto.save()

    if len(book_mmto.app.books) == 1:
        book_mmto.app.quit()
    else:
        book_mmto.close()

    return result

def getTableOfExcelSheet(file_path: str, sheet: str, macro: str = const.MACRO_EXTRACT_TABLE_SHEET) -> 'Any':
    """Get Table of sheet in Excel File

    Raises:
        Exception: [description]

    Returns:
        Any: tuple
    """
    try:
        _table, _columns = RunMacro(file_path, macro, [sheet])

        return _table, _columns

    except Exception as e:
        raise Exception(f"getTableOfExcelSheet - {e}")
    