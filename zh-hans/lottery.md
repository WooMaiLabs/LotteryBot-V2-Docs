[<- 返回目录](index.md)

# 中奖结果的计算

> Revision 1

我们为 [Lottery Bot V2](about.md) 设计了一套抽奖算法。设计该算法的目的是使用具有不可否认性的随机数据来源来进行透明公正的抽奖计算。<br>
该算法基于[以太坊](https://zh.wikipedia.org/wiki/%E4%BB%A5%E5%A4%AA%E5%9D%8A)区块链数据来计算获奖者。<br>
由于区块链的去中心化特性，用户无需信任我们，也可确保抽奖结果的公平公正。

> 注意: 本文中所述的“以太坊”均为 Ethereum 1.0 (PoW) 区块链, 并非 Ethereum 2.0 (PoS)。

## 计算方式

### 准备数据

1. 抽奖 ID、抽奖参与人数与奖品份数。
2. 公示的所有参与用户的 [Telegram User ID Hash](#user-id-hash-的计算方式)，将这些 ID 写入一个数组，并按 ASCII 码<b>从大到小</b>分配 0 开始的自增 ID。
3. 开奖时间之后的第一个以太坊 Block Hash (不包含 `0x` 前缀)。

我们提供了一个 API 接口以获取这些数据。

```
# curl https://lottery.tg/lottery/{Lottery_ID}/data
```

### 计算初始开奖种子

伪代码， `sha256` 函数返回格式为小写 Hex 字符串， `+` 号为拼接字符串。

```
开奖种子 = sha256(抽奖ID + 参与人数 + 总奖品份数 + Block Hash)
```

### 计算中奖人

> 须使用大数运算

1. 将 `开奖种子` 的 16 进制转换为 10 进制。
2. 将该十进制数字除以总参与人数，余数对应的自增 ID 即为中奖人，奖品按顺序发放。
3. 如该用户已在中奖列表或不符合中奖条件，或者尚有未开奖品，则将 `开奖种子` 再次 SHA256，作为新的 `开奖种子` ，回到第 1 步再次计算，直到所有奖品分发完成。

## 验证工具

我们提供了用于自行验证中奖结果的工具。该工具是 [开源的](https://github.com/WooMaiLabs/LotteryBot-V2-Docs/tree/master/tools/verify-tool)。

## 关于计算方式的更新

我们可能会出于漏洞修复、稳定性、公平合理性、数据源不可用等原因修改抽奖算法。<br>
如果我们修改了计算方法，将会同步更新此文档。<br>
同时，如果您认为当前的计算方式存在问题或抱有疑问，欢迎通过邮件 `lotbot@wmlabs.net` 联系我们。

## 附录

### User ID Hash 的计算方式

我们在设计算法时尽可能同时保证透明公开与用户隐私。<br>
在计算中奖人时，计算 User ID Hash 的伪代码如下，其中 `+` 号为拼接字符串:

``` 

User ID Hash = sha256(User ID + 抽奖ID)
```

### 如何控制中奖结果？

首先，你需要拥有可观的以太坊算力（中奖概率和算力呈正比，甚至达到[全网算力的 51%](https://academy.binance.com/zh/security/what-is-a-51-percent-attack)）参与挖矿。<br>
如果你在开奖后最先挖出了新区块并且计算出自己没有中奖，则可以放弃这个区块的奖励（当前每个区块收益相当于 2000 美元左右）不上报，然后在期望没有其他矿工抢先的情况下，自己挖出的下一个区块可以让自己中奖。<br>
所以在绝大多数情况下，控制中奖结果或提高中奖概率是非常困难、成本相当高且仍然难以控制的。

### 为什么选择基于以太坊区块链？

我们首先确定了选择使用基于 [工作量证明 (PoW)](https://www.coindesk.com/what-is-proof-of-work) 的区块链作为不可否定的随机数据来源。<br>
在 [PoW 加密货币排行](https://www.f2pool.com/coins) 中的前几位中，比特币的全网算力位列第一，但由于 [比特币的平均 Block Time](https://bitinfocharts.com/comparison/bitcoin-confirmationtime.html) 为 10 分钟（一般在 5~60 分钟中浮动），在一个即时通信平台上，未免时间有些太长。<br>
我们将目光转向了排名第二的以太坊。[以太坊的平均 Block Time](https://etherscan.io/chart/blocktime) 仅为 13.3 秒，同时全网算力仍然[高到难以实施攻击](https://www.crypto51.app/)。<br>
这正是我们所需要的。所以我们选择了以太坊。
