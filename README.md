## start
* Fiddler Classic 抓包夸克浏览器签到页（手机安装fiddler证书后，同一网络环境，设置代理为电脑ip与fiddler端口8888）

> [!GET] 
>
> ```json
> https://drive-m.quark.cn/1/clouddrive/capacity/growth/info?__t=1727427154544&sign_cyclic=true
> &kps=AASiFHJ8BL2%2BH0WI9AlgfsSNj8tIhPNUSTBG9qW%2FSdcEX%2Bhkyk7PjOrGSsZCF54cAu8ne%2BUGkIE2w7jsXH7ZnMUUtfr1sHHJduOGNjDeHiHvSA%3D%3D
> &sign=AARdsyNJXV3mw1Mj3aXX0PlsWikTh8fphI%2B6hmwIVao84zyyxvflFmT3yr4nQV9O7Vc%3D
> &vcode=1727427154531
> &uc_param_str=dnfrpfbivessbtbmnilauputogpintnwmtsvcppcprsnnnchmicckp&dn=62793693876-c3bf4fbb&fr=android&pf=3300&bi=35937&ve=6.1.8.242&ss=393x857&ni=bTkwBKYy1OJeqHB%2Bu4t3PEo0cWXKex7VVxB2EG%2F4O9%2Fnv%2BM%3D&la=zh&ut=AAObwLw3yjXjUgtnEUCuj%2BC0SH8cz0KfnhBcpiNDj1v%2BMQ%3D%3D&nt=5&nw=0&mt=UQMBLHlLPIv9TQKSMjtotKlvYYc1IIzC&sv=release&pc=AASZtg30J6cEZGl0meB9hj0EXmtm8MuBTzuGEVLqhTFBUDEr7mf7YNH5zAJENvF6fkdFZGvZjca6cwNWjrEPTJA8&pc=AASZtg30J6cEZGl0meB9hj0EXmtm8MuBTzuGEVLqhTFBUDEr7mf7YNH5zAJENvF6fkdFZGvZjca6cwNWjrEPTJA8&pr=ucpro&sn=2409-62793693876-b8a316df&ch=kk%40store&mi=M2006J10C&kp=AASiFHJ8BL2%2BH0WI9AlgfsSNj8tIhPNUSTBG9qW%2FSdcEX%2Bhkyk7PjOrGSsZCF54cAu8ne%2BUGkIE2w7jsXH7ZnMUUtfr1sHHJduOGNjDeHiHvSA%3D%3D
> ```


> [!CAUTION]
> 
> ⛔️⛔️⛔️ 注意！资源不会每时每刻更新，**严禁设定过高的定时运行频率！** 以免账号异常或给夸克服务器造成不必要的压力。雪山崩塌，每一片雪花都有责任！

