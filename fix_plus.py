import copy
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============ 可调参数：三列宽度比例 ============
# 顺序：新空列、原来的第1列（文字列）、原来的第2列（公式列）
# 三者之和建议为 1.0；脚本会自动换算成 twips
COL_RATIOS = [0.10, 0.80, 0.10]

# 表格总宽占"纸张可用宽度"的比例。1.0 = 铺满正文区
TOTAL_WIDTH_RATIO = 1.0

# 左右再留一点额外安全边距（厘米），一般 0
SAFETY_MARGIN_CM = 0.0

# 页面尺寸缺失时的兜底（twips）
DEFAULT_PAGE_WIDTH_TWIPS = 11906   # A4 宽 21cm
DEFAULT_MARGIN_TWIPS     = 1440    # 默认 2.54cm

# 常用标签缓存
M_OMATH     = qn('m:oMath')
M_OMATHPARA = qn('m:oMathPara')
W_TC        = qn('w:tc')
W_TCPR      = qn('w:tcPr')
W_GRIDSPAN  = qn('w:gridSpan')
W_VMERGE    = qn('w:vMerge')
W_TR        = qn('w:tr')
W_P         = qn('w:p')
W_GRIDCOL   = qn('w:gridCol')
W_TBLPR     = qn('w:tblPr')
W_TBLW      = qn('w:tblW')
W_TBLLAYOUT = qn('w:tblLayout')


def cm_to_twips(cm: float) -> int:
    # 1 inch = 1440 twips, 1 cm ≈ 567 twips
    return int(round(cm * 567))


def set_gridcol_width(gridCol, twips: int):
    gridCol.set(qn('w:w'), str(twips))


def set_cell_width(tc, twips: int):
    """给 <w:tc> 写 <w:tcPr><w:tcW w:w=.. w:type='dxa'/>"""
    tcPr = tc.find(W_TCPR)
    if tcPr is None:
        tcPr = OxmlElement('w:tcPr')
        tc.insert(0, tcPr)
    tcW = tcPr.find(qn('w:tcW'))
    if tcW is None:
        tcW = OxmlElement('w:tcW')
        tcPr.append(tcW)
    tcW.set(qn('w:w'), str(twips))
    tcW.set(qn('w:type'), 'dxa')


def set_table_width(tblEl, twips: int):
    """设置表格总宽度（配合 fixed 布局，让三列总宽一致）"""
    tblPr = tblEl.find(W_TBLPR)
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tblEl.insert(0, tblPr)
    tblW = tblPr.find(W_TBLW)
    if tblW is None:
        tblW = OxmlElement('w:tblW')
        tblPr.append(tblW)
    tblW.set(qn('w:w'), str(twips))
    tblW.set(qn('w:type'), 'dxa')


def set_fixed_layout(tblEl):
    """把表格布局改为 fixed，列宽才会被尊重"""
    tblPr = tblEl.find(W_TBLPR)
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tblEl.insert(0, tblPr)
    layout = tblPr.find(W_TBLLAYOUT)
    if layout is None:
        layout = OxmlElement('w:tblLayout')
        tblPr.append(layout)
    layout.set(qn('w:type'), 'fixed')


# ============ 纸张可用宽度计算 ============

def _len_to_twips(length_obj, default_twips: int) -> int:
    """python-docx 的 Length 对象转 twips；为 None 时回退默认值"""
    if length_obj is None:
        return default_twips
    return length_obj.twips


def get_usable_width_twips(section, safety_cm: float = 0.0) -> int:
    """返回正文区可用宽度（twips）= 页宽 - 左边距 - 右边距 - 安全边距"""
    pw = _len_to_twips(section.page_width,    DEFAULT_PAGE_WIDTH_TWIPS)
    lm = _len_to_twips(section.left_margin,   DEFAULT_MARGIN_TWIPS)
    rm = _len_to_twips(section.right_margin,  DEFAULT_MARGIN_TWIPS)
    usable = pw - lm - rm - cm_to_twips(safety_cm)
    return max(usable, 1000)   # 兜底，避免负数或过小


