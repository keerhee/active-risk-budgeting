# 액티브 리스크 배분 모형

**사이트:** <https://keerhee.github.io/active-risk-budgeting/> — 슬라이드와 노트를 한곳에서 열어볼 수 있습니다.

Ostrum / EDHEC-Risk "Fixed-Income Portfolio Construction with Active Views" 자료를 재구성해,
정보계수(IC) 기반 사전 정보비율과 트래킹 에러 예산 배분을 투자위원회용으로 정리한 자료 일체.

작성일 2026년 9월 26일

---

## 구성

### 본 설명자료 (38장)

[슬라이드 PDF](decks/Active_Risk_Budgeting_IC_Framework.pdf) · [노트](notes/Risk_Budgeting_IC_Framework.md) · [노트 웹 페이지](https://keerhee.github.io/active-risk-budgeting/notes/Risk_Budgeting_IC_Framework.html)

JJ 브리프 덱. 여섯 섹션으로 구성한다.

| 섹션 | 내용 |
|---|---|
| 01 개요 | 알파 · 트래킹 에러 · 정보비율의 정의 |
| 02 원리 | FLAM · 뷰에서 알파로 · 전이계수 · 결합 IR · 원 모형 도출 |
| 03 결함 | 층위 혼동 · 유효 breadth · IC 집계 포화 · 누적 효과 |
| 04 재구성 | 사전 IR 조립 · 슬리브별 비교 · 개선된 최적화식 |
| 05 적용 | 배분 결과 · Aggregate 스킬 민감도 |
| 06 운영 | 승인 항목 · 진단 분해 · 사후 루프 · 한계 |

핵심 주장 — 원 모형의 구조는 타당하나 TC, 베팅 간 상관, 뷰 분산 보정이 빠져
기대 정보비율이 실제의 3~6배로 나온다. 세 항을 넣으면 예시 기준 0.42가 0.13으로 내려온다.

### 실행 부록 (33장)

[슬라이드 PDF](decks/Risk_Budgeting_Implementation_Appendix.pdf) · [노트](notes/Risk_Budgeting_Implementation_Appendix.md) · [노트 웹 페이지](https://keerhee.github.io/active-risk-budgeting/notes/Risk_Budgeting_Implementation_Appendix.html)

배분된 트래킹 에러를 실제 포지션과 계약 수로 바꾸는 절차.

| 섹션 | 내용 |
|---|---|
| 01 원칙 | 제곱합 합산 · 본문 배분표 정정 · 무제약 최적해 재계산 |
| 02 절차 | 단위 리스크 구조 · 크기 결정 · 제약 투영 |
| 03 예제 | 1,000억원 · 100bp · 금리와 달러 두 전략 |
| 04 환산 | 상한 구속 · 미사용 예산 · 1차·2차 환산 |
| 05 현금 | 오버레이 구조 · 증거금 · 현금 버퍼 |
| 06 검증 | 실현 TE 검산 · 괴리 진단 · TC 수축 · 위원회 항목 |

핵심 주장 — 리스크 예산 배분과 자금 배분은 다른 단계다. 배분 TE는 금액이 아니라
포지션 크기의 스케일 계수이며, 1조원 기준 실제로 움직이는 현금은 증거금과 담보 315억원뿐이다.

---

## 저장소 구성

```
decks/   슬라이드 PDF 2개
notes/   노트 Markdown 2개 (본문 노트가 실행 부록 노트로 링크된다)
site/    GitHub Pages 사이트 (tools/make_site.py로 생성)
tools/   사이트 생성 스크립트와 pandoc 필터
```

노트의 수식은 GitHub에서 그대로 렌더링되고, 사이트에서는 KaTeX로 표시된다.

---

## 핵심 수식

사전 정보비율

$$
IR_i^{\text{ante}} \;=\; IC_i \times \sqrt{BR_i^{\text{eff}}} \times TC_i, \qquad
BR_i^{\text{eff}} \;=\; \frac{BR_i}{1 + (BR_i - 1)\bar\rho_i}
$$

리스크 예산 최적화

$$
\max_{TE}\; a^\top TE - \tfrac{\lambda}{2} TE^\top \Omega\, TE
\quad \text{s.t.}\quad TE^\top C\, TE \le \sigma_A^2, \;\; 0 \le TE_i \le \bar{TE}_i
$$

실행 환산

$$
\text{포지션 크기} \;=\; \frac{TE_i}{\sigma(\text{리스크 요인})}
$$

---

## 예시 수치의 일관성

두 자료는 같은 네 슬리브 예시를 쓴다.

| 슬리브 | IC | 명목 BR | 내부 상관 | 유효 BR | TC | 사전 IR | View | 상한 적용 TE |
|---|---|---|---|---|---|---|---|---|
| 듀레이션 | 0.06 | 12 | 0.15 | 4.3 | 0.75 | 0.093 | +2 | 160bp |
| FX | 0.05 | 10 | 0.20 | 3.6 | 0.80 | 0.076 | +1 | 148bp |
| 주식 국가배분 | 0.04 | 20 | 0.35 | 2.6 | 0.40 | 0.026 | 0 | 0bp |
| 크레딧 | 0.05 | 8 | 0.30 | 2.5 | 0.50 | 0.040 | +1 | 78bp |

- 승인 총 액티브 리스크 400bp, 슬리브 상한 40%(160bp)
- 무제약 최적해 363 / 148 / 78bp → 제곱합 400bp
- 상한 적용 후 160 / 148 / 78bp → 제곱합 **231bp**, 169bp 미사용
- 기대 총 알파 44bp, 기대 IR 0.19

**정정 이력** — 본 덱 29장의 배분표는 당초 155 / 105 / 0 / 55bp를 산술합 400bp로 적었다.
제곱합으로는 195bp이므로 승인 예산의 절반만 쓴 배분이었다. 무제약 최적해를 다시 풀고
슬리브 상한을 적용해 위 수치로 고쳤으며, 경위는 부록 §1에 남겼다.

---

## 제작 도구

| 요소 | 도구 |
|---|---|
| 덱 | jj-brief-deck (pptxgenjs, 10 × 5.625 in) |
| 수식 | pdflatex → pdftoppm, 300 DPI PNG |
| 차트 | matplotlib (Noto Sans CJK) |
| 도해 | 직접 작성한 SVG → cairosvg |
| 마크다운 | obsidian-math-md 4규칙 |

