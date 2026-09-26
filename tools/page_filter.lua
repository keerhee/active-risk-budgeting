-- 노트 웹 페이지용 pandoc 필터
-- 1) 본문 첫 H1은 YAML title과 겹치므로 지운다
-- 2) mermaid 코드블록을 mermaid.js가 읽는 <pre class="mermaid">로 바꾼다
local seen_h1 = false

function Header(el)
  if el.level == 1 and not seen_h1 then
    seen_h1 = true
    return {}
  end
end

function CodeBlock(el)
  if el.classes:includes("mermaid") then
    local t = el.text:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;")
    -- mermaid 라벨의 <br/>은 줄바꿈으로 써야 하므로 되살린다
    t = t:gsub("&lt;br/&gt;", "<br/>")
    return pandoc.RawBlock("html", '<pre class="mermaid">' .. t .. "</pre>")
  end
end

-- 3) 저장소 안 노트 간 링크(.md)는 사이트에서 .html로 연결한다
function Link(el)
  if not el.target:match("^%a+://") then
    el.target = el.target:gsub("%.md$", ".html"):gsub("%.md#", ".html#")
  end
  return el
end
