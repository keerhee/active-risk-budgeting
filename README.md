# 액티브 리스크 배분 모형

**사이트:** <https://keerhee.github.io/active-risk-budgeting/> — 슬라이드와 노트를 한곳에서 열어볼 수 있습니다.

Ostrum / EDHEC-Risk "Fixed-Income Portfolio Construction with Active Views" 자료를 재구성해,
정보계수(IC) 기반 사전 정보비율과 트래킹 에러 예산 배분을 투자위원회용으로 정리한 자료 일체.

작성일 2026년 9월 27일

---

## 구성

### 본 설명자료 (38장)

[슬라이드 PDF](decks/Active_Risk_Budgeting_IC_Framework.pdf) · [노트](notes/Risk_Budgeting_IC_Framework.md) · [노트 웹 페이지](https://keerhee.github.io/active-risk-budgeting/notes/Risk_Budgeting_IC_Framework.html)

JJ 브리프 덱. 메인식은 Ostrum / EDHEC-Risk 원자료의 식을 그대로 쓰고, 보정은 뒤에서 계수로 얹는다.

| 섹션 | 내용 |
|---|---|
| 01 메인식 | 목적함수 · 제약 · 입력 셋 · 네 줄짜리 해 |
| 02 손계산 | 전략 3개 · 300bp · 네 단계를 계산기로 푼다 |
| 03 배경 | FLAM · 적중률과 IC · 뷰에서 알파로 · 가법성 |
| 04 보정 | 전이계수 · 유효 breadth · 뷰 스케일 · 같은 예제 재계산 |
| 05 심화 | 층위 문제 · IC 집계 포화 |
| 06 운영 | 승인 항목 · 상한 구속 · 사후 루프 · 진단 · 한계 |

핵심 주장 — 식은 끝까지 바뀌지 않는다. IR 자리에 들어가는 숫자만 보정한다.
예시 기준 원식 IR 0.50이 보정 후 0.19로 내려오며, 후자가 멀티에셋 액티브의 방어 가능 구간이다.

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

## 손계산 예제

본 자료 02장의 예제. 전략 셋, 승인 리스크 300bp.

| 전략 | $IC$ | $BR$ | $\sqrt{BR}$ | $IR$ | $View$ | 점수 $a$ |
|---|---|---|---|---|---|---|
| 듀레이션 | 0.05 | 16 | 4 | 0.20 | +2 | 0.40 |
| FX | 0.06 | 25 | 5 | 0.30 | +1 | 0.30 |
| 크레딧 | 0.04 | 9 | 3 | 0.12 | 0 | 0 |

점수 벡터의 길이가 3-4-5 직각삼각형으로 떨어진다.

$$
\sqrt{0.40^2 + 0.30^2} = 0.50, \qquad TE^\star = 300 \times \frac{a}{0.50}
$$

듀레이션 240bp · FX 180bp · 크레딧 0bp. 검산 $\sqrt{240^2 + 180^2} = 300$bp.
기대 알파 150bp, 기대 IR 0.50.

### 보정을 넣으면

| 전략 | $\bar\rho$ | 유효 $BR$ | $TC$ | 보정 $IR$ | 점수 $a$ | 배분 $TE$ |
|---|---|---|---|---|---|---|
| 듀레이션 | 0.20 | 4.0 | 0.80 | 0.080 | 0.160 | 257bp |
| FX | 0.22 | 4.0 | 0.80 | 0.096 | 0.096 | 154bp |
| 크레딧 | 0.30 | 2.6 | 0.50 | 0.033 | 0 | 0bp |

기대 알파 56bp, 기대 IR 0.19. 원식 대비 2.7배 과대평가였다.
명목 BR이 컸던 FX가 더 크게 깎이면서 배분 비율도 1.33에서 1.67로 이동한다.

**정정 이력** — 초판 배분표는 슬리브별 TE를 산술합으로 400bp라 적었다. 트래킹 에러는
제곱합으로 더하므로 그 표는 실제로 195bp를 쓴 배분이었다. 합산 원칙과 재계산 경위는
실행 부록 §1에 남겼다.

---

## 제작 도구

| 요소 | 도구 |
|---|---|
| 덱 | jj-brief-deck (pptxgenjs, 10 × 5.625 in) |
| 수식 | pdflatex → pdftoppm, 300 DPI PNG |
| 차트 | matplotlib (Noto Sans CJK) |
| 도해 | 직접 작성한 SVG → cairosvg |
| 마크다운 | obsidian-math-md 4규칙 |

