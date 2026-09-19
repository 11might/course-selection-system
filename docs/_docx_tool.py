# -*- coding: utf-8 -*-
"""docx 读写工具 —— 给下一次对话的 AI（也给人看）

背景：从 2026-09-19 起本项目「以 Word 为主」，docs 里不再有 md 源文件。
所以以后要读/改学习文档，都得直接操作 .docx。本脚本就是干这个的。

用法（都在 I:\\EE （2） 下执行）：

  1) 看全文（带段落编号，方便定位）
     python docs\\_docx_tool.py read "docs\\给新Agent交接手册.docx"
     python docs\\_docx_tool.py read "docs\\给新Agent交接手册.docx" --out C:\\Temp\\dump.txt

  2) 搜关键词，只打印命中的段落号和内容（改之前先定位）
     python docs\\_docx_tool.py find "docs\\学习日记汇总.docx" 2026-09-19

  3) 把某一段替换成新文字（默认先预览，不写盘）
     python docs\\_docx_tool.py replace "docs\\给新Agent交接手册.docx" 58 "新的整段文字"
     python docs\\_docx_tool.py replace "docs\\给新Agent交接手册.docx" 58 "新的整段文字" --apply

  4) 往中间章节插一段（在第 N 段之后）
     python docs\\_docx_tool.py insert "docs\\给新Agent交接手册.docx" 58 "要插入的文字" --apply

  5) 删掉某一段（比如插错位置、或明显错误的句子）
     python docs\\_docx_tool.py delete "docs\\给新Agent交接手册.docx" 189 --apply

  6) 文末追加一段（比如续写日记）
     python docs\\_docx_tool.py append "docs\\学习日记汇总.docx" "## 续写：2026-09-20（...）" --apply

  7) 重建「学习总结完整版.docx」合并本（改完其他 Word 后跑一次同步）
     python docs\\_docx_tool.py combined --apply
     说明：按 手册 → 进度 → 日记 → 时间表 的顺序，从现有 docx 抽取文字拼成一份。
     抽取是纯文字（表格会拍平成一行），所以合并本只适合通勤/手机速览；
     要看细节请看对应的单份 Word。

规则 / 已知坑（都是真踩过的）：

- 一个「段落」在 Word 内部可能被拆成多个 run（格式变了就会拆）。
  replace 会保留第 1 个 run 的格式，把其余 run 清空 —— 所以整段会统一成一种样式。
  需要段内一部分加粗时，得手工处理 run，本工具不管。
- replace 只改你指定的那一段，**不会按关键词匹配**。
  （2026-09-19 的教训：按关键词批量替换，一次冲掉了 6 段，只好从 git 捞原文重来。）
- 覆盖前先 commit 存档。docx 是二进制，git 看不见改了什么，只能整份存；
  改坏了就用 `git show <commit>:docs/xxx.md` 或 `git checkout <commit> -- docs/xxx.docx` 找回。
- python-docx 不在 backend\\requirements.txt 里（那是后端的），依赖清单见 docs\\requirements-docs.txt。
- 旧脚本 _md_to_docx.py 是 md→docx 导出器，md 已删，它跑不起来了；留作历史。
"""

import argparse
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn


def _load(path: Path) -> Document:
    if not path.exists():
        sys.exit(f"找不到文件：{path}")
    if path.suffix.lower() != ".docx":
        sys.exit(f"不是 .docx：{path}")
    return Document(str(path))


def cmd_read(args) -> None:
    doc = _load(args.path)
    lines = [f"[{i}] {p.text}" for i, p in enumerate(doc.paragraphs)]
    text = "\n".join(lines)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
        print(f"已写出：{args.out}（{len(lines)} 段）")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
        print(f"\n--- 共 {len(lines)} 段 ---", file=sys.stderr)


def cmd_find(args) -> None:
    doc = _load(args.path)
    sys.stdout.reconfigure(encoding="utf-8")
    hits = 0
    for i, p in enumerate(doc.paragraphs):
        if args.keyword in p.text:
            print(f"[{i}] {p.text}")
            hits += 1
    print(f"\n命中 {hits} 段", file=sys.stderr)
    if not hits:
        sys.exit(1)


def _set_paragraph_text(paragraph, new_text: str) -> None:
    """保留首个 run 的格式，整段替换为新文字（其余 run 清空）。"""
    if paragraph.runs:
        paragraph.runs[0].text = new_text
        for run in paragraph.runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(new_text)


def cmd_replace(args) -> None:
    doc = _load(args.path)
    if not (0 <= args.index < len(doc.paragraphs)):
        sys.exit(f"段落号越界：{args.index}（本文共 {len(doc.paragraphs)} 段，编号 0 起）")
    para = doc.paragraphs[args.index]
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"原文[{args.index}]：{para.text}")
    print(f"新文[{args.index}]：{args.text}")
    if not args.apply:
        print("\n（预览模式，未写盘。确认无误后加 --apply）", file=sys.stderr)
        return
    _set_paragraph_text(para, args.text)
    doc.save(str(args.path))
    print(f"\n已写入：{args.path}", file=sys.stderr)


def cmd_append(args) -> None:
    doc = _load(args.path)
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"将追加：{args.text[:80]}{'...' if len(args.text) > 80 else ''}")
    if not args.apply:
        print("（预览模式，未写盘。确认无误后加 --apply）", file=sys.stderr)
        return
    doc.add_paragraph(args.text)
    doc.save(str(args.path))
    print(f"已追加到：{args.path}（现 {len(Document(str(args.path)).paragraphs)} 段）", file=sys.stderr)


def cmd_insert(args) -> None:
    """在第 index 段之后插入一段新文字（用于往中间章节补内容）。"""
    doc = _load(args.path)
    if not (0 <= args.index < len(doc.paragraphs)):
        sys.exit(f"段落号越界：{args.index}（本文共 {len(doc.paragraphs)} 段）")
    sys.stdout.reconfigure(encoding="utf-8")
    anchor = doc.paragraphs[args.index]
    print(f"锚点[{args.index}]：{anchor.text[:70]}")
    print(f"插入  ：{args.text[:70]}{'...' if len(args.text) > 70 else ''}")
    if not args.apply:
        print("\n（预览模式，未写盘。确认无误后加 --apply）", file=sys.stderr)
        return
    new_para = doc.add_paragraph(args.text)  # 先建到文末，再挪到锚点后面
    anchor._p.addnext(new_para._p)
    doc.save(str(args.path))
    paras = Document(str(args.path)).paragraphs
    pos = next((i for i, p in enumerate(paras) if p._p is new_para._p), None)  # 同一进程内可用；重开文档则对象不同
    where = f"新段落号 {pos}" if pos is not None else "已插入（段落号请用 read 复核）"
    print(f"\n已插入到：{args.path}（{where}，现共 {len(paras)} 段）", file=sys.stderr)


def cmd_delete(args) -> None:
    """删除指定段落（用于清理插错位置或明显错误的内容）。"""
    doc = _load(args.path)
    if not (0 <= args.index < len(doc.paragraphs)):
        sys.exit(f"段落号越界：{args.index}（本文共 {len(doc.paragraphs)} 段）")
    para = doc.paragraphs[args.index]
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"将删除[{args.index}]：{para.text}")
    if not args.apply:
        print("\n（预览模式，未写盘。确认无误后加 --apply）", file=sys.stderr)
        return
    para._p.getparent().remove(para._p)
    doc.save(str(args.path))
    print(f"\n已删除，现存 {len(Document(str(args.path)).paragraphs)} 段", file=sys.stderr)


def _set_run_font(run, size: int, bold: bool = False) -> None:
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = "Microsoft YaHei"
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.get_or_add_rFonts()
    rfonts.set(qn("w:eastAsia"), "Microsoft YaHei")


# 合并本的组成顺序（改完单份 Word 后跑 combined 同步）
COMBINED_PARTS = [
    ("给新Agent交接手册.docx", "第一部分：给新 Agent 的交接手册"),
    ("学习进度与技术说明.docx", "第二部分：学习进度与技术说明"),
    ("学习日记汇总.docx", "第三部分：学习日记（按时间续写）"),
    ("每日学习时间表与督学约定.docx", "第四部分：每日学习时间表与督学约定"),
]


