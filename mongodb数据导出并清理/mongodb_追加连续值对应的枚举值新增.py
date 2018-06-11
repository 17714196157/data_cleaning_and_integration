import time
from mongoengine import Document, IntField, StringField, connect, DateTimeField
import mongoengine
from datetime import datetime
import re

# conn_mongodb = connect('BusinessCircles', host='localhost', port=27017, username='guiji', password='guiji@123qwe')

conn_mongodb = connect('admin', host='192.168.1.192', port=27017, username='qinyuchen', password='qq3@django')

print("has connect")

class Company(mongoengine.Document):
    name = mongoengine.StringField(max_length=255, required=True)
    lagel_person = mongoengine.StringField(max_length=255, null=True)
    register_capital = mongoengine.StringField(null=True)
    # register_time = db.DateTimeField(null=True)
    register_time = mongoengine.StringField(null=True)
    tel = mongoengine.StringField(null=True)
    area = mongoengine.StringField(required=True, default="中国")
    update_time = mongoengine.DateTimeField(default=datetime.now)
    company_id = mongoengine.SequenceField(required=True)
    reg_time = mongoengine.StringField(default="0")
    reg_capital = mongoengine.StringField(default="0")
    # 定义为索引
    meta = {
         'indexes': ["name", "lagel_person", "area"]
    }


REGISTER_TIME_ENUM = {'1': [-1, 2018],
                      '2': [2017, 2013],
                      '3': [2012, 2008],
                      '4': [2007, 2003],
                      '5': [2002, -1],
                      }

REGISTER_CAPITAL_ENUM= {'1': [100, 0],
                      '2': [200, 100],
                      '3': [500, 200],
                      '4': [1000, 500],
                      '5': [-1, 1000],
                      }


def enumerate_valueof_enum(node_value, REGISTER_ENUM_MAP):
    '''
    :param node_value: 可以是 表示整数的 str 或者 int
    :param REGISTER_ENUM_MAP:
    :return:
    '''
    if isinstance(node_value, str) and node_value.isdigit:
        node_value = int(node_value)
    elif isinstance(node_value, int):
        pass
    else:
        node_ENUM = '0'
        return node_ENUM

    for enum in REGISTER_ENUM_MAP:
        end = REGISTER_ENUM_MAP[enum][0]
        start = REGISTER_ENUM_MAP[enum][1]
        # print(start, end)
        if start != -1 and end !=-1 :
            if node_value in range(start, end+1):
                node_ENUM = enum
                return node_ENUM
        if start == -1 and node_value <= end:
            node_ENUM = enum
            return node_ENUM
        if end == -1 and node_value >= start:
            node_ENUM = enum
            return node_ENUM


res_db = Company.objects()

index = 0
for item in res_db:
    node_data = eval(item.to_json())
    print(type(node_data), node_data)

    register_time = node_data['register_time']
    register_capital = node_data['register_capital'].strip()

    try:
        date_node_register = time.strptime(register_time, "%Y-%m-%d")
    except Exception as e:
        print("ERROR ", register_time, register_capital)
        node_REGISTER_TIME_ENUM = "0"

    node_REGISTER_TIME_ENUM = enumerate_valueof_enum(date_node_register.tm_year, REGISTER_TIME_ENUM)
    if register_capital != "":
        # capital = re.findall(register_capital, "")
        capital = re.findall(r"(\d+)[.]*\d*\s*万",register_capital)
        if len(capital) != 0:
            capital = capital[-1]
            node_REGISTER_CAPITAL_ENUM = enumerate_valueof_enum(capital, REGISTER_CAPITAL_ENUM)
        else:
            print("ERROR register_capital not find", register_capital,node_data['name'])
            node_REGISTER_CAPITAL_ENUM = "0"
    else:
        node_REGISTER_CAPITAL_ENUM = "0"


    # node_data.update({'REGISTER_TIME_ENUM':node_REGISTER_TIME_ENUM,'REGISTER_CAPITAL_ENUM':node_REGISTER_CAPITAL_ENUM})
    # print(dir(Company))
    # Company.update(node_data)
    item.reg_time = node_REGISTER_TIME_ENUM
    item.reg_capital = node_REGISTER_CAPITAL_ENUM
    item.save()
    if divmod(index, 10000)[1] == 0:
        print(register_time, register_capital)
        print(node_REGISTER_TIME_ENUM, node_REGISTER_CAPITAL_ENUM)
        print(str(index), eval(item.to_json()))
    index = index + 1


    # # 插入数据
    # node_data_object = Company(
    #     node_data
    # )
    # node_data_object.save()
    # input(node_data)
