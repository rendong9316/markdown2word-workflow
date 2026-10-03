chapters: true
chapDelim: "\u2011"
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



上文为md文档开头yaml块配置内容。先得到写好的md文档。

然后使用pandoc运行pandoc test.md -o 输出15.docx --filter pandoc-crossref --reference-doc=模板1.docx

其中：模板1为根目录下的模板（不能改动），各种内容配置个大概。

转换出来之后，运行python fix_plus.py（其中需要根据文档名称配置） ，用来将公式表格补充左侧空白列。

但是这样之后，唯一不足就是公式字体还是默认的。这时候全局调整公式字体：公式->e^x转换右下角的放大框进入公式选项，改变默认字体为XITS。

之后：全选->字体设置为XITS->全选->字体设置为新罗马。这样就做到公式全为特别像新罗马的xits，其他字母都是标准新罗马。

之后：宏处理：进入开发-vb，输入脚本：批量设置三线表的宏.txt，运行后会把所有非单行表格设为三线表。但是会把一部分多行公式也处理，需要手动核查。