> [!TIP]
>
> 受 [@BNDou](https://github.com/BNDou) 提示和方法借鉴，**已适配新的签到方式**。
>
> 你需要手机端访问签到页，抓包 <u>/1/clouddrive/capacity/growth/info</u> 请求的 kps, sign, vcode 三个参数，**纯签到只需这三个参数即可！** 转存号可附在 cookie 的最后，如：
>
> > cookie=`;kps=123456789&sign=123456789&vcode=123456`
>
> 如果你纯粹需要签到功能，建议移步 @BNDou 的 [Auto_Check_In](https://github.com/BNDou/Auto_Check_In/blob/main/checkIn_Quark.py) 项目，更聚焦一些。

> [!NOTE]
> 
> 因不想当客服处理各种使用咨询，即日起 Issues 关闭，如果你发现了 bug 、有好的想法或功能建议，欢迎通过 PR 和我对话，谢谢！

> [!important]
>
> 更改的文件
>
> * `utils/notify.py` 通知的环境变量可设置成空串代替（取消）默认值
>
> * `.env` 环境变量（github环境变量）
>
>   * ```json
>     COOKIE_QUARK="user=移动号;kps=AASiFHJ8BL2%2BH0WI9AlgfsSNj8tIhPNUSTBG9qW%2FSdcEX%2Bhkyk7PjOrGSsZCF54cAu8ne%2BUGkIE2w7jsXH7ZnMUUtfr1sHHJduOGNjDeHiHvSA%3D%3D;sign=AARdsyNJXV3mw1Mj3aXX0PlsWikTh8fphI%2B6hmwIVao84zyyxvflFmT3yr4nQV9O7Vc%3D;vcode=1727427154531"
>     ```
>
> * `accounts.json` 通知邮件的账号密码（github秘密）
>
>   * ```json
>     [
>       {"SMTP_SERVER": "smtp.qq.com:465", "SMTP_SSL": "true", "SMTP_EMAIL": "@qq.com","SMTP_PASSWORD": "","SMTP_NAME": "夸克自动登录脚本通知（自己发送给自己）"}
>     ]
>     ```
>
> * `checkIn_Quark.py` 无异常则每周一发送通知，异常直接发送通知（适配accounts.json、.env文件）
>
> * `.github/workflows/login.yaml` Github Action 自动执行工作流的配置文件
>
>   * `cron: "0 9 * * *"  # 每1天运行一次`
>
>   * ```yaml
>     run: |
>       python checkIn_Quark.py
>     ```

### action配置

* 配置环境变量，用户登录签到

> [New repository variable](https://github.com/qingdog/Auto_Check_In/settings/variables/actions/new)
>
> | Name           | Value                                                        | Last updated | Actions |
> | -------------- | ------------------------------------------------------------ | ------------ | ------- |
> | `COOKIE_QUARK` | user=移动号;kps=AASiFHJ8BL2%2BH0WI9AlgfsSNj8tIhPNUSTBG9qW%2FSdcEX%2Bhkyk7PjOrGSsZCF54cAu8ne%2BUGkIE2w7jsXH7ZnMUUtfr1sHHJduOGNjDeHiHvSA%3D%3D;sign=AARdsyNJXV3mw1Mj3aXX0PlsWikTh8fphI%2B6hmwIVao84zyyxvflFmT3yr4nQV9O7Vc%3D;vcode=1727427154531 | yesterday    |         |


* 配置密钥，异常时用于发送qq邮件

> Actions secrets and variables
>
> Repository secrets
>
> [New repository secret](https://github.com/qingdog/Auto_Check_In/settings/secrets/actions/new)
>
> | Name            | Last updated  | Actions |
> | --------------- | ------------- | ------- |
> | `ACCOUNTS_JSON` | 3 minutes ago |         |
>
> ```json
> [
>   {"SMTP_SERVER": "smtp.qq.com:465", "SMTP_SSL": "true", "SMTP_EMAIL": "@qq.com","SMTP_PASSWORD": "","SMTP_NAME": "夸克自动登录脚本通知（自己发送给自己）"}
> ]
> ```



<!--

 * @Author       : BNDou
 * @Date         : 2022-10-30 19:12:57
 * @LastEditTime: 2024-08-05 03:12:06
 * @FilePath: \Auto_Check_In\README.md
 * @Description  :
-->

# Auto_Check_In

> 每日自动签到集合

~~小米社区~~ | 掌飞签到 | 掌飞购物 | 掌飞寻宝 | speed大乐透 | 夸克网盘 | 人人视频 | 恩山论坛 | ~~必应搜索~~

## 更新日志
- 2024-08-05 新增 speed端游-周末大乐透 系列工具
- 2024-07-15 修复 夸克网盘自动签到
- ~~2024-07-14 修复 【测试版】夸克网盘自动签到~~
- 2024-06-12 新增 掌飞扫码登录 获取cookie关键属性(参数只适用于签到脚本)
- 2024-05-10 新版掌飞V4 签到已更新
- 新版掌飞V3 签到、掌飞购物、掌飞寻宝、掌飞开金丝篓已修复

## 青龙部署

1. 拉库指令（拉库失败请自行添加代理）

```
ql repo "https://github.com/BNDou/Auto_Check_In.git" "checkIn_" "backUp" "utils" "main" "py"
```

2. 根据“**_代码文件头部注释_**”或者“**_运行提示_**”添加对应的“**_环境变量_**”

## 捐赠支持，用爱发电

<a href="https://github.com/BNDou/"><img height="200px" src="https://cdn.bndou.eu.org/gh/BNDou/Auto_Check_In/readme/donate.jpg" /></a>

您的赞赏，激励我更好的创作！谢谢~

个人维护开源不易，本项目的开发与维护全都是利用业余时间。

如果觉得我写的程序对你小有帮助，或者

想投喂 `雪王牌柠檬水 * 1`

那么上面的微信赞赏码可以扫一扫呢

赞赏时记得留下【`GitHub昵称`】和【`留言`】

### 捐赠榜

| 用户 | 平台 |
|:---:|:---:|
| Citizen Z | WeChat |
| 钟情于 | WeChat |
| M | WeChat |
| [Struggle-best](https://github.com/Struggle-best) | WeChat |
| [Machae1](https://github.com/Machae1) | WeChat |
| [AfanChang](https://github.com/AfanChang) | WeChat |
| [1983shake](https://github.com/1983shake) | WeChat |

## 技术鸣谢
- [Chiupam](https://github.com/chiupam)
- [Cp0204](https://github.com/Cp0204)

## 免责声明
- 这里的脚本只是自己学习 python 的一个实践。
- 仅用于测试和学习研究，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。
- 仓库内所有资源文件，禁止任何公众号、自媒体进行任何形式的转载、发布。
- 该项目的归属者对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害。
- 间接使用脚本的任何用户，包括但不限于建立 VPS 或在某些行为违反国家/地区法律或相关法规的情况下进行传播, 该项目的归属者对于由此引起的任何隐私泄漏或其他后果概不负责。
- 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。
- 任何以任何方式查看此项目的人或直接或间接使用该 Python 项目的任何脚本的使用者都应仔细阅读此声明。 该项目的归属者保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或 Python 项目的规则，则视为您已接受此免责声明。

---

[![](https://komarev.com/ghpvc/?username=BNDou&&label=Views "To Github")](https://github.com/BNDou/)
