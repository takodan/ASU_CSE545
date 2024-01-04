## U5M1 棧
1. 函數的臨時儲存區域, 大部分CPU都是基於棧的設計
2. 先進後出, 後進先出
3. 棧指針: 棧頂位置, 低於棧頂的值為垃圾數據, 存在rsp 中
4. 範例1
    1. rax:0xa, rbx:0x0, rsp:0x1000
    2. push rax
        1. rsp = rsp-8 = 0xfff8
        2. 0xfff8 = rax = 0xa
    3. pop rbx
        1. rbx = 0xfff8 = 0xa
        2. rsp = rsp+8 = 0x10000
5. 幀指針(機指針): 幀棧的起始位置, 可以配合偏移計算變數位置, 有時存在rbp 中
    1. 範例2
    ```c
    int main()
    {
        int a;
        int b;
        float c;
        a = 10;
        b = 100;
        c =10.45;
        a = a + b;
        return 0;
    }
    ```
    2. 編譯器偽代碼
    ```
     a @ rbp + A # a存放在rbp 加偏移A 的位置
     b @ rbp + B
     c @ rbp + C

     mem[rbp+A] = 10 # 記憶體位置rbp+A 的值改為10
     mem[rbp+B] = 100
     mem[rbp+C] = 10.45

     mem[rbp+A] = mem[rbp+A] + mem[rbp+A] # 記憶體位置rbp+A 的值改為rbp+A和rbp+B 位置相加
    ```
    3. 實際執行可能的匯編碼
    ```
    a @ rbp - 0xc # 棧的記憶體位置由上往下, int 和float 的大小都是4, 所以分別對應這些位置
    b @ rbp - 0x8
    c @ rbp - 0x4

    mov rbp, rsp # 把rsp 放到rbp 中
    mov dword ptr [rbp-0xc], 0xa # 把值0xa放到記憶體位置[rbp-0xc]
    mov dword ptr [rbp-0x8], 0x64
    movss xmm0, dword ptr [rip+0xa0] # 把浮點數表達放入xmm 寄存器(這裡用到x86-64的rip相對循址)
    movss dword ptr [rbp-0x4], xmm0 # 把xmm 中的浮點數放入記憶體位置[rbp-0x4]
    mov eax, [rbp-0x8] # eax:0x64
    add [rbp-0xc], eax # 0xa + 0x64
    ```
    4. 棧針變化
        1. rax: , rsp: 0x10000,rbp:
        2. mov rbp, rsp
            - rax: , rsp: 0x10000, rbp: 0x10000
        3. mov [rbp-0xc], 0xa
            - rax: , rsp: 0x10000, rbp: 0x10000
            - [rbp-0xc] = 0xFFF4 = 0xa
        4. mov [rbp-0x8], 0x64
            - rax: , rsp: 0x10000, rbp: 0x10000
            - [rbp-0x8] = 0xFFF8 = 0x64
        5. 這裡有一個Red Zone 的概念
            1. 儲存的兩個數據, 記憶體位置都在棧指針rsp:0x10000之下
            2. 一般來說這些數據會被當作類色數據
            3. 但是x86-64有在棧外保留128bytes 的紅區供函數使用
            4. 所以這兩個數據是存放在紅區之中
        6. 浮點數轉換後數據0x4127333 存到xmm0
        7. movss [rbp-0x4], xmm0
            - rax: , rsp: 0x10000, rbp: 0x10000
            - [rbp-0x4] = 0xFFFC = 0x4127333
        8. mov eax, [rbp-0x8] # eax是rax 的低四位, int只會用到4bytes, 高四位會自動清空
            - rax: 0x64 , rsp: 0x10000, rbp: 0x10000
        9. add [rbp-0xc], eax
            - rax: 0x64 , rsp: 0x10000, rbp: 0x10000
            - [rbp-0xc] = 0xFFF4 = 0x6E
