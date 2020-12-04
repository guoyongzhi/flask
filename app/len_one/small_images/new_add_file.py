

init_info = """import unittest
from common.factory import Factory
from common.log import mylog
from ddt import ddt, data, feed_data, add_test
from common.getconf import *


@ddt
class Test_case_%s(unittest.TestCase):
    fac = Factory("%s", r"%s")
    isOK, execute_cases = fac.init_execute_case()

    @data(*execute_cases)  # 方法三（data数据list重载，需要缩进到for循环添加重载后面）
    def test_run_%s(self, cases_dict):
"""
pah = r"""
        for key, cases in cases_dict.items():
            mylog.info('\n----------用例【%s】开始----------' % cases[0].get('sheet'))
            print('\n')
            for case in cases:
                # print(case)
                isOK, result = self.fac.execute_keyword(**case)
                if isOK:
                    # print(result)
                    mylog.info(result)
                else:
                    mylog.error(result)
                    raise Exception(result)
            mylog.info('\n----------用例【%s】结束----------' % cases[0].get('sheet'))
        
        # def tearDown(self):
        #     return self.fac.close()
        
        
if __name__ == '__main__':
    unittest.main()
"""


def write_test_info(name, n, path):
    with open(r'I://work//TestUI//execute_test//test_' + name + '.py', mode='w', encoding='utf-8') as f:
        f.write(init_info % (name, n, path, name) + pah)
    f.close()
    return True


if __name__ == '__main__':
    a = write_test_info('test_', 'sf', r'info\set')
    print(a)
