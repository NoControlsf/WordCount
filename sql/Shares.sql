DROP TABLE IF EXISTS HSSharesA;
CREATE TABLE HSSharesA(
"stockCode" TEXT,       --股票代码
"stockName" TEXT,       --名称
"lastPrice" TEXT,       --最新价
"RFPrice" TEXT,         --涨跌额
"RFRange" TEXT,         --涨跌幅
"Swing" TEXT,           --振幅
"DealNum" TEXT,         --成交量(手)
"DealPrice" TEXT,       --成交额
"YTDClose" TEXT,        --昨收
"TDOpen" TEXT,          --今开
"MaxPrice" TEXT,        --最高
"MinPrice" TEXT,        --最低
"RFFiveMS" TEXT,        --5分钟涨跌
"QRR" TEXT,             --量比
"ChangeHands" TEXT,     --换手
"PERatio" TEXT,         --市盈率(动)
"Date" TEXT             --日期
);


--港股 港元
DROP TABLE IF EXISTS HKShares;
CREATE TABLE HKShares(
"stockCode" TEXT,       --股票代码
"stockName" TEXT,       --名称
"lastPrice" TEXT,       --最新价
"RFPrice" TEXT,         --涨跌额
"RFRange" TEXT,         --涨跌幅
"DealNum" TEXT,         --成交量(股)
"DealPrice" TEXT,       --成交额（港元）
"TDOpen" TEXT,          --今开
"MaxPrice" TEXT,        --最高
"MinPrice" TEXT,        --最低
"YTDClose" TEXT,        --昨收
"Date" TEXT             --日期
);

--美股 美元
DROP TABLE IF EXISTS USShares;
CREATE TABLE USShares(
"shortName" TEXT,       --简称
"stockName" TEXT,       --名称
"TDOpen" TEXT,          --今开
"YTDClose" TEXT,        --昨收
"lastPrice" TEXT,       --最新价
"RFPrice" TEXT,         --涨跌额
"RFRange" TEXT,         --涨跌幅
"ChangeHands" TEXT,     --换手率
"MaxPrice" TEXT,        --最高价
"MinPrice" TEXT,        --最低价
"DealNum" TEXT,         --成交量
"DealPrice" TEXT,       --成交额
"Buy" TEXT,             --外盘
"Sell" TEXT,            --内盘
"GeneralCapital" TEXT,  --总股本
"MarketCap" TEXT,       --总市值
"PBR" TEXT,             --市净率
"Income" TEXT,          --收益(动)
"ShowDate" TEXT,        --时间
"BVPS" TEXT,            --每股净资产
"AveragePrice" TEXT     --均价
);