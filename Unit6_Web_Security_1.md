# Web Security
## U6M1 Web
1. Web 核心
    1. URI統一資源標識符: 資源的唯一名稱
    2. HTTP超文本傳輸協議: 傳輸資源的協議
    3. HTML超文本標記語言: 被傳輸的文本, 會包含URL
2. URI
    1. 查找或是獲取資源的基本元數據
    2. URI 包含
        1. 有被請求資源的服務器
        2. 如何向服務器何請求資源
        3. 服務器如何定位被請求資源
    3. 最新的URI 定義於RFC 3986
    4. URI 語法
        1. `<scheme>:<authority>/<path>?<query>#<fragment>`
        2. `<協議>:<authority>/<路徑>?<查詢參數>#<片段>`
            1. 協議: 用來請求資源的協議
            2. authority: 控制URI 剩餘部分, 通常是伺服器名稱
                - <用戶名>:<密碼>@<主機>:<端口>
            3. 路徑: 分層的路徑名, 會有上下層關係
            4. 查詢參數: 無分層的數據, 沒有上下層關係
            5. 片段: 資源的下屬節或下屬資源
    5. URI 範例1
        1. `foo://example.com:8042/over/there?test=bar#nose`
        2. 協議: foo
        3. authority: 主機名: example.com, 端口: 8042
        4. 路徑: over/there
        5. 查詢參數: test=bar
        6. 片段: nose
    6. URI 範例2
        1. `mailto:fishw@asu.edu`
        2. 協議: mailto
        3. authority: 用戶名: fishw, 主機名: asu.edu
    7. URI 有許多保留字符, 須改用百分號編碼表示
        1. 非保留字符: `[a-zA-Z][0-9]-._~`
        2. 保留字符百分號編碼: `%<十六進制表示>`
            1. 舉例
                1. "&": %26
                2. "%": %25
                3. " ": %20
    8. URI 相對路徑
        1. 絕對路徑: `https://example.com/text/help.html`
        2. 相對路徑:
            1. 當前協議: `//example.com/text/help.html`
            2. 當前authority: `/text/help.html`
            3. 當前路徑: `../../help.html`
3. HTTP
    1. 描述web客戶端如何向web服務器請求資源
    2. 基於TCP, 默認端口80
    3. HTTP 版本:
        1. 1.1版: RFC 2616, 最廣泛使用
        2. 3.0版: RFC 9000, 基於QUIC, UDP而非TCP
    4. HTTP 流程
        1. 服務器監聽TCP
        2. 客戶端傳送TCP 連接請求
        3. 客戶端傳送HTTP 請求
        4. 服務器讀取HTTP 請求
        5. 服務器傳送HTTP 響應
    5. HTTP實際流程還會包含緩存和代理
        1. 客戶端會查找請求的資源是否存在客戶端緩存
        2. 客戶端鏈接到服務器會經過防火牆和代理
        3. 代理也會會查找請求的資源是否存在代理緩存
    6. HTTP請求
        ```
        <方法> <資源(來自URI)> <協議版本>
        <客戶端訊息(請求頭)>
        <主體(可選)>
        ```
        1. 每行由`CRLF`隔開
        2. `CRLF`=`CR+LF`=`\r\n`=`chr(0xd)+chr(0xa)`
        3. 方法
            1. GET: 請求傳輸由URI指定的資源
            2. POST: 請求把提交的資源和URI指定的資源進行處理
            3. PUT: 請求把提交的資源儲存到指定的URI
            4. HEAD: 和GET, 但返回不包含主體
            5. web服務器可以提供任意擴展方法供客戶端請求
    7. HTTP響應
        ```
        <協議版本> <狀態碼> <狀態碼摘要>
        <響應頭>
        <主體(可選)>
        ```
        1. 基本和請求構造相同
        2. 常見狀態碼
            1. 1XX: 一般訊息
            2. 2XX: 成功
                1. 200 OK
                2. 201 Created
                3. 202 Accepted
                4. 204 No Content
            3. 3XX: 重定向
                1. 301 Moved Permanently
                2. 307 Temporary Redirect
            4. 4XX: 客戶端錯誤
                1. 400 Bad Request
                2. 401 Unauthorized
                3. 403 Forbidden
                4. 404 Not Found
            5. 5XX: 服務器錯誤
                1. 500 Internal Server Error
                2. 501 Not Implemented
                3. 502 Bad Gateway
                4. 503 Service Unavailable
    8. HTTP 基本驗證
        1. 客戶端請求未包含授權訊息, 服務器回應401 Unauthorized, 響應頭包含
            - `WWW-Authenticate: Basic realm="ReservedDocs"`
        2. 客戶端重新訪問, 在請求頭包含
            - `Authorization: Basic <Base64編碼的用戶名和密碼>`
        3. 非常不安全
    9. HTTP 1.1 身分驗證
        1. 服務器發回應隨機數作為質詢
        2. 客戶端請求包含一組哈希, 哈希由用戶名, 密碼, 指定隨機數 HTTP 方法, URL組成
        3. 服務器需要更多資訊(例如明文密碼)來驗證, 如果服務器被攻擊就有可能外洩
    10. HTTP攻擊目標
        1. 嗅探器
        2. 伺服器日志
        3. 瀏覽器
        4. 客戶端代理, 服務器代理, 防火牆
        5. TCP劫持, DPT深度包檢查機制
    11. HTTP攻擊工具
        1. 瀏覽器擴展: LiveHTTPHeader, Tamper Data
        2. Burp Suite