6. 調用規範
    1. 函數運行時需要從記憶體和寄存器調用各種數據, 需要有規範來決定
    2. x86-64 Linux最常見的規範是"System V AMD64 ABI"
        1. 調用方
            1. 前六個數值或指針按順序存入rdi, rsi, rdx, rcx, r8, r9
            2. 其他照由右至左順序入棧
            3. 最後要把返回指令地址入棧
        2. 被調用方
            1. 如有需要
                1. 原本的幀指針(例如 rbp)入棧
                2. 分配局部變量空間(紅區不需要分配)
            2. 確保返回後棧指針回到原位置
            3. 返回值儲存在rax
    3. 範例3
        1. 
        ```c
        int callee(int a, int b)
        {
            return a + b + 1;
        }
        int main()
        {
            int a;
            a = callee(10, 40)
            return a;
        }
        ```
        2. 運作過程
            1. rip:0x555555554611 # gdb默認位置無關的二進制程序基址為0x555555554000
            2. rsp:0x7fffffffdd78 # 棧指針
            3. rbp:0x555555554630 # 執行main之前其他函數的值, main之前會有一些函數(libc start main)先進行準備工作, main結束之後會回到這函數進行清理
            4. `main`函數頭: 運行函數前的一些指令
                1. push rbp # rbp這數值之後會用到, 先保存到棧, rsp-8 = 0x7fffffffdd70
                2. mov rbp, rsp # 把rsp移動到rbp
                    - rbp = 0x7fffffffdd70
                3. sub rsp, 0x10 # 為main函數分配空間
                    - rsp = 0x7fffffffdd60
            5. 把`callee`的兩個參數值放入寄存器
                1. mov esi, 0x28
                2. mov edi, 0xa
            6. 調用`callee`
                1. call 5fa `<callee>`
                    1. `<callee>`的地址在0x5555555545fa
                    2. call 會把下一個地址推到棧上, 按照一開始的rip計算會是0x555555554628, rsp-8
                        - rsp = 0x7fffffffdd58
                    3. rip值更改到`<callee>`的地址0x5555555545fa
            7. `callee`函數頭
                1. push rbp # 0x7fffffffdd70, rsp-8
                    - rsp = 0x7fffffffdd50
                2. mov rbp, rsp # 把rsp移動到rbp
                    - rbp = 0x7fffffffdd50
                3. 無須額外分配空間
            8. 執行`callee`程式碼
                1. 類似範例1, 會用到rbp 計算位置, 儲存變數到紅區
                2. `[rbp-0x4]`儲存變數rsi, `[rbp-0x8]`儲存變數edi
                2. 把兩個位置的值分別放到rax和rdx進行計算
            9. `callee`函數尾: 結束函數回到前一個函數
                1. pop rbp # 把原本變為rsp的數值改回原本的rbp
                    - rbp = 0x7fffffffdd70
                2. ret # 把呼叫函數之前, call 的時候保存的地址傳回rip, 回到上個函數繼續執行
                    - rip = 0x555555554628
            10. 繼續`main`
                1. mov `[rbp-4]`, eax # 把上個函數的返回值放到`main`的棧幀上
                2. mov eax, `[rbp-4]` # 把暫存的值放到rax作為返回值
            11. `main`函數尾
                1. leave # 包含把rsp和rbp恢復, 因為一開始有分配控間所以rsp 也要恢復
                2. ret # 回到上個函數繼續執行
