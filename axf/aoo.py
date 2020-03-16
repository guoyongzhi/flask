#!/usr/bin/Python-3.6.2
# coding=utf-8
import sys

from abc import ABCMeta, abstractmethod


class User():
    """
    用户类，模拟用户表，假设只有ID和name两个字段
    """
    
    def __init__(self):
        self.id = None
        self.name = None


class SqlServerUser():
    """
    sqlserveruser类，用于操作User表
    """

    def insert(self, user):
        print("向SQL Server中添加一个User")

    def get_user(self, id):
        print("从SQL Server中搜索User", id)


class IUser():
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, user):
        pass

    @abstractmethod
    def get_user(self, id):
        pass


class AccessUser(IUser):

    def insert(self, user):
        print("在Access中添加一个User")

    def get_user(self, id):
        print("从Access中搜索User", id)


# class IFactory():
#     __metaclass__ = ABCMeta
#
#     @abstractmethod
#     def create_user(self):
#         pass


# class SqlServerFactory(IFactory):
#     def create_user(self):
#         return SqlServerUser()
#
#
# class AccessFactory(IFactory):
#     def create_user(self):
#         return AccessUser()


class Department():
    def __init__(self):
        self.id = None
        self.name = None


class IDepartment():
    __metaclass__ = ABCMeta

    @abstractmethod
    def insert(self, department):
        pass

    @abstractmethod
    def get_department(self, id):
        pass


class SqlServerDepartment(IDepartment):
    def insert(self, department):
        print("在SQL Server中添加一个Department")

    def get_department(self, id):
        print("从SQL Server中搜索Department", id)


class AccessDepartment(IDepartment):
    def insert(self, department):
        print("在Access中添加一个Department")

    def get_department(self, id):
        print("从Access中搜索Department", id)


class IFactory():
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_user(self):
        pass

    @abstractmethod
    def create_department(self):
        pass


class SqlServerFactory(IFactory):
    def create_user(self):
        return SqlServerUser()

    def create_department(self):
        return SqlServerDepartment()


class AccessFactory(IFactory):
    def create_user(self):
        return AccessUser()

    def create_department(self):
        return AccessDepartment()


class DataAcess():
    # 类变量，通过`类名.变量名`访问
    db = "sql_server"

    @classmethod
    def create_user(self):
        if DataAcess.db == "sql_server":
            return SqlServerUser()
        elif DataAcess.db == "access":
            return AccessUser()

    @classmethod
    def create_department(self):
        if DataAcess.db == "sql_server":
            return SqlServerDepartment()
        elif DataAcess.db == "access":
            return AccessDepartment()


# def main1():
#     user = User()
#     dept = Department()
#
#     iu = DataAcess.create_user()
#     iu.insert(user)
#     iu.get_user(1)
#
#     idept = DataAcess.create_department()
#     idept.insert(dept)
#     idept.get_department(1)


def createInstance(module_name, class_name, *args, **kwargs):
    class_meta = getattr(module_name, class_name)
    obj = class_meta(*args, **kwargs)
    return obj


def main():
    db = "Access"  # load from config file
    user = User()
    dept = Department()
    
    iuser = createInstance(sys.modules[__name__], "{}User".format(db))
    iuser.insert(user)
    iuser.get_user(1)
    
    idept = createInstance(sys.modules[__name__], "{}Department".format(db))
    idept.insert(dept)
    idept.get_department(1)


main()
