DROP TABLE IF EXISTS transactionlist;
CREATE TABLE transactionlist (
"交易编号" TEXT,
"宗地名称" TEXT,
"iid" TEXT NOT NULL,
"宗地位置" TEXT,
"竞价起始时间" TEXT,
"起始价(万元)" TEXT,
"土地面积(平方米)合计" TEXT,
"土地面积(平方米)建设用地面积" REAL,
"土地面积(平方米)代征地面积" TEXT,
"规划建筑面积(平方米)" TEXT,
"交易方式" TEXT,
"规划用途" TEXT,
"成交日期" TEXT,
"成交价(万元)" TEXT,
"受让单位" TEXT,
"开发程度" REAL,
"现场竞价次数" REAL,
"保证金(万元)" REAL,
PRIMARY KEY ("iid")
);



DROP TABLE IF EXISTS transactionDetail;
CREATE TABLE transactionDetail (
"iid" TEXT NOT NULL,
"标题" TEXT,
"发行时间" TEXT,
"交易文件编号" TEXT,
"建设用地面积(平方米)" TEXT,
"代征地面积(平方米)" TEXT,
"规划建筑面积最小值(平方米)" TEXT,
"规划建筑面积最大值(平方米)" TEXT,
"用地性质" TEXT,
"土地开发程度" TEXT,
"地块位置" TEXT,
"挂牌竞价起始时间" TEXT,
"投标时间" TEXT,
"起始价(万元)" TEXT,
"挂牌竞买申请截止时间" TEXT,
"固定交易价格" TEXT,
"挂牌竞价截止时间" TEXT,
"最小递增幅度(万元)" TEXT,
"保证金(万元)" TEXT,
"其它文件下载" TEXT,
"交易地点" TEXT,
"联系电话" TEXT,
"下载文档路径" TEXT,
"历史报价" TEXT,
"成交时间" TEXT,
"成交价格" TEXT,
"竞得人" TEXT,
"其他竞得条件" TEXT,
PRIMARY KEY ("iid")
);


DROP TABLE IF EXISTS landLeasingList;
CREATE TABLE landLeasingList (
"受让方" TEXT,
"土地位置" TEXT,
"宗地面积（平方米）	" TEXT,
"iid" TEXT NOT NULL,
PRIMARY KEY ("iid")
);


DROP TABLE IF EXISTS landLeasingDetail;
CREATE TABLE landLeasingDetail (
"iid" TEXT NOT NULL,
"受让方名称" TEXT,
"土地位置" TEXT,
"区县" TEXT,
"宗地面积" TEXT,
"规划建筑面积" TEXT,
"规划用途" TEXT,
"土地成交价" TEXT,
"宗地四至" TEXT,
"签约时间" TEXT,
"合同约定开工时间" TEXT,
"合同约定竣工时间" TEXT,
"容积率（地上）" TEXT,
"发布时间" TEXT,
PRIMARY KEY ("iid")
);


DROP TABLE IF EXISTS buildingNameApprovalList;
CREATE TABLE buildingNameApprovalList (
"建设单位" TEXT,
"项目名称" TEXT,
"发文号" TEXT,
"立案号" TEXT,
"id" TEXT  NOT NULL,
PRIMARY KEY ("id")
);

DROP TABLE IF EXISTS buildingDetail;
CREATE TABLE buildingDetail (
"id" TEXT  NOT NULL,
"建设单位" TEXT,
"项目名称" TEXT,
"建设位置" TEXT,
"发文号" TEXT,
"立案号" TEXT,
"项目办理状态" TEXT,
PRIMARY KEY ("id")
);