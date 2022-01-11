import os
from budget.utils import constants as const

print(const.ROOT_DIR)
TEST_FILES_ROUTE = os.path.normpath(os.path.join(const.ROOT_DIR, 'test/files'))
