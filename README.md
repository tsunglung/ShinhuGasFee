<a href="https://www.buymeacoffee.com/tsunglung" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="30" width="120"></a>

Home assistant support for Shinhu Gas Fee

The method was provided by [Jason Lee](https://www.dcard.tw/@jas0n.1ee.com).

***User the integration by your own risk***

## Install

You can install component with [HACS](https://hacs.xyz/) custom repo: HACS > Integrations > 3 dots (upper top corner) > Custom repositories > URL: `tsunglung/ShinhuGasFee` > Category: Integration

Or manually copy `shinhugas_fee` folder to `custom_components` folder in your config folder.

Then restart HA.

# Setup

You need to grab two tokens.

**1. Basic steps for grabbing**

1. Open the development tools (use Google chrome/Microsoft Edge) [Crtl+Shift+I / F12]
2. Open the Network tab
3. Open the [Shinhu Gas Fee Web site](http://www.shinhugas.com.tw/Default.aspx), Enter the User name and password.
4. Search for "member" (for me only one itemes shows up, choose the first one)
5. Go to "headers" -> "from data"
6. copy the 1168 characters like "\wXXXXXXXXXXXX....=" in the field "\__VIEWSTATE:"  (mark with a mouse and copy to clipboard)
7. copy the 8 characters like "\wXXXXXXXXXXXX....." in the field "\__VIEWSTATEGENERATOR:"  (mark with a mouse and copy to clipboard)

# Config

![grabbing](grabbing.png)

**2. Please use the config flow of Home Assistant**


1. With GUI. Configuration > Integration > Add Integration > ShinhuGas Fee
   1. If the integration didn't show up in the list please REFRESH the page
   2. If the integration is still not in the list, you need to clear the browser cache.
2. Enter Gas ID without dash.
3. Paste the viewstate and generator token, validation toekn into the indicated field, all fields are Required.

# Notice
The viewstate and generator tokens will expired after hours. If you saw the https_result is 403, you need get the new tokens again.
Then got to Configuration > Integration > ShinhuGas Fee > Options, enter the info of tokens.
