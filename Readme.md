# Readme

* 项目状态：开发中。

# 简介：

* 目前的功能是请求对应IP的会员购页面，记录已有商品，出现新商品时，发邮件通知用户。
* 请填写`config.toml`​中对应的配置，`token`​为smtp的授权码。
* 添加新IP请自行抓取IP的API请求，查看POST报文内`IP`对应的值，将其作为添加到主函数内的字典。
## TODO:
* [ ] 添加图片到邮件中