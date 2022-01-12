import unittest
import gc
from faker import Faker
from test.test_fixtures import FakeTable
from budget.dataframes.dataframe_optimized import DataFrameOptimized

def criteriaDeleteRows(dataframe):
    validator = {
        "columna1": lambda x: str(x).lower().startswith("e"),
    }

    return DataFrameOptimized.make_criteria(dataframe, validator)

class TestDataFrameOptimized(unittest.TestCase):

    def setUp(self) -> None:
        self.fake = Faker()
        self.table = FakeTable.generateFrom({
            "columna1": self.fake.sentence,
            "columna2": self.fake.sentence,
            "columna3": self.fake.sentence
        })
    
    def test_dataframe_from_tuple(self) -> None:
        _table = DataFrameOptimized.from_tuple(self.table.values, self.table.columns)
        self.assertIsInstance(_table, DataFrameOptimized)
    
    def test_dataframe_delete_rows(self) -> None:
        _table = DataFrameOptimized.from_tuple(self.table.values, self.table.columns)
        self.assertIsInstance(_table, DataFrameOptimized)
        _table.de(criteriaDeleteRows(_table))

    def tearDown(self) -> None:
        #clear data
        del self.table
        del self.fake
        gc.collect()