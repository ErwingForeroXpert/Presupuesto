#  -*- coding: utf-8 -*-
#    Created on 07/01/2022 15:51:23
#    @author: ErwingForero 
# 

from typing import Any
import vaex as vx
from vaex.dataframe import DataFrameLocal
import pandas as pd
import numpy as np
from utils import utils 

class DataFrameOptimized(DataFrameLocal):

    def __init__(self, table = None) -> None:
        super().__init__()
        self.table = table
        self.__alerts = np.array([])

    def getTableExcel(self, path: str, sheet: str) -> 'DataFrameOptimized':
        try:
            self.table = self.from_tuple(utils.getTableOfExcelSheet(path, sheet))
            return self
        except Exception as e:
            raise Exception(f"getTableExcel - {e}")

    def deleteRows(self, criteria: function) -> 'DataFrameOptimized':
        
        try:
            if self.table != None:
                _df = self.table
            else:
                raise ValueError("instance need table value")

            self.table = _df[criteria]
            return self

        except Exception as e:
            raise Exception(f"deleteRows {e}")

    def insertAlert(self, alert) -> None:

        try:
            np.append(self.__alerts, alert, axis=0)
        except Exception as e:
            raise Exception(f"insertAlert {e}")
        
    def getAlerts(self) -> 'np.array':
        return self.__alerts

    @staticmethod
    def from_tuple(values: tuple, columns: tuple) -> 'Any':
        try:
            assert len(values[0]) != len(columns) #if num of columns not is the same

            return vx.from_pandas(pd.DataFrame(values, columns=columns))
        except Exception as e:
            raise Exception(f"from_tuple - {e}")
    
    @staticmethod
    def make_criteria(dataframe: 'DataFrameOptimized', validator: 'dict[str:function]') -> 'np.array':
        mask = None

        for column, validation in validator.items(): # str, function
            mask = np.apply_along_axis(validation, 0, np.array(dataframe[f"{column}"]))  \
                if mask is None else mask & np.apply_along_axis(validation, 0, np.array(dataframe[f"{column}"]))
        
        return mask
