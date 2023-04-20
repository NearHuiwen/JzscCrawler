## **建筑数据破解JS逆向爬虫**
Requests+PyExecJS

网站调用的JS文件：req_aes.js

**目标**

```python
抓包，抓取建筑市场数据(注：用于学习，不是商用或其他恶意用途)
```

**实现步骤**

- **1、Fidder抓包,发现返回的数据跟个鬼一样**

<img src="https://raw.githubusercontent.com/NearHuiwen/JzscCrawler/master/image/1681978576151.png" width="800">
  

- **2、定位JS文件**

那我们通过url 下手试试 在All里面全局 搜索 project/list(url后面的参数，怎么方便怎么来) 
  
一直定位到这里，很明显看得出用了AES加密，国企项目都那么喜欢AES吗，哈哈。。。

其实大厂加密都简单，安全防护之类的完全不靠js加密，靠的是风控，用一个大佬跟我说的话，当你把加解密破解之后，游戏才刚刚开始

<img src="https://raw.githubusercontent.com/NearHuiwen/JzscCrawler/master/image/1681979257343.png" width="800">
  
确定AES了，考虑一般是AES直接加密或者AES + RSA，企业比较广泛吧，不知道哪个Diao毛想的，玩挺花

当然AES + RSA 组合更加安全,RSA的公钥私钥保持不变,AES的秘钥每次随机生成,发送方用AES加密原文,再用公钥加密AES的秘钥,带上加密后的秘钥和密文去请求.而接受方则先用私钥解密得到AES的秘钥再对密文进行解密
 
- **3、手撕JS代码（扣代码）**

```js
var CryptoJS = require('crypto-js')

function getDecryptedData(t) {
    var m = CryptoJS.enc.Utf8.parse("偏移值"),
        f = CryptoJS.enc.Utf8.parse("秘钥"),
        e = CryptoJS.enc.Hex.parse(t),
        n = CryptoJS.enc.Base64.stringify(e),
        a = CryptoJS.AES.decrypt(n, f, {
            iv: m,
            mode: CryptoJS.mode.CBC,
            padding: CryptoJS.pad.Pkcs7
        }),
        r = a.toString(CryptoJS.enc.Utf8);
    return r.toString()
}
```

直接写python也可以
```Python
f = '秘钥'  # 秘钥
m = '偏移值'  # 偏移值
# 转码  utf-8?  字节 16进制
m = bytes(m, encoding='utf-8')
f = bytes(f, encoding='utf-8')
# 创建一个AES算法 秘钥  模式 偏移值
cipher = AES.new(f, AES.MODE_CBC, m)
# 解密
decrypt_content = cipher.decrypt(bytes.fromhex(response))
result = str(decrypt_content, encoding='utf-8')
# OKCS7 填充
length = len(result) # 字符串长度
unpadding = ord(result[length - 1]) # 得到最后一个字符串的ASCII
result = result[0:length - unpadding]
```