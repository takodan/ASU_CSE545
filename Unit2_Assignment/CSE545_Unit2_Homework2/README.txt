# Part 0 smart hacker
1. 已安裝Git for Windows, 使用Git Bash
2. gpg --full-generate-key: 按步驟生成公私鑰
3. cat hacker.txt | gpg --output hacker.txt.asc --clearsign: 生成clearsign簽名文件
4. gpg --import <filename>: 匯入公鑰
5. gpg -r <email> --encrypt -a hacker.txt.asc: 生成ascii-armored加密
6. gpg -a --export <email>: 匯出ascii-armored公鑰


# Part 1 ssh
1. 使用 PuTTY Key Generator生成SSH金鑰

# Part 2 badcrypt
1. 查看gz文檔得知Header, Footer, 自行生成gz文件, 以xxd -b觀察得知Header後的bytes可能會是原始檔名secretfile.txt
2. 取得bytes和ASCII字母部分做XOR, 嘗試得到和原始檔名相同組合的ASCII, 以取得密鑰
3. 嘗試復原位移取得原始檔名相同的ASCII, 以取得位移量
4. 復原檔案並解壓縮