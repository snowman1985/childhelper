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


为一个用户上传头像 
POST domain/photos/uploadhead/ 
必选参数： 
username base64编码过的用户名 password base64编码过的密码 
head  头像图片（jpg）
返回： 
AUTH_FAILED 身份认证失败 
正确返回 头像图片的url，图片大小100像素
note：
上传图片的请求模拟form提交图片的模式
示例Java代码：
package httpclienttest;

import java.io.File;  
import java.io.IOException;  
  
import org.apache.http.HttpEntity;  
import org.apache.http.HttpResponse;  
import org.apache.http.HttpStatus;  
import org.apache.http.client.ClientProtocolException;  
import org.apache.http.client.HttpClient;  
import org.apache.http.client.methods.HttpPost;  
import org.apache.http.entity.mime.MultipartEntity;  
import org.apache.http.entity.mime.content.FileBody;  
import org.apache.http.entity.mime.content.StringBody;  
import org.apache.http.impl.client.DefaultHttpClient;  
import org.apache.http.util.EntityUtils;  
  
public class SendFile {  
  
    public static void main(String[] args) throws ClientProtocolException,  
            IOException {  
        HttpClient httpclient = new DefaultHttpClient();  
        //请求处理页面  
        HttpPost httppost = new HttpPost(  
                "http://localhost:8000/photos/uploadhead/");  
        //创建待处理的文件  
        FileBody file = new FileBody(new File("head.jpg"));  
        //创建待处理的表单域内容文本  
        StringBody username = new StringBody("testuser01"); 
        StringBody password = new StringBody("testuser01pwd"); 
        //对请求的表单域进行填充  
        MultipartEntity reqEntity = new MultipartEntity();  
        reqEntity.addPart("head", file);  
        reqEntity.addPart("username", username); 
        reqEntity.addPart("password", password);  
        //设置请求  
        httppost.setEntity(reqEntity);  
        //执行  
        HttpResponse response = httpclient.execute(httppost);  
        //HttpEntity resEntity = response.getEntity();  
        //System.out.println(response.getStatusLine());  
        if(HttpStatus.SC_OK==response.getStatusLine().getStatusCode()){  
            HttpEntity entity = response.getEntity();  
            //显示内容  
            if (entity != null) {  
                System.out.println(EntityUtils.toString(entity));  
            }  
            if (entity != null) {  
                entity.consumeContent();  
            }  
        }  
    }  
} 




获取一个用户的头像url
POST domain/photos/gethead/ 
必选参数： 
username base64编码过的用户名 password base64编码过的密码 
返回： 
AUTH_FAILED 身份认证失败 
正确返回 头像图片的url，图片大小100像素

获取一个用户的个人信息
POST domain/user/getinfo/
必选参数： 
username base64编码过的用户名 password base64编码过的密码 
返回： 
AUTH_FAILED 身份认证失败 
正确返回 json，示例如下：
{"username": "sg", "schooladdr": "", "babyname": "沈如意", "birthday": "2012-05-05", "height": 32.0, "city": "北京市", "homeaddr": "北京市万泉河路68号紫金庄园", "sex": "男", "weight": 56.0, "userid": 28}



