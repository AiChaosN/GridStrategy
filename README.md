# GridStrategy 目前测试阶段 

### TODO
- [ ] 1. 参数部xx
  - [x] 1.1 参数初步确认
  - [ ] 1.2 参数整理
  - [ ] 1.3 自动调参
- [ ] 2. 股票数据
  - [x] 2.1 特定数据获取
  - [x] 2.2 数据存储
  - [ ] 2.3 灵活数据获取
  - [ ] 2.4 动态获取数据
- [ ] 3. 网格策略实现
  - [x] 3.1 基础网格策略
  - [ ] 3.2 网格策略完善
  - [ ] 3.3 网格策略优化
- [ ] 4. 可视xx
  - [x] 4.1 数据可视化
  - [ ] 4.2 策略可视化
  - [ ] 4.3 交易可视化


### 未来
- [ ] 5.部署
  - [ ] 5.1 服务器部署
  - [ ] 5.2 本地部署
  - [ ] 5.3 交易部署



### 代码目录:
```
.
├── README.md
├── config.json
├── data
├── images
├── main.ipynb
├── old
└── src
```


### 相关参数说明:

数据获取阶段:
```
url api网址
productType 产品类型
granularity 时间粒度
startTime 开始时间
endTime 结束时间
kLineType K线类型
limit 限制条数
```

策略参数:
```
gridNum 网格数量
lower_bound 下限
upper_bound 上限

investment 投资金额
leverage 杠杆倍数
mode 网格模式
```


策略数据结构:
```
股票价格



```
参考指标:
```
1. 网格收益率
2. 网格收益率标准差

```


