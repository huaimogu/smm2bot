# smm2bot
## 马造2查询机器人  
### 1.功能：https://kdocs.cn/l/saSleN4dPYUj 中的马造相关功能  
### 2.运行所需  
 (1) ~~gocqhttp~~ 已替换为官方qq  
 (2) toost(https://github.com/TheGreatRambler/toost)  
 (3) 科学上网环境  
### 3.感谢  
tgr(https://github.com/TheGreatRambler)提供的api以及采用c++重构的马造2编辑器  
jixiaomai(https://github.com/JiXiaomai) 马造2编辑器探索者和所有一些素材文件提供者  
### 4.go-cqhttp迁移方法
(1) https://bot.q.qq.com/ 注册，设置并上线机器人  
(2) 在原nonebot2项目中使用nb adapter install nonebot-adapter-qq  
(3) 在.env中的qq配置信息填入机器人的id,token,secret信息  
(4) nb run --reload启用新机器人