开头必须以：
chapters: true
chapDelim: "\u2011"
numberSections: true
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

正文中最多三级标题，最重要的作为章节，设为一级标题。

正文中的段落，只能是标准的段落，不能出现任何有序列表。需要列表的时候，也不能以有序列表的格式，只能是普通的段落，里面用普通数字标号。

不要随意设置黑体加粗的文本。

各种段落不要有任何缩进。

章节内的所有公式，如果不是行内公式，是需要单行居中展示的公式，必须参考以下格式设置以便于完成自动编号和交叉引用（如果需要引用）：



$$ R_g = asfasdfsdafsdafdsR_{g,T}+R_{g,jksahfkahfkjhaskfhsdjR} $$ {#eq:rg_total}

收发站总群距离如[@eq:rg_total]所示。

$$ R_g = asfasdfsdafsdafdsR_{g,T}+RKJHJKGJGJ_{g,jksrtrsetertherjkaflkhsdkjfhkjshgakshfhwekjrthwkjhqwkhekrjthwjsahfkahfkjhaskfhsdjR} $$ {#eq:rg_total1}

收发站总群距离如[@eq:rg_total1]所示。



图片也是同理：

![图注文字内容](Pictures/Camera Roll/微信图片_20230801152751.jpg){#fig:geo-model}