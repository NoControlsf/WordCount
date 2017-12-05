drop table if EXISTS house163;
create table house163(
"website" TEXT,                 --网址
"statisticsDate" TEXT,          --统计日期
 "realEstateName" TEXT,         --楼盘名
 "district" TEXT,               --区域
 "num" TEXT,                    --已售统计套数
 "area" TEXT,                   --已售统计面积
 "averagePrice" TEXT,           --已售统计均价
"salesAmount" TEXT,             --已售统计销售金额
"soldNumber" TEXT,              --累计已售套数
"soldArea" TEXT,                --累计已售面积
"unsoldNumber" TEXT,            --累计未售套数
"unsoldArea" TEXT,              --累计未售面积
"percent" TEXT                  --去化
)