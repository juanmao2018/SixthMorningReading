# 2018-12-02    Version 0.1
**说明**
1. 新增CleanMessage模块。

**TIPS**
1. 在CleanMessage模块中使用多进程方式运行时间（6.3S）大于未使用多进程方式的运行时间（4.1S），保留未使用多进程的版本。



# 2018-12-09    Version 0.1.1
**结构**
- CleanMessage 清洗消息记录

**TIPS**
1. try-except语句比if-else语言效率更高。
2. 非常规的字符太多，清洗的问题没有完全解决。
  (1) 发言人的QQ号标识中出在尖括号中。
  (2) 一开始只选取Scalers的发言来清洗任务，清洗相对简单，但未能找到所有任务，比如Day 5。
  (3) 个人回答问题的电子工具不同，看到的空格都有很多种，测试了多次才发现这个问题，(╥╯^╰╥)
  (4) 以“（回答问题时请注意复制作业的以上内容，不要自行删除，否则你的作业不会被程序纳入统计）”或者页码拆分内容，有些任务中不包含这些内容。只有回车符是每个任务都有的，(*/ω＼*)
  (5) 没有想到好的拆分任务的办法，打算任务和回答何在一起作为发言内容，但是又会影响后期数据分析的准确性；还是决定任务和回答拆分，但是木有找到比较好的办法，今天试了好多，都不理想。后续打算尝试一下set并、交、差的用法。



# 2018-12-23    Version 0.2
**结构**
- Model 
  - MemberModel.py 成员模型定义
  - MessageModel.py 消息模型定义
- Controller
  - DBController.py 数据库控制程序 
  - Cleaning
    - CleanTask.py 清洗任务信息
    - CleanMember.py 清洗成员信息
    - CleanMessage.py 清洗消息记录
    - GetInputTexts.py 获取输入的文件
  - Persistence
    - StoreMember.py 成员信息存入数据库
    - StoreMessage.py 消息存入数据库
- Utils
  - Configuration.py 公共信息
- inputs
- outputs


**说明**
1. CleanTask中多个正则表达式同时使用，提升匹配效率。
2. CleanMesssage
  (1) 去掉ID为'2109723514'或'scalerstalk@gmail.com'的发言记录；
3. 新增 MemberModel、CleanMember、StoreMember 模块。


**TIPS**
1. 使用单线程、多线程、多进程的时间均为34S左右。
2. 使用str.replace(old, new[, max])和re.sub(pattern,repl,string,count,flags)的时间分别为：9.4S、34S。
3. 使用数据库表的unique限制（发言日期、发言时间）对消息去重，清洗完的数据有73362条，插入数据库的数据有13116条。
4. 清洗入库数据SQL：
  (1) ID为邮箱，但相同用户名的有对应QQ号的清洗
```
UPDATE test.six_member six inner JOIN test.fr_member fr ON six.qqID = fr.email
SET six.qqID = fr.qq_id WHERE six.qqID like '%@%'; -- 与参照表对照

UPDATE test.six_member a inner JOIN test.six_member b ON a.qqName = b.qqName
SET a.qqID = b.qqID WHERE a.qqID like '%@%' and b.qqID not like '%@%'; -- 与自身表的对照
```
  (2) 去掉某列重复的记录
```
delete from test.six_member 
where memberid not in (select min(memberid) from (select * from test.six_member) a group by qqID);
```

