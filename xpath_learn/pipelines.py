# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.utils.project import get_project_settings
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XpathLearnPipeline:
    def __init__(self):
        settings = get_project_settings()
        self.client = pymongo.MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])

        # 数据库登录需要帐号密码的话
        print(settings['MONGODB_USER'])
        self.client.admin.authenticate(settings['MONGODB_USER'], settings['MONGODB_PASSWORD'])

        self.db = self.client[settings['MONGODB_DB']]  # 获得数据库的句柄
        self.coll = self.db[settings['MONGODB_COL']]  # 获得collection的句柄


    def process_item(self, item, spider):

        x = self.coll.insert_one(dict(item))
        print(x.inserted_id)
        return item