def distribute_widths(usable_twips: int,
                      ratios,
                      total_ratio: float = 1.0):
    """
    按比例把可用宽度分给各列：
      - 先按 ratios 分配
      - 舍入误差全部塞给最宽的一列（视觉影响最小）
      - 保证 sum(widths) == target_total
    """
    target_total = int(round(usable_twips * total_ratio))
    widths = [int(round(target_total * r)) for r in ratios]
    diff = target_total - sum(widths)
    # 找最宽的一列的索引
    widest = max(range(len(widths)), key=lambda i: widths[i])
    widths[widest] += diff
    return widths


# ============ 判断逻辑 ============

def cell_has_math(cell) -> bool:
    tc = cell._tc
    return bool(tc.findall('.//' + M_OMATH) or tc.findall('.//' + M_OMATHPARA))


def table_has_math(tbl) -> bool:
    return any(cell_has_math(c) for row in tbl.rows for c in row.cells)


def is_formula_table(tbl) -> bool:
    """
    真正的公式表格判定：
      1) 一定是一行两列（普通表格基本不会只有一行）
      2) 必须包含 OMML 公式
    """
    try:
        n_rows = len(tbl.rows)
        n_cols = len(tbl.columns)
    except Exception:
        return False

    if n_rows != 1 or n_cols != 2:
        return False

    return table_has_math(tbl)


# ============ 主流程 ============

doc = Document("输出15.docx")

# 取文档主 section 的可用宽度
# 注意：若文档含多节且页宽不同，需要更精细地按表格所在节取，
#       常见单节文档用 sections[0] 即可
section = doc.sections[0]
usable_twips = get_usable_width_twips(section, SAFETY_MARGIN_CM)

# 按比例分配三列宽度
widths_twips = distribute_widths(usable_twips, COL_RATIOS, TOTAL_WIDTH_RATIO)
total_twips  = sum(widths_twips)

print(f"纸张可用宽度 = {usable_twips} twips "
      f"(≈ {usable_twips / 567:.2f} cm)")
print(f"三列实际宽度 = {widths_twips} twips "
      f"(≈ {[round(w / 567, 2) for w in widths_twips]} cm)")

processed = 0

for tbl in doc.tables:
    if not is_formula_table(tbl):
        continue

    tblEl = tbl._tbl
    grid = tblEl.find(qn('w:tblGrid'))
    if grid is None:
        continue

    # 1) 最左侧插入一个新的 gridCol
    newGridCol = copy.deepcopy(grid[0])
    grid.insert(0, newGridCol)

    # 2) 重新分配三列宽度（覆盖原来的 w:w）
    gridCols = grid.findall(W_GRIDCOL)
    for gc, w in zip(gridCols, widths_twips):
        set_gridcol_width(gc, w)

    # 3) 每行最前面插入空 tc，并给整行三个单元格重设宽度
    for tr in tblEl.findall(W_TR):
        tcs = tr.findall(W_TC)
        if not tcs:
            continue

        newTc = copy.deepcopy(tcs[0])

        # 清空除 tcPr 外的内容
        for child in list(newTc):
            if child.tag != W_TCPR:
                newTc.remove(child)

        # 清掉从被复制单元格带过来的合并信息，避免干扰列宽/布局
        tcPr = newTc.find(W_TCPR)
        if tcPr is not None:
            for tag in (W_GRIDSPAN, W_VMERGE):
                el = tcPr.find(tag)
                if el is not None:
                    tcPr.remove(el)

        newTc.append(OxmlElement('w:p'))   # 占位空段落
        tr.insert(0, newTc)

        # 重设本行三个单元格宽度
        tcs = tr.findall(W_TC)             # 重新取，现在是 3 个
        for tc, w in zip(tcs, widths_twips):
            set_cell_width(tc, w)

    # 4) 公式列（现在的第 2 列，索引 1）内容居中
    for row in tbl.rows:
        if len(row.cells) >= 2:
            for p in row.cells[1].paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # 5) 固定布局 + 表格总宽度 + 表格整体居中
    set_fixed_layout(tblEl)
    set_table_width(tblEl, total_twips)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    processed += 1

print(f"共处理公式表格：{processed} 个")
doc.save("输出3_fixed.docx")