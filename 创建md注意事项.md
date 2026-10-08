开头必须以：
chapters: true
chapDelim: "\u002d"
numberSections: false
secHeaderDelim: " "
eqnLabels: arabic
autoEqnLabels: false
tableEqns: true
eqnBlockInlineMath: true
eqnIndexTemplate: "($$i$$)"
eqnPrefixTemplate: "公式($$i$$)"
figureTitle: "图"
figPrefix: ["图", "图"]
figIndexTemplate: "$$i$$"
tableTitle: "表"
tblPrefix: ["表", "表"]
tblIndexTemplate: "$$i$$"
titleDelim: " "

作为yaml配置块。

正文中最多四级标题，最重要的作为章节，设为一级标题。

正文中的段落，只能是标准的段落，不能出现任何有序列表、无序列表、引用片段、分割线等。需要列表的时候，也不能以有序列表的格式，只能是普通的段落，里面用普通数字标号。

不要随意设置黑体加粗的文本。

各种段落不要有任何缩进。

章节内的所有公式，如果不是行内公式，是需要单行居中展示的公式，必须参考以下格式设置以便于完成自动编号和交叉引用（如果需要引用）：



$$ R_g = asfasdfsdafsdafdsR_{g,T}+R_{g,jksahfkahfkjhaskfhsdjR} $$ {#eq:rg_total}

收发站总群距离如[@eq:rg_total]所示。

$$ R_g = asfasdfsdafsdafdsR_{g,T}+RKJHJKGJGJ_{g,jksrtrsetertherjkaflkhsdkjfhkjshgakshfhwekjrthwkjhqwkhekrjthwjsahfkahfkjhaskfhsdjR} $$ {#eq:rg_total1}

收发站总群距离如[@eq:rg_total1]所示。

这里要注意：类似 {#eq:rg_total1}这样的标签要在公式标记$$的外面末尾。

图片也是同理：

![图注文字内容](Pictures/Camera Roll/微信图片_20230801152751.jpg){#fig:geo-model}

此处注意：图注文字内容中不要再出现 “图1 ”这类的东西了。
错误示范：

![图5 校准航迹：先验参考航迹与未校准雷达航迹](fig1_calibration_ck.png){#fig:calib_track}

正确示范：![校准航迹：先验参考航迹与未校准雷达航迹](fig1_calibration_ck.png){#fig:calib_track}

还有：如果出现连续多行都是公式，而且是不同编号的（互相独立的），务必在行间插入一行<div>&#8203;</div>

举例：

$$R_{g,k}^{corr}=R_{g,k}^{obs}-\widehat{\Delta R}_{sync},\qquad
\phi_{az,k}^{corr}=\phi_{az,k}^{obs}-\widehat{\Delta\theta}$$ {#eq:eq032}

<div>&#8203;</div>

$$r_k=\sqrt{\left(\frac{R_{g,k}^{corr}}{2}\right)^2-4\hat h^2},\qquad
x_k=r_k\sin\phi_{az,k}^{corr},\qquad
y_k=r_k\cos\phi_{az,k}^{corr}$$ {#eq:eq033}



还有：所有公式都不允许有\bar和任何形式的空格。\bar应该用\overline代替。所有形式的空格如\,，\quad，\qquad，反斜杠空格 \ ，以及半角空格用于分隔公式元素等，都不允许出现。根本不必空格分割。

具体细则（务必遵守）：

1. 禁止的空格形式（全部要删除）：
   - \bar：一律用 \overline 代替（\bar s → \overline s；注意 \overline s、\overline{s^2} 里用花括号时，内容前不要再写 \bar）。
   - 反斜杠空格 \ （即 backslash 紧跟一个空格，如 "a \ b"、"10\ km"）：一律删除。表格单元格、行内公式、独立公式里出现的都要删。
     - 反例：$(300,\ 10,\ 5.0)$、$10\ \text{km}$、$(720.5,\ 284.7)$、\rho_c\in\{450,600,750,900\}\ \text{km}
     - 正例：$(300,10,5.0)$、$10\text{ km}$、$(720.5,284.7)$、\rho_c\in\{450,600,750,900\}\text{ km}
   - \quad、\qquad：一律删除，用普通逗号 "," 分隔并列子式即可。
     - 反例：$$R=R_1,\qquad R=R_2$$、$$a=\frac{1}{x},\qquad b=\frac{1}{y}$$
     - 正例：$$R=R_1, R=R_2$$、$$a=\frac{1}{x}, b=\frac{1}{y}$$（逗号后普通半角空格可保留，这不是"公式内的空格命令"，属于正常标点；但绝不能用 \、\quad、\qquad）
   - \;、\:、\! 等其它显式间距命令：同样禁止，删除后直接拼接或改用普通逗号。

2. 受控例外（不属于"禁止空格"，允许保留，但不要误删）：
   - 矩阵内部用于换行的 \\ （bmatrix / pmatrix / cases 等环境里的行分隔符，形如 "…& -1\ σ_R\ 0\\[6pt] 0&0&…"）：这是 LaTeX 矩阵语法的行换行，不是"分隔元素用的空格"，必须保留。
   - 在正文中作为示例去解释某个命令本身时（例如用文字说明"上标 $\hat{\ }$ 表示估计量"里的 \ ），属于元说明、不是参与排版的公式内容，允许保留。
   判定原则：凡是"用于在两个数学元素之间塞间距"的 \、\quad、\qquad、\; 等，一律删；凡是"矩阵换行"或"文字里举例说明某命令"的，保留。

3. 自查方法：搜 \ （反斜杠加空格）、\quad、\qquad、\;、\, 与 \bar，逐一确认是否属于上述两类受控例外，否则全部删除；同时确认 \bar 已全部改成 \overline。

还有：所有表格都必须要按照下面格式书写：



| 参数 | 真值 | 估计值 | 绝对误差 | 相对误差 |
| ---- | ---- | ------ | -------- | -------- |
|      |      |        |          |          |

| 电离层等效虚高 $h/\mathrm{km}$ | 300.000 | 298.877 | $-1.123$ | 0.374% |
| ------------------------------ | ------- | ------- | -------- | ------ |
|                                |         |         |          |        |

| 时间同步距离偏置 $\Delta R_{sync}/\mathrm{km}$ | 10.000 | 13.590 | $+3.590$ | 35.895% |
| ---------------------------------------------- | ------ | ------ | -------- | ------- |
|                                                |        |        |          |         |

| 方位系统偏差 $\Delta\theta/^\circ$ | 5.000 | 4.799 | $-0.201$ | 4.021% |
| ---------------------------------- | ----- | ----- | -------- | ------ |
|                                    |       |       |          |        |



 : 参数估计结果（实施例一） {#tbl:ex1}



表格格式解读：在常规表格下，先空一行，然后添加“:表格注解标题{#tbl:ex1}”
必须是空一行，然后有个英文冒号，再加上类似的自动编号标签。