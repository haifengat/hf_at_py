# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2017/11/13'
"""
import time
from .structs import IntervalType
from .bar import Bar
from .data import Data
from .order import OrderItem


class Strategy(object):
    '''策略类 '''

    def __init__(self, dict_cfg):
        '''初始化'''
        '''策略标识'''
        self.ID = 0
        '''数据序列'''
        self.Datas = []
        """起始测试时间
        格式:yyyyMMdd[%Y%m%d]
        默认:20170101"""
        self.BeginDate = '20170101'
        
        '''参数'''
        self.Params = []
        '''分笔测试'''
        self.TickTest = False

        if dict_cfg == '':
            return
        else:
            self.ID = dict_cfg['ID']
            self.Params = dict_cfg['Params']
            self.BeginDate = str(dict_cfg['BeginDate'])
            if 'TickTest' in dict_cfg:
                self.TickTest = dict_cfg['TickTest']
            for data in dict_cfg['Datas']:
                newdata = Data(self.__BarUpdate, self.__OnOrder)
                newdata.Instrument = data['Instrument']
                newdata.Interval = data['Interval']
                newdata.IntervalType = IntervalType[data['IntervalType']]
                self.Datas.append(newdata)        

    @property
    def Bars(self):
        '''k'''
        return self.Datas[0].Bars

    @property
    def Instrument(self):
        '''合约'''
        return self.Datas[0].Instrument

    @property
    def Interval(self):
        '''周期'''
        return self.Datas[0].Interval

    @property
    def IntervalType(self):
        '''周期类型'''
        return self.Datas[0].IntervalType

    @property
    def Orders(self):
        '''买卖信号'''
        return self.Datas[0].Orders

    @property
    def IndexDict(self):
        '''指标字典
        策略使用的指标保存在此字典中
        以便管理程序显示和处理'''
        return self.Datas[0].IndexDict

    @property
    def D(self):
        '''时间'''
        return self.Datas[0].D

    @property
    def H(self):
        '''最高价'''
        return self.Datas[0].H

    @property
    def L(self):
        '''最低价'''
        return self.Datas[0].L

    @property
    def O(self):
        '''开盘价'''
        return self.Datas[0].O

    @property
    def C(self):
        '''收盘价'''
        return self.Datas[0].C

    @property
    def V(self):
        '''交易量'''
        return self.Datas[0].V

    @property
    def I(self):
        '''持仓量'''
        return self.Datas[0].I

    @property
    def AvgEntryPriceShort(self):
        '''开仓均价-空'''
        return self.Datas[0].AvgEntryPriceShort

    @property
    def AvgEntryPriceLong(self):
        '''开仓均价-多'''
        return self.Datas[0].AvgEntryPriceLong

    @property
    def PositionLong(self):
        '''持仓-多'''
        return self.Datas[0].PositionLong

    @property
    def PositionShort(self):
        '''持仓-空'''
        return self.Datas[0].PositionShort

    @property
    def EntryDateLong(self):
        '''开仓时间-多'''
        return self.Datas[0].EntryDateLong

    @property
    def EntryPriceLong(self):
        '''开仓价格-多'''
        return self.Datas[0].EntryPriceLong

    @property
    def ExitDateShort(self):
        '''平仓时间-空'''
        return self.Datas[0].ExitDateShort

    @property
    def ExitPriceShort(self):
        '''平仓价-空'''
        return self.Datas[0].ExitPriceShort

    @property
    def EntryDateShort(self):
        '''开仓时间-空'''
        return self.Datas[0].EntryDateShort

    @property
    def EntryPriceShort(self):
        '''开仓价-空'''
        return self.Datas[0].EntryPriceShort

    @property
    def ExitDateLong(self):
        '''平仓时间-多'''
        return self.Datas[0].ExitDateLong

    @property
    def ExitPriceLong(self):
        '''平仓价-多'''
        return self.Datas[0].ExitPriceLong

    @property
    def LastEntryDateShort(self):
        '''最后开仓时间-空'''
        return self.Datas[0].LastEntryDateShort

    @property
    def LastEntryPriceShort(self):
        '''最后开仓价-空'''
        return self.Datas[0].LastEntryPriceShort

    @property
    def LastEntryDateLong(self):
        '''最后开仓时间-多'''
        return self.Datas[0].LastEntryDateLong

    @property
    def LastEntryPriceLong(self):
        '''最后开仓价-多'''
        return self.Datas[0].LastEntryPriceLong

    @property
    def IndexEntryLong(self):
        '''开仓到当前K线数量-多'''
        return self.Datas[0].IndexEntryLong

    @property
    def IndexEntryShort(self):
        '''开仓到当前K线数量-空'''
        return self.Datas[0].IndexEntryShort

    @property
    def IndexLastEntryLong(self):
        '''最后平仓到当前K线数量-多'''
        return self.Datas[0].IndexLastEntryLong

    @property
    def IndexLastEntryShort(self):
        '''最后平仓到当前K线数量-空'''
        return self.Datas[0].IndexLastEntryShort

    @property
    def IndexExitLong(self):
        '''平仓到当前K线数量-多'''
        return self.Datas[0].IndexExitLong

    @property
    def IndexExitShort(self):
        '''平仓到当前K线数量-空'''
        return self.Datas[0].IndexExitShort

    @property
    def Position(self):
        '''持仓净头寸'''
        return self.Datas[0].Position

    @property
    def CurrentBar(self):
        '''当前K线序号(0开始)'''
        return self.Datas[0].CurrentBar

    def Buy(self, price: float, volume: int, remark: str = ''):
        """买开"""
        self.Datas[0].Buy(price, volume, remark)

    def Sell(self, price, volume, remark):
        """买平"""
        self.Datas[0].Sell(price, volume, remark)

    def SellShort(self, price, volume, remark):
        """卖开"""
        self.Datas[0].SellShort(price, volume, remark)

    def BuyToCover(self, price, volume, remark):
        """买平"""
        self.Datas[0].BuyToCover(price, volume, remark)

    def OnBarUpdate(self, data: Data, bar: Bar):
        """行情触发
        历史行情:每分钟触发一次
        实时行情:每分钟触发一次"""
        pass

    def __BarUpdate(self, data: Data, bar: Bar):
        """调用策略的逻辑部分"""
        # self.OnBarUpdate(data, bar)
        if data.Interval == self.Interval and data.IntervalType == self.IntervalType:
            self.OnBarUpdate(data, bar)

    def __OnOrder(self, data: Data, order: OrderItem):
        """调用外部接口的reqorder"""
        # 同时接口发单可不注释 
        self._data_order(self, data, order)

    # 外层接口调用
    def _data_order(self, stra, data: Data, order: OrderItem):
        """继承类中实现此函数,有策略信号产生时调用"""
        pass
