#  -*- coding: utf-8 -*-
#    Created on 07/01/2022 15:51:23
#    @author: ErwingForero 
# 

from genericpath import exists
import os
from typing import Any
import vaex as vx
from vaex.dataframe import DataFrameLocal
import pandas as pd
import numpy as np
from vaex.strings import array
from utils import utils 

class DataFrameOptimized(DataFrameLocal):

    def __init__(self, table = None) -> None:
        super().__init__()
        self.table = self.__process_table(table) if table is not None else None
        self.__alerts = np.array([])

    def __process_table(self, table):

        if isinstance(table, str):
            if not os.path.exists(table):
                raise FileNotFoundError(f"file not found {table}")
            if "csv" in table:
                self.table = vx.from_csv(table)
            
        elif isinstance(table, (tuple, array)):
            self.table = vx.from_arrays(table)
        elif isinstance(table, pd.DataFrame):
            self.table = vx.from_csv(table)
        else:
            raise TypeError(f"Invalid permisible type of {table}")

    def getTableExcel(self, path: str, sheet: str) -> 'DataFrameOptimized':
        try:
            self.table = self.from_tuple(utils.getTableOfExcelSheet(path, sheet))
            return self
        except Exception as e:
            raise Exception(f"getTableExcel - {e}")

    def deleteRows(self, criteria: list, limit: 'Any' = None) -> 'DataFrameOptimized':
        
        try:
            
            if self.table != None:
                _df = self.table
            else:
                raise ValueError("deleteRows - instance need table")

            if limit != None and limit > len(self.table):
                raise IndexError("deleteRows - limit is more bigger that table")

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
    def make_criteria(dataframe: 'DataFrameOptimized', validator: 'dict[str:function]', limit:'Any' = None) -> 'np.array':
        """AI is creating summary for make_criteria

        Raises:
            IndexError: Limit more bigger that dataframe

        Returns:
            numpy.Array: mask of values found with validator
        
        Examples
        --------
        dataframe = DataFrameOptimized([["column"], ["first", "second", "estr", "car", "ert", "eft"]])
        >>> mask = make_criteria(dataframe, {
            "column": lambda x: str(x).start_with("e")
        }, limit = 2)

        array([False, False, True, False, True, False])

        """
        mask = None

        for column, validation in validator.items(): # str, function
            mask = np.apply_along_axis(validation, 0, np.array(dataframe[f"{column}"]))  \
                if mask is None else mask & np.apply_along_axis(validation, 0, np.array(dataframe[f"{column}"]))
        
        if limit != None and limit > len(dataframe):
                raise IndexError("make_criteria - limit is more bigger that table")
        elif limit is not None:
            _index = 0
            while _index < limit:
                if mask[_index] == True:
                    _index += 1
            mask[_index + 1:] = False
        
        return mask
        
