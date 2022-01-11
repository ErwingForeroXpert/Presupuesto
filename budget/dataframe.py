#  -*- coding: utf-8 -*-
#    Created on 07/01/2022 15:51:23
#    @author: ErwingForero 
# 

import vaex
from utils import utils 

class DataFrameOptimized(vaex):

    def __init__(self) -> None:
        super().__init__()
        self.table = None
        
    def getTableExcel(self, path: str, sheet: str) -> None:
        self.table = utils.getTableOfExcelSheet(path, sheet)
    
    def 