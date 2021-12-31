<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

Home assistant for 欣湖天然氣

此方法是由強者 [Jason Lee](https://www.dcard.tw/@jas0n.1ee.com) 所提供.

使用本整合, 必須由你承擔任何風險.

## 安裝

你可以使用 [HACS](https://hacs.xyz/) 來安裝此整合元件. 步驟如下 custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/ShinhuGasFee` > Category: Integration

或是手動複製 `shinhugas_fee` 到你的設定資料夾 (像是 /config) 下的 `custom_components` 目錄.

然後重新啟動 HA.


# 前置作業

你必須取得 VIEWSTATE 令牌. 如果你遇到 http_result 500 的問題，你必須要重新取得令牌，因為欣湖網站已經改版。

**1. 取得步驟**

1. 開啟開發者工具 (使用 Google chrome/Microsoft Edge) [Crtl+Shift+I / F12]
2. 打開 Network 頁面
3. 打開 [欣湖天然氣](http://www.shinhugas.com.tw/Default.aspx) 的網站, 登入你的帳號密碼.
4. 在 filter 欄位, 搜尋 "member" (可能會有多個項目，選擇第一個)
5. 移動 "headers" -> "from data"
6. 複製在 \__VIEWSTATE: 欄位下, 一段很長的字串, 像 "GA1adsm2S50n;2xlmbbG9....=" (使用滑鼠並複製到剪貼簿, 或是記事本)
7. 如果，你想要有自報度數的功能。你可以點擊 [自報度數](http://www.shinhugas.com.tw//自報度數.htm) 的按鈕，自報一次天氣然度數。
   移動 "headers" -> "from data" 後，找到 \__VIEWSTATE (636 字元) 複製到記事本。

![grabbing](grabbing.png)

# 設定

**2. 使用 Home Assistant 整合**

1. 使用者介面, 設定 > 整合 > 新增整合 > ShinhuGas Fee
   1. 如果整合沒有出在清單裡，請重新整理網頁
   2. 如果重新整理網頁後，整合還是沒有出在清單裡，請您清除瀏覽器的快取
2. 輸入欣湖天然氣號
3. 貼上 VIEWSTATE 和 VIEWSTATEGENERATOR 令牌到指定的欄位, 所有的欄位都要填入。
4. 如果，你想要有自報度數的功能，可以填入 自報度數的 VIEWSTATE。

# 自報度數

1. 到 HA 的開發工具 > 服務
2. 選擇 shinhugas_fee.gas_upload_usage
3. 選擇你的 實體 (binary_sensor.shinhu_gas_upload_usage_123456789)
4. 在服務資料填入
   usage: 5421 （你要自報的天然氣度數)
5. 按下執行服務，如果自報度數正常，binary_sensor.shinhu_gas_upload_usage_123456789 就會變成 True
6. 你也可以在 binary_sensor.shinhu_gas_upload_usage_123456789 實體的屬性得知自報度數結果 (https result) 和時間。

# Notice.
在 VIEWSTATE 和 VIEWSTATEGENERATOR 令牌如果過期. 你在感測器的屬性看到 `Https result` 是 403, 你必須重新再取得一次新的 VIEWSTATE 和 VIEWSTATEGENERATOR 令牌.
然後到 設定 > 整合 > ShinhuGas Fee > 選項, 輸入新的 VIEWSTATE 和 VIEWSTATEGENERATOR 令牌.

打賞

|  LINE Pay | LINE Bank | JKao Pay |
| :------------: | :------------: | :------------: |
| <img src="https://github.com/tsunglung/OpenCWB/blob/master/linepay.jpg" alt="Line Pay" height="200" width="200">  | <img src="https://github.com/tsunglung/OpenCWB/blob/master/linebank.jpg" alt="Line Bank" height="200" width="200">  | <img src="https://github.com/tsunglung/OpenCWB/blob/master/jkopay.jpg" alt="JKo Pay" height="200" width="200">  |