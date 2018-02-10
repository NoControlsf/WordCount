drop table if EXISTS pjws;
create table pjws(
"文件名" TEXT,
"法院名称" TEXT,
 "文书类型" TEXT,
 "案号" TEXT,
 "原告" TEXT,
 "被告" TEXT,
 "裁判日期" TEXT,
"裁判要旨段原文" TEXT
)

drop table if EXISTS pjwserror;
create table pjwserror(
'errorurl' TEXT
)

drop table if EXISTS pjwserrorart;
create table pjwserrorart(
"文件名" TEXT,
"法院名称" TEXT,
 "文书类型" TEXT,
 "案号" TEXT,
 "裁判要旨段原文" TEXT
)