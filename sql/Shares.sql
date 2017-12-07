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