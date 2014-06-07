ywbserver
=========

yangwabao server (app and weixin) new version
RESTful API:

yangwabao server (app and weixin) 
new version RESTful API:

注册 
POST domain/user/register/ 
必选参数： username base64编码过的用户名 password base64编码过的密码 
可选参数： name 用户宝贝的名字 babyheight 宝贝的体重 babyweight 宝贝的身高 birthday 宝贝的生日 （格式：2014-01-01） babysex 宝贝的性别 （'boy' or 'girl'） 
返回： True 注册成功 False 注册失败 DuplicateName 用户名已被注册

身份验证 （无状态登录） 
POST domain/user/informationcheck/ 
必选参数： username base64编码过的用户名 password base64编码过的密码 
返回： True 身份验证成功 False 身份验证失败

更新用户信息 
POST domain/user/update/ 
必选参数： username base64编码过的用户名 password base64编码过的密码 
可选参数： name 用户宝贝的名字 babyheight 宝贝的体重 babyweight 宝贝的身高 birthday 宝贝的生日 （格式：2014-01-01） babysex 宝贝的性别 （'boy' or 'girl'） 返回： AUTH_FAILED 身份认证失败 True 更新成功 False 更新失败


获取今日知识的列表 
POST domain/mobile/getknowledges 
必选参数： username base64编码过的用户名 password base64编码过的密码 
可选参数： knumber 要返回知识的条数 
返回数据： AUTH_FAILED 认证失败 
或者 json格式字符串（若干条知识简易内容的列表）： [ {knowledgeId:知识id, knowledgeTitle:知识标题, pic:知识图片链接, icon:知识图标链接}, ..... ]


获取周边商家的列表 
POST domain/mobile/getshops 
必选参数： username base64编码过的用户名 password base64编码过的密码 
可选参数： snumber 要返回知识的条数 
返回数据： AUTH_FAILED 认证失败 
或者 json格式字符串（若干条周边商家的列表）


获取今日特价的列表 
POST domain/mobile/getconsumptions 
必选参数： username base64编码过的用户名 password base64编码过的密码 
可选参数： cnumber 要返回知识的条数 
返回数据： AUTH_FAILED 认证失败 
或者 json格式字符串（若干条商品信息的列表）


根据id获取一条知识的详细内容 
GET domain/knowledge/webview/{id}/ 
必选参数： {id} 知识的id 
返回数据： 对应知识的html页面

根据id获取一个商家的详细内容 
GET domain/shop/webview/{id}/ 
必选参数： {id} 商家的id 
返回数据： 对应商家的html页面

根据id获取一件商品的详细内容 
GET domain/consumption/webview/{id}/ 
必选参数： {id} 商品的id 
返回数据： 对应商品的html页面

访问用户的圈圈
GET  domain/quan/gettopicwebview/{id}/
必选参数： {id} 商品的id
返回数据： 用户圈圈的html页面

收藏一条知识 
POST domain/knowledge/collectknowl 
必选参数： username base64编码过的用户名 password base64编码过的密码 id 知识id 
返回： AUTH_FAILED 身份认证失败 True 收藏成功 False 收藏失败