7. 棧緩衝區溢出
    1. 複製數據沒有檢查邊界, 覆蓋到棧上的其他數據, 導致段錯誤
    2. 假如覆蓋到會返回值, 也就是函數結束會返回的rip地址, 就可以劫持控制流, 執行特定的代碼 
    3. 劫持執行的代碼權限會和原本程序相同
    4. call 一個函數時, 根據調用規範
        1. 當前rip會加一後存入棧中, 以便之後返回上一個函數
        2. 當前rbp會存入棧中, rbp會被rsp的值取代以計算偏移, 函數結束也需要回復
    5. 範例4
        ```c
        #include <string.h>
        #include <stdio.h>
        void mycpy(char* str)
        {
            char foo[4];
            strcpy(foo, str);
        }
        int main(int argc, char** argv)
        {
            mycpy(argv[1]);
            printf("After");
            return 0;
        }
        ```
        1. 這次分析著重在記憶體上
            1. rsp:`0x7fffffffdd88`
            2. rbp:`0x5555555546f0`
            3. rip:`0x5555555546ac`
        2. `main`函數頭
            1. push rbp
                - rsp:`0x7fffffffdd80`
                - `0x7fffffffdd80`:`0x5555555546f0`
            2. mov rbp rsp
                - rbp:`0x7fffffffdd80` # rbp 現在是`main`棧幀起始位置
            3. sub rsp, 0x10
                - rsp:`0x7fffffffdd70` # rsp 現在是`main`棧幀結束位置, 中間分配用來存放數據
            4. mov `[rbp-0x4]`, edi # 存第一個參數argc到棧幀, argc是參數數量
            5. mov `[rbp-0x10]`, rsi # 存第二個參數argv的地址到棧幀, 這些地址指向一個數列的元素
            6. mov rax, `[rbp-0x10]` # rax放入argv值
            7. add rax, 0x8 # argv值一個佔8bytes, rax+0x8會是`argv[1]`的地址
            8. mov rax, `[rax]` # 拿rax的值作為地址取值, 得到`argv[1]`的值, 存到rax
            9. mov rdi, rax # rdi=`argv[1]`, 準備給`mycpy`使用
            10. call 68a `<mycpy>`
                - 原本的rip會加一推到棧上
                    1. - rsp:`0x7fffffffdd68`
                    2. `0x7fffffffdd68`:`0x5555555546ce`
                1. push rbp
                    - rsp:`0x7fffffffdd60`
                    - `0x7fffffffdd60`:`0x7fffffffdd80`
                2. mov rbp rsp # rbp 現在是`mycpy`棧幀起始位置
                3. sub rsp, 0x20 # rsp 現在是`mycpy`棧幀結束位置, 中間分配用來存放數據
                4. mov [rbp-0x18], rdi
                    - `0x7fffffffdd48`:`0x7fffffffe180(argv[1])`
                5. mov rdx, [rbp-0x18]
                    - rdx:`0x7fffffffe180(argv[1])`
                6. lea rax, [rbp-0x4] # `[rbp-04]`是給`char foo[4]`保留的位置
                    - rax:`0x7fffffffdd5c(foo)`
                7. mov rsi, rdx
                    - rsi:`0x7fffffffe180(argv[1])`
                8. mov rdi, rax
                    - rdi:`0x7fffffffdd5c(foo)`
                9. call 550 `<strcpy@plt>`
                    - 把`argv[1]`字串寫到`foo`
                10. 這時`(gdb) x/s 0x7fffffffe180`會顯示`argv[1]`的字串
                12. `(gdb) x/19bx 0x7fffffffe180` 會依照字節方式顯示
                13. `foo`只有四個字節, 所以拷貝會溢出
                14. `0x7fffffffdd5c``0x7fffffffdd60``0x7fffffffdd68`都會被覆蓋
                15. `0x7fffffffdd60`是要返回的rbp
                16. `0x7fffffffdd68`是要返回的rip
                17. 後面運行leave和ret會擺錯誤數據寫回
                18. 因為rip不是有效的內存空間, 會出現"Segmentation Fault"段錯誤
    6. 一些gdb
        1. `gdb ./file` 以gdb開啟檔案
        2. `(gbd) r argv` 以參數開始運行檔案
        3. `(gbd) info registers` 顯示寄存器資訊
    7. C語言初始設計沒有考慮到緩衝區溢出攻擊問題, 許多函數都有此漏洞
        1. 例如`get()`,`strcpy()`,`strcat()`,`sprintf()`,`vsprintf()`
        2. 之後有設計許多安全版本的函數
## U5M2 利用溢出
1. 目標是控制rip
2. 假設有一個函數位於`0x400990`,只要用`90 09 04 00 00 00 00 00`覆蓋儲存的rip(因為是小端序)
3. 程式中不一定有我們想執行的函數, 可以寫入Shellcode來執行特定代碼

