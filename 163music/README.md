### 模拟登录网易云音乐

---
  - 1.URL识别
        URL: https://music.163.com/weapi/login/cellphone?csrf_token=
  - 2.返回Json 
  - 3.传递参数
    - params
    - encSecKey
    <p>加密后的参数</p>
   - **参数解析**
   
     ```javascript
          #  bqL2x(["流泪", "强"])："010001"  
          #  bqL2x(Yb6V.md)："00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
          #  bqL2x(["爱心", "女孩", "惊恐", "大笑"])： "0CoJUm6Qyw8W8jud"
          var bVV0x = window.asrsea(JSON.stringify(i1x), bqL2x(["流泪", "强"]), bqL2x(Yb6V.md), bqL2x(["爱心", "女孩", "惊恐", "大笑"]));
          e1x.data = k1x.cv3x({
                      params: bVV0x.encText,
                      encSecKey: bVV0x.encSecKey
                  }
      ```
   - window.asrsea方法
     ```javascript
        !function() {
            function a(a) {
                var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
                for (d = 0; a > d; d += 1)
                    e = Math.random() * b.length,
                    e = Math.floor(e),
                    c += b.charAt(e);
                return c
            }
            function b(a, b) {
                var c = CryptoJS.enc.Utf8.parse(b)
                  , d = CryptoJS.enc.Utf8.parse("0102030405060708")
                  , e = CryptoJS.enc.Utf8.parse(a)
                  , f = CryptoJS.AES.encrypt(e, c, {
                    iv: d,
                    mode: CryptoJS.mode.CBC
                });
                return f.toString()
            }
            function c(a, b, c) {
                // i,e,f
                var d, e;
                return setMaxDigits(131),
                d = new RSAKeyPair(b,"",c),
                e = encryptedString(d, a)
            }
            function d(d, e, f, g) {
                var h = {}
                  , i = a(16);
                return h.encText = b(d, g),
                h.encText = b(h.encText, i),
                h.encSecKey = c(i, e, f),
                h
            }
            function e(a, b, d, e) {
                var f = {};
                return f.encText = c(a + e, b, d),
                f
            }
            window.asrsea = d,
            window.ecnonasr = e
        }();
      ```

   - JSON.stringify(i1x) 数据参数
    <p>i1x:这里使用Firefox的调试功能，设置断点，然后进行分析得出
     ```javascript
     # 登录时
         args = '{"phone":"%s","password":"%s","rememberLogin":"true","checkToken":"","csrf_token": ""}' % (
            self.username, hashlib.md5(bytes(self.password, encoding="utf-8")).hexdigest())
     # 签到时
         args = '{"type":1,"csrf_token":"%s"}' % csrf_token
     ```
   
  