"""site/ 생성기. 실행: python3 tools/make_site.py (저장소 루트에서)

- site/index.html : 자료 목록 (CSS·JS는 total-portfolio-approach 사이트와 같은 tools/tpl/)
- site/notes/<이름>.html : notes/<이름>.md를 KaTeX 수식·Mermaid 흐름도로 읽는 페이지
필요: pandoc, pdfinfo
"""
import html, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "https://github.com/keerhee/active-risk-budgeting"
BLOB, RAW = f"{REPO}/blob/main", f"{REPO}/raw/main"
PAGE_CSS = (pathlib.Path(__file__).with_name("page.css")).read_text()

# 섹션 id, 색, 라벨, 제목, 부제, 덱 파일, 노트 파일, 덱 설명, 노트 설명, 검색어
PARTS = [
    ("MAIN", "m1", "본문", "액티브 리스크 배분 모형 — IC로 트래킹 에러 예산을 나눈다",
     "메인식 · 손계산 · 배경 · 보정 · 심화 · 운영",
     "Active_Risk_Budgeting_IC_Framework", "Risk_Budgeting_IC_Framework",
     "원자료 최적화식 → 전략 3개·300bp 손계산 → FLAM·뷰에서 알파로 → TC·유효 breadth·뷰 스케일 보정 → 층위 문제 → 승인·사후 루프",
     "덱의 전체 서술본 · 메인식과 네 줄짜리 해 · 3-4-5 손계산 · 보정 후 IR 0.50→0.19 · IC 집계 포화 · 사후 IC 수축 루프",
     "ic 정보계수 ir 정보비율 flam fundamental law breadth 전이계수 tc 트래킹 에러 te 최적화 손계산 view 확신도 natixis ostrum edhec"),
    ("APPX", "m2", "부록", "부록 — 리스크 예산에서 실제 실행까지",
     "원칙 · 절차 · 예제 · 환산 · 현금 · 검증",
     "Risk_Budgeting_Implementation_Appendix", "Risk_Budgeting_Implementation_Appendix",
     "제곱합 합산·배분표 정정 → 실행 3단계 → 1,000억원 예제 → 계기별 환산 → 증거금·현금 버퍼 → 실현 TE 검산",
     "배분된 TE를 포지션 크기·계약 수로 · DV01 · 오버레이와 증거금 · 사후 검산과 TC 실측 · 위원회 점검 항목",
     "실행 오버레이 overlay dv01 계약 선물 증거금 담보 현금 버퍼 실현 te 검산 tc 실측"),
    ("CODE", "m3", "구현", "Claude Code 구현 가이드 — 리스크 예산에서 선물 계약까지",
     "개요 · 준비 · 배분 · 보정 · 실행 · 운영",
     "Risk_Budgeting_Claude_Code_Implementation", None,
     "사용자 프롬프트 15개로 따라가는 구현 — 저장소·규칙·입력 등록부 → 닫힌 해와 손계산 테스트 → 보정·상한 → 계약 수·현금 → 사후 검산·수축·/quarterly",
     None,
     "claude code 프롬프트 prompt 구현 자동화 claude.md yaml pytest 테스트 quarterly 보고서 수축 체결 계약 수"),
]


def pdf_pages(rel):
    out = subprocess.run(["pdfinfo", str(ROOT / rel)], capture_output=True, text=True, check=True).stdout
    return int(next(l.split()[-1] for l in out.splitlines() if l.startswith("Pages:")))


def size(rel):
    b = (ROOT / rel).stat().st_size
    return f"{b/1024/1024:.1f} MB" if b >= 1024 * 1024 else f"{round(b/1024)} KB"


def link(label, href, cls="vw", new=True):
    tgt = ' target="_blank" rel="noopener"' if new else ""
    return f'<a class="act {cls}" href="{href}"{tgt}>{label}</a>'


def row(tag, tcls, dtype, title, sub, meta, keys, links):
    e = html.escape
    return (f'<li class="row" data-k="{e((title + " " + sub + " " + keys).lower())}" data-t="{dtype}">'
            f'<span class="tag {tcls}">{tag}</span><span class="ttl">{e(title)}<em>{e(sub)}</em></span>'
            f'<span class="meta">{meta}</span><span class="acts">{"".join(links)}</span></li>')


def build_note(stem, back_label):
    hdr, bef, aft = (ROOT / "tools/_hdr.html", ROOT / "tools/_bef.html", ROOT / "tools/_aft.html")
    hdr.write_text('<link rel="icon" href="data:,">\n'
                   '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.min.css">\n'
                   f"<style>{PAGE_CSS}</style>")
    bef.write_text(f'<div class="topbar"><a href="../">← 액티브 리스크 배분</a> · {back_label}</div><main>')
    aft.write_text('</main>\n<script type="module">\n'
                   'import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";\n'
                   'const dark = matchMedia("(prefers-color-scheme: dark)").matches;\n'
                   'mermaid.initialize({startOnLoad: true, theme: dark ? "dark" : "neutral", fontFamily: "Pretendard, sans-serif"});\n'
                   '</script>')
    try:
        subprocess.run(["pandoc", str(ROOT / f"notes/{stem}.md"), "-s", "--katex", "--toc", "--toc-depth=2",
                        "--lua-filter", str(ROOT / "tools/page_filter.lua"),
                        "-M", "toc-title=목차", "-M", "lang=ko",
                        "-H", str(hdr), "-B", str(bef), "-A", str(aft),
                        "-o", str(ROOT / f"site/notes/{stem}.html")], check=True)
    finally:
        for p in (hdr, bef, aft):
            p.unlink(missing_ok=True)


def build_index():
    style = (ROOT / "tools/tpl/style.html").read_text()
    script = (ROOT / "tools/tpl/script.html").read_text()
    style = style.replace('font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif',
                          'font:16px/1.65 Pretendard,-apple-system,BlinkMacSystemFont,"Apple SD Gothic Neo","Segoe UI",sans-serif;word-break:keep-all')
    if "footer a,.panel a" not in style:
        style = style.replace("footer a{color:var(--accent)}", "footer a,.panel a{color:var(--accent)}")

    total, secs, nav = 0, [], []
    for sid, m, label, title, sub, deck, note, dsub, nsub, keys in PARTS:
        rel = f"decks/{deck}.pdf"
        pages = pdf_pages(rel)
        total += pages
        rows = [
            row("강의덱", "t-l", "강의덱", f"{label} 슬라이드", dsub, f"{pages}장 · {size(rel)}", keys,
                [link("보기", f"{BLOB}/{rel}"), link("내려받기", f"{RAW}/{rel}", "dl", False)]),
        ]
        if note:
            rows.append(row("노트", "t-d", "노트", f"{label} 노트", nsub, "웹 페이지", keys,
                [link("읽기", f"notes/{note}.html", "dl", False), link("Markdown", f"{BLOB}/notes/{note}.md")]))
        nav.append(f'<a class="wknav {m}" href="#{sid}" data-w="{sid}" title="{html.escape(title)}">{label}</a>')
        secs.append(f'<section class="wk" id="{sid}"><h2><span class="wn {m}">{sid}</span>'
                    f'<span class="h2t">{html.escape(title)}<em>{html.escape(sub)}</em></span>'
                    f'<span class="cnt">{len(rows)}</span></h2><ul class="list">{"".join(rows)}</ul></section>')
    chips = "".join(f'<button class="chip" data-f="{f}" aria-pressed="{"true" if not f else "false"}">{l}</button>'
                    for f, l in [("", "전체"), ("강의덱", "강의덱"), ("노트", "노트")])

    page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>액티브 리스크 배분 모형</title>
<meta name="description" content="정보계수(IC)로 트래킹 에러 예산을 나누는 방법 — 투자위원회용 설명자료, 실행 부록, Claude Code 구현 가이드.">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%2314203a'/%3E%3Crect x='14' y='34' width='8' height='16' fill='%237aa7f0'/%3E%3Crect x='28' y='24' width='8' height='26' fill='%237aa7f0'/%3E%3Crect x='42' y='14' width='8' height='36' fill='%237aa7f0'/%3E%3C/svg%3E">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/pretendard@1.3.9/dist/web/static/pretendard.min.css">
{style}<body>

<header class="top"><div class="wrap">
  <div class="code">ACTIVE RISK BUDGETING · 2026</div>
  <h1>액티브 리스크 배분 모형</h1>
  <p class="lead">정보계수(IC)로 트래킹 에러 예산을 나누는 방법을 투자위원회용으로 정리했습니다.
  본문은 메인식과 손계산, 보정을 다루고, 부록은 배분된 리스크 예산을 실제 포지션과 계약 수로 바꾸는 절차를,
  구현 가이드는 그 전 과정을 Claude Code에 시키는 프롬프트를 다룹니다.</p>
  <div class="stats">
    <div><b>{len(PARTS)}</b><span>강의 덱</span></div>
    <div><b>{total}</b><span>슬라이드</span></div>
    <div><b>2</b><span>노트</span></div>
    <div><b>15</b><span>프롬프트</span></div>
  </div>
</div></header>

<div class="bar"><div class="wrap">
  <div class="r1">
    <input id="q" type="search" placeholder="검색 — 예: 전이계수, breadth, DV01, 증거금" autocomplete="off">
    {chips}
  </div>
  <nav class="r2">{"".join(nav)}</nav>
</div></div>

<div class="wrap">

<section class="panel">
  <h2>핵심 주장</h2>
  <p><strong>각 전략에 점수 하나(IC × √BR × View)를 매기고, 승인된 트래킹 에러 예산을 그 점수에 비례해 나눕니다.</strong>
  식은 끝까지 바뀌지 않고, IR 자리에 들어가는 숫자만 전이계수(TC), 유효 breadth, 뷰 스케일로 보정합니다.
  예시 기준 원식 IR 0.50이 보정 후 0.19로 내려오며, 후자가 멀티에셋 액티브의 방어 가능 구간입니다.
  IR은 결과라 늦게 보이고, IC는 원인이라 빨리 보입니다 — IC로 관리하고 IR로 검증합니다.</p>
  <p><strong>리스크 예산 배분과 자금 배분은 다른 단계입니다.</strong> 배분된 트래킹 에러는 금액이 아니라 포지션 크기의 스케일 계수이고,
  실행은 대부분 파생상품 오버레이로 합니다. 1조원 기준 실제로 움직이는 현금은 증거금과 담보 315억원뿐입니다.</p>
  <p><strong>판단은 사람이 정하고, 계산과 검산은 Claude Code가 합니다.</strong> 구현 가이드는 단계마다 프롬프트 하나, 산출물 파일 하나,
  사람이 확인할 숫자 하나를 짝지어 분기 루틴을 <code>/quarterly</code> 명령 하나로 묶습니다.</p>
  <div class="cpwrap"><button class="cp">복사</button><pre>git clone {REPO}.git</pre></div>
  <p class="note">원자료: Ostrum / EDHEC-Risk "Fixed-Income Portfolio Construction with Active Views" 강의 자료를 재구성했습니다.
  본문과 구현 가이드는 세 전략 · 300bp 손계산 예제를, 부록은 네 슬리브 · 400bp와 1조원 실무 예제를 씁니다.</p>
</section>

{"".join(secs)}

<div id="empty" class="empty hide">검색 결과가 없습니다.</div>
<div id="tail"></div>

<footer>
  <p><strong>정정 이력</strong> — 초판 배분표는 슬리브별 TE를 산술합으로 400bp라 적었습니다. 트래킹 에러는 제곱합으로 더하므로
  그 표는 실제로 195bp를 쓴 배분이었으며, 합산 원칙과 재계산 경위는 부록 §1에 남겼습니다.
  부록 28장 · §7.1의 실현 TE 합계는 222bp에서 225bp(√(160² + 148² + 55²))로 고쳤습니다(2026-09-27).
  &middot; <a href="{REPO}">저장소</a></p>
</footer>
</div>

{script.replace("Press \\\\u2318C", "⌘C를 누르세요").replace("'Copied'", "'복사됨'").replace("'Copy'", "'복사'")}
</body></html>
"""
    (ROOT / "site/index.html").write_text(page)
    print(f"site/index.html: {len(PARTS)} decks {total} slides")


if __name__ == "__main__":
    build_note("Risk_Budgeting_IC_Framework", "본문 노트")
    build_note("Risk_Budgeting_Implementation_Appendix", "실행 부록 노트")
    build_index()