def cmd_combined(args) -> None:
    """从 4 份单文档重建「学习总结完整版.docx」，供通勤/手机速览。"""
    docs_dir = args.path
    if not docs_dir.is_dir():
        docs_dir = docs_dir.parent
    missing = [n for n, _ in COMBINED_PARTS if not (docs_dir / n).exists()]
    if missing:
        sys.exit(f"缺少单份文档：{missing}（在 {docs_dir}）")

    combined = Document()
    style = combined.styles["Normal"]
    style.font.name = "Microsoft YaHei"
    style.font.size = Pt(11)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Microsoft YaHei")

    title = combined.add_paragraph()
    _set_run_font(title.add_run("选课系统 · 学习总结完整版（交接手册 + 进度说明 + 日记 + 时间表）"), 18, True)
    title.paragraph_format.space_after = Pt(12)

    total = 0
    counts = []
    for filename, part_title in COMBINED_PARTS:
        head = combined.add_paragraph()
        _set_run_font(head.add_run(part_title), 16, True)
        sep = combined.add_paragraph()
        _set_run_font(sep.add_run("————————"), 10)
        texts = _extract_texts(docs_dir / filename)
        counts.append((filename, len(texts)))
        for text in texts:
            para = combined.add_paragraph()
            _set_run_font(para.add_run(text), 11)
            total += 1

    sys.stdout.reconfigure(encoding="utf-8")
    print("将按此顺序合并：")
    for filename, n in counts:
        print(f"  {filename}  ->  {n} 段")
    print(f"合计 {total} 段 -> {docs_dir / '学习总结完整版.docx'}")

    if not args.apply:
        print("\n（预览模式，未写盘。确认无误后加 --apply）", file=sys.stderr)
        return

    out = docs_dir / "学习总结完整版.docx"
    combined.save(str(out))
    print(f"\n已重建：{out}", file=sys.stderr)


def _extract_texts(path: Path):
    """抽出单份 docx 的正文段落，跳过前两行（大标题与分隔线）。"""
    texts = [p.text for p in Document(str(path)).paragraphs]
    return [t for t in texts[2:] if t.strip()]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="_docx_tool.py",
        description="直接读写 docs 里的 Word 学习文档（md 已废弃）",
        epilog="改 Word 前先 git commit 存档；replace 默认预览，确认后加 --apply。",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_read = sub.add_parser("read", help="按段落号打印全文")
    p_read.add_argument("path", type=Path)
    p_read.add_argument("--out", type=Path, default=None, help="改为写入文本文件（推荐，避免终端乱码）")
    p_read.set_defaults(func=cmd_read)

    p_find = sub.add_parser("find", help="按关键词找段落号")
    p_find.add_argument("path", type=Path)
    p_find.add_argument("keyword")
    p_find.set_defaults(func=cmd_find)

    p_rep = sub.add_parser("replace", help="替换指定段落（默认预览）")
    p_rep.add_argument("path", type=Path)
    p_rep.add_argument("index", type=int, help="段落号，0 起")
    p_rep.add_argument("text")
    p_rep.add_argument("--apply", action="store_true", help="真正写盘")
    p_rep.set_defaults(func=cmd_replace)

    p_app = sub.add_parser("append", help="在文末追加一段（默认预览）")
    p_app.add_argument("path", type=Path)
    p_app.add_argument("text")
    p_app.add_argument("--apply", action="store_true", help="真正写盘")
    p_app.set_defaults(func=cmd_append)

    p_ins = sub.add_parser("insert", help="在第 N 段之后插入一段（默认预览）")
    p_ins.add_argument("path", type=Path)
    p_ins.add_argument("index", type=int, help="锚点段落号，0 起；新段落插在它后面")
    p_ins.add_argument("text")
    p_ins.add_argument("--apply", action="store_true", help="真正写盘")
    p_ins.set_defaults(func=cmd_insert)

    p_del = sub.add_parser("delete", help="删除第 N 段（默认预览）")
    p_del.add_argument("path", type=Path)
    p_del.add_argument("index", type=int, help="段落号，0 起")
    p_del.add_argument("--apply", action="store_true", help="真正写盘")
    p_del.set_defaults(func=cmd_delete)

    p_com = sub.add_parser("combined", help="从 4 份单文档重建学习总结完整版.docx（默认预览）")
    p_com.add_argument("path", type=Path, nargs="?", default=Path(__file__).resolve().parent, help="docs 目录，默认脚本所在目录")
    p_com.add_argument("--apply", action="store_true", help="真正写盘")
    p_com.set_defaults(func=cmd_combined)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