4. HTML
    1. 以簡單的數據格式創建可移植的超文本文檔(有超連結的文檔)
    2. 一開始基於標準通用標記語言
    3. 概念是以標籤為文本添加含意
        1. `<foo>text</foo>`: 開始標籤, 文本, 結束標籤
        2. `<bra />`: 自結束標籤
        3. `<img>`: 空白標籤
    4. 標籤屬性
        1. `<foo bar>`: 標籤 屬性
        2. `<foo bar=baz>`: 標籤 屬性=值, 值可以用單引號或雙引號
    5. 超連結標籤(anchor標籤)
        1. `<a href="https://google.com">Example</a>`
    6. 基本HTML5頁面
        ```
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <title>CES 545</title>
            </head>
            <body>
            </body>
        </html>
        ```
    7. HTML瀏覽器
        1. User Agent: 用來解析HTML, 包括但不限於瀏覽器
    8. HTML字符引用
        1. 可以使用實體引用或實體編碼
        2. 範例:"<"
            1. `&lt;`: 命名引用
            2. `&#60`:十進制引用
            3. `&#x3c`:十六進制引用
            4. `&#x0003c`:十六進制引用
    9. HTML表單
        1. 頁面組件, 用來創建HTTP請求
        2. `<form action="foo" method="bar">`
            1. action: HTTP請求目標URI, 默認是當前頁面
            2. method: HTTP請求方法GET 或POST, 默認是GET
                1. method 如果是GET, 輸入會轉換成URL 上的查詢參數
                2. POST會在主體中傳輸, 不會在URL顯示出來
                3. GET 輸入大小會受URL長度限制, POST 則可以由服務器自訂
        3. 傳輸默認會使用"application/x-www-form-urlencode"方式編碼
            1. 數據會以key-value pairs 發送, 屬性name為key, 屬性value 或是用戶輸入值為value,
            2. 屬性value莫認為空字串
            3. 會對符號以百分號編碼, 對空格轉換為"+", 鍵值對以"&"分隔
        4. 範例
            ```
            <form action="http:/example.com/submit">
                <input type="text" name="student">
                <input type="text" name="grade">
                <input type="submit" name="submit">
            ```
            1. 輸入"Fish W", "A+"後案提交
            2. URL 會變成`http:/example.com/submit?student=Fish+W&grade=A%2B&submit=Submit`
            3. 如果method 改用POST 會以查詢參數作為主體傳送到`http:/example.com/submit`


## U6M2 Web Application
1. web應用程序
    1. web設計是支持動態響應的, 但要確保響應的是同個用戶需要有狀態 而HTTP本身是無狀態協議
    2. 需要有其他方式實現status狀態, 並創建session會話, 把多個請求對應到同個用戶
        1. 在URL 中鑲入訊息
        2. 在表單使用隱藏文本框
        3. 使用cookies
    3. 通常web應用程序會設置在不同於服務器的主機, web應用程序只接收服務器訊息, 方便分開更新和管理
    4. web應用程序儲存訊息
        1. 可以利用實現狀態的三種方式
        2. HTML5新增LocalStorage
        3. 儲存的訊息是允許被更改的, 服務器不應該盲目相信這些訊息
        4. 
2. cookies
    1. 服務器可以請求user agent儲存一段cookie 字串以發起會話
    2. 兩端都可以終止會話, 只需要刪除cookies 即可
        1. 服務器只要更改到期時間就可以刪除user agent的cookies
        2. user agent會提供刪除cookies 的方式
    3. cookies 是以鍵值對方式儲存
        1. 服務器會把"Set-Cookie"包含在HTTP 響應頭回傳給user agent, 可以有多個"Set-Cookie"
            - Set-Cookie: USER=foo;
        2. user agent下次請求會包含"Cookie"傳送給伺服器
            - Cookie: USER=foo;
    4. cookie 屬性
        1. cookie也可以包含多個屬性
            1. path
            2. domain
            3. expires
            4. HttpOnly
            5. secure
    5. 範例
        1. 用curl向www.google.com發送請求
        2. google回應包含多個"Set-Cookie"
            1. ```Set-Cookie:NID=67=bs1l(...省略);expire=Sat, 27-Nov-2021 16:11:12 GMT;path=/;domain=.google.com; HttpOnly```
            2. "NID=67=bs1l(...省略)": 服務器提供的cookie字串, 通常用來辨識用戶身分發起會話
            3. "expire=...": cookie 到期時間
            4. "path=/": 瀏覽器會把cookie 使用在所有"www.google.com/"的子路徑
            5. "domain=.google.com": 瀏覽器也會把cookie 使用在所有.google.com的域名, 例如drive.google.com
            6. "HttpOnly": 安全用途, 代表這段cookie不予許使用JavaScript代碼訪
    6. cookie工具
        1. Python: requests
        2. Chrome: EditThisCookie
        3. Firefox: Cookie-Editor
3. 表單隱藏文本框
    1. 在HTML 表單中`<input type="hidden" value="foobar">`
    2. 此標籤不會顯示在瀏覽器中, 但會被一起回傳
    3. 多用於Captcha人機驗證和CSRF保護
    4. 可以在瀏覽器開發者工具輕易更改, 或直接作為HTTP 主體以cURL傳送
4. URL 參數
    1. 某些服務器會直接使用URL 參數
    2. 可以直接在URL 修改
5. Referer
    1. HTTP 請求頭, 會自動回傳當前的URI
    2. Referer實際上應該拼寫成Referrer
    3. 有些服務器會用Referer 來判斷請求是否是從可信任的位置發送
    4. 可以以cURL傳送修改請求頭來傳送請求
## U6M3 frontend backend
1. 前端後端
    1. HTML 表單輸入驗證
        1. HTML5 有內建的屬性可以使用
            1. required
            2. type=email
            3. pattern
        2. 也可以使用JavaScript 自訂
        3. 以上都是在瀏覽器(前端)進行, 也就是可以被繞過
        4. 驗證應該在後端同樣進行
2. ASP
    1. 微軟開發的後端語言, 常和HTML混寫
    2. 範例
        ```
        <% strName = Request.Querystring("Name") IF strName<> "" Then% >
        <b>Welcome!</b>
        <% Response.Write(strName) Else %>
        <b>You didn't provide a name</b>
        ```
3. PHP
    1. 專為web 設計的語言
    2. 開源且被廣泛使用, 但也出現過不少安全問題
    3. 範例
        ```html
        <!DOCTYPE html>
        <html>
            <head>
                <title>PHP</title>
            </head>
            <body>
                <?php echo '<p>Hello World</p>'; ?>
            </body>
        </html>
        ```
    4. 特性
        1. 字符串變量替代
        ```
        <?php
        $juice = "apple";
        echo "He drank some $juice";
        $juices = array("apple", "orange");
        echo "He drank some $juices[0]"
        ```
        2. 動態文件包含
