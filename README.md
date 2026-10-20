# 🌸 EFV∞《永不退電的一朵花》V6.4 — 終極原詞與編曲標籤全對位 × 1080P 首尾幀連續運鏡規格與自動化管線庫

[![Spec Version](https://img.shields.io/badge/Spec-V6.4.0-amber)](#)
[![Keyframes](https://img.shields.io/badge/1080P_Keyframes-99-blue)](#)
[![Video Morphs](https://img.shields.io/badge/Continuous_Morphs-88%2B11-purple)](#)
[![Dual Mode](https://img.shields.io/badge/Dual_Mode-%CE%BB_H%E2%88%88%7B1%2C0%7D-success)](#)

> **核心架構：** 歌詞意味「三階抽遞法」($\mathcal{D}_{\text{Lyric}}^{(3)}$) × 正面/側面/逆轉三態運鏡術式 ($\mathcal{O}_{\text{Front}} / \mathcal{O}_{\text{Side}} / \mathcal{O}_{\text{Inv}}$) × 九宮格「起・承・轉・合・雙伏筆 ($\alpha/\beta$)」拓撲 × 五維「抽象/理性度量衡交融張量 ($\mathcal{M}_{\text{RP}}$)」 × 可切換「有女主 ($\lambda_H=1$) / 無女主純抽象 ($\lambda_H=0$)」雙模態同構鎖 × 12 大電影大師 6-DoF 運鏡 × `55% / 30% / 15%` 首尾幀全連續影片生成。

本儲存庫將 **《永不退電的一朵花》V6.4** 單一龐大規格書徹底工程化與模組化，提供**分章節/分 SET 導覽文件**、**自動化編譯器**、**一鍵分離雙模態 (`λ_H=1` vs `λ_H=0`) 的 JSON/CSV 資料庫**，以及 **CLI 快速檢索與匯出工具 (`efv_cli.py`)**，可直接對接 Midjourney / FLUX 圖像生成與 Runway / Kling / Veo / Sora 首尾幀連續影片管線。

---

## 🚀 1. 快速上手 (Quick Start)

### A. 使用 CLI 檢索任一 SET、關鍵幀或運鏡 Prompt (`efv_cli.py`)

不需安裝任何額外第三方套件（純 Python 標準庫即可運行）：

```bash
# 1. 檢視全曲 11 個 SET 總覽與編曲導引標籤
python3 efv_cli.py list

# 2. 檢視指定段落（例如 SET_05 Chorus 1）的原詞與全部 Prompts（九宮格 + 關鍵幀 + 運鏡 + 橋接）
python3 efv_cli.py set 5 --mode heroine

# 3. 透過 Prompt ID 取得單一 Prompt（可選 heroine / abstract / dual）
python3 efv_cli.py get SET_01_K01_1080P --mode abstract
python3 efv_cli.py get SET_09_p06_MORPH --mode heroine
python3 efv_cli.py get SET_11_TO_SET_01_BRIDGE_b11

# 4. 依關鍵字或原詞搜尋對應鏡號與 Prompt
python3 efv_cli.py search "沙漏"

# 5. 一鍵匯出指定類型的純文字 Prompts（type: all|grids|keyframes|morphs|bridges）
python3 efv_cli.py export --type keyframes --mode heroine --out keyframes_heroine_99.txt
python3 efv_cli.py export --type keyframes --mode abstract --out keyframes_abstract_99.txt
```

### B. 重新編譯 V6.4 規格書與重新抽提 JSON / CSV 題詞庫

若你修改了 `src/efv_infinity_v6_4_pipeline_generator.py` 中的歌詞對位或編曲參數，可隨時重新編譯：

```bash
python3 src/efv_infinity_v6_4_pipeline_generator.py
```

### C. 一鍵推送至你的 GitHub 新 Repo

本專案已預先完成 `git init` 與初始 Commit，解壓縮後直接執行：

```bash
# 若已安裝 GitHub CLI (gh)，一行指令自動建立新 Repo 並推送：
bash scripts/push_to_github.sh efv-infinity-v6.4 public

# 或直接綁定你在 GitHub 建立好的新 Repo URL：
bash scripts/push_to_github.sh https://github.com/<你的帳號>/<你的新Repo>.git
```

---

## 📁 2. 儲存庫目錄結構 (Repository Structure)

```text
efv-infinity-v6.4/
├── README.md                                      # 專案總覽、11 SET 快速導航表與 CLI 說明
├── efv_cli.py                                     # 互動式 / 命令列 Prompt 檢索與批次匯出工具
├── scripts/
│   └── push_to_github.sh                          # 一鍵建立並推送到 GitHub 新 Repo 腳本
├── src/
│   └── efv_infinity_v6_4_pipeline_generator.py    # V6.4 自動化規格書與 Prompt 編譯器核心程式
├── prompts/
│   ├── json/
│   │   ├── efv_v6_4_prompts_manifest.json         # 全量結構化總庫 (含預分離之 λ_H=1 與 λ_H=0 欄位)
│   │   ├── master_grids_11.json                   # 11 組 3×3 九宮格母圖 Prompts
│   │   ├── keyframes_99.json                      # 99 組 1080P 關鍵幀 Prompts (含 heroine/abstract 獨立欄位)
│   │   ├── morphs_88.json                         # 88 組 SET 內首尾幀 6s 運鏡 Prompts (p00..p07)
│   │   └── bridges_11.json                        # 11 組跨 SET 首尾幀伏筆交接 Prompts (b01..b11)
│   └── csv/
│       ├── keyframes_99.csv                       # 99 張關鍵幀表格 (可直接匯入 Notion / Airtable / ComfyUI)
│       └── video_morphs_and_bridges_99.csv        # 99 段首尾幀影片運鏡表格 (88 段內 + 11 跨段閉環)
└── docs/
    ├── efv_infinity_v6_4_chaincontinuity_1080p_full_spec.md  # V6.4 單檔完整規格書 (1,341 行)
    ├── 00_Architecture_and_Equations.md           # 第零章：六階作業流、核心數學公式、12 大師運鏡與原詞總表
    └── sets/                                      # 分段獨立檢視 Markdown (含前後段快速跳轉導覽列)
        ├── SET_01.md                              # SET_01 Intro (58 BPM ➔ Hard Cut)
        ├── SET_02.md                              # SET_02 Verse 1A (62 BPM)
        ├── SET_03.md                              # SET_03 Verse 1B (62 BPM)
        ├── SET_04.md                              # SET_04 Pre-Chorus (64 ➔ 138 BPM)
        ├── SET_05.md                              # SET_05 Chorus 1 (140 BPM)
        ├── SET_06.md                              # SET_06 Break (Hard Drop to 65 BPM)
        ├── SET_07.md                              # SET_07 Verse 2 (65 BPM)
        ├── SET_08.md                              # SET_08 Bridge (Suspended ➔ 160 BPM Last Push)
        ├── SET_09.md                              # SET_09 Chorus 2 (160 BPM Release Valve)
        ├── SET_10.md                              # SET_10 Outro (Decay & Dissolve ➔ Silence)
        └── SET_11.md                              # SET_11 Post-Outro (Final Glitch Burst ➔ Cold Stop)
```

---

## 🎵 3. 全曲 11 SET 曲速曲線 × 編曲導引標籤 × 模組化文件快速導覽

| SET 段落 | 曲速 (`BPM`) | 編曲導引標籤 (`Arrangement Directive`) | 原詞核心句摘錄 | 雙伏筆迴路 (`α_S` 段內 / `β_S` 跨段) | 獨立規格文件 |
| --- | --- | --- | --- | --- | --- |
| **SET_01** _(Intro)_ | `58 BPM ➔ Hard Cut` | `[ "Intro: 58 BPM. Sparse electric piano, low synth haze, a soft pulse that never fully lands. Tiny glassy accents drift at the edges." ] ➔ [ "Hard Cut" ]` | `靜电—沉降 / 声断连— / 闪烁的印記 灑落—— / 永不退電的一朵—花` | `α_01` 無源慢脈搏核<br>`β_01` 地底霓虹引線 | [docs/sets/SET_01.md](docs/sets/SET_01.md) |
| **SET_02** _(Verse 1A)_ | `62 BPM` | `[ "Verse 1: 62 BPM. Thin groove, brushed percussion, sub bass holding back. Voice stays close, almost conversational, with a few breathy lifts." ]` | `——霓虹脉络流淌在——午夜的各金属下—— / 我在網格——曲折—重載間—漫步— (huh-hum!) [ "humming" ] / 你的精准呼吸，記下了分秒` | `α_02` 呼吸白霧張力弧<br>`β_02` 同軸霧輪化磁帶軸 | [docs/sets/SET_02.md](docs/sets/SET_02.md) |
| **SET_03** _(Verse 1B)_ | `62 BPM` | `[ "Verse 1: 62 BPM..." ] (Part B)` | `底噪的磁带悄然泛起(喚起)——昔日沉睡的凝視 / 一道溫柔的脉搏，正穿透这冰冷堡垒` | `α_03` 類比底噪穿牆韌性<br>`β_03` 橋頂壓迫巨齒輪 | [docs/sets/SET_03.md](docs/sets/SET_03.md) |
| **SET_04** _(Pre-Chorus)_ | `64 → 138 BPM` | `[ "Pre-Chorus: 64 to 138 BPM. The pattern tightens fast; percussion stacks, synths lean forward, tension keeps climbing." ]` | `运转从未过问我们为何存在 / 只在乎我们究竟能承受多久的运——转——` | `α_04` 同軸暗紅抗壓波<br>`β_04` 空拍穿鏡閃光弧 | [docs/sets/SET_04.md](docs/sets/SET_04.md) |
| **SET_05** _(Chorus 1)_ | `140 BPM` | `[ "Chorus: 140 BPM. Full lift, wide drums, bright brass layers, guitars opening up hard. Keep the hook direct and forward-driving." ]` | `当自我遗忘了沉默的脚本，/ 节奏低吟出心促—的赞歌—— / ... / 在苦甜参半的深夜里—— (EH)，/ 我们又—載——入再次启程。` | `α_05` 殘缺呼吸苦甜火種<br>`β_05` Hard Drop 靜電銀霜 | [docs/sets/SET_05.md](docs/sets/SET_05.md) |
| **SET_06** _(Break)_ | `140 → 65 BPM` | `[ "Break: Hard drop to 65 BPM. Strip everything back to a bare pulse, a single sustained chord, and air around the vocal." ]` | `靜电—沉降 / 声断连—(降)——(连)——(降)(断)` | `α_06` 延音和弦逆重力微塵<br>`β_06` 刺入透明地層潮絲 | [docs/sets/SET_06.md](docs/sets/SET_06.md) |
| **SET_07** _(Verse 2)_ | `65 BPM` | `[ "Verse 2: 65 BPM. Denser low end, rougher edges, more movement in the bassline and percussion, like the track has picked up static." ]` | `心情浮沉如低音涌动 / ... / 故障打擊樂敲碎了沙漏的流轉—— / 我將名字留在一個標為“已淘汰”的文件夾中 / ... / 感知導線的溫度` | `α_07` 淘汰文件夾慢速餘溫<br>`β_07` 觸碰夜色邊界波紋 | [docs/sets/SET_07.md](docs/sets/SET_07.md) |
| **SET_08** _(Bridge)_ | `65 → 160 BPM` | `[ "Bridge: Suspended, almost weightless. Leave space between phrases; let the harmony breathe before the last push." ]` | `夜色中的释怀 / 没有宏大的蓝图 / 只有温柔的抗拒—— / 拒绝永远停留在边界之内` | `α_08` 穿縫滲出溫柔破界霧<br>`β_08` 160 BPM 衝天花莖橋 | [docs/sets/SET_08.md](docs/sets/SET_08.md) |
| **SET_09** _(Chorus 2)_ | `160 BPM` | `[ "Chorus 2: 160 BPM. Bigger, wider, more overloaded. Everything feels opened to the top end; final chorus should hit like a release valve." ]` | `当自我——遗忘了沉默的脚本，/ 节奏吟唱出——躍下的赞歌。/ ... / 也不是游荡的 / 模拟的 / 幽灵的 / 微风裡的 / 数字—— (EH)` | `α_09` 差一指寬穿光孔隙<br>`β_09` 拆解節奏前低鳴光環 | [docs/sets/SET_09.md](docs/sets/SET_09.md) |
| **SET_10** _(Outro)_ | `Decay → Silence` | `[ "Outro: Decay and dissolve. Pull the rhythm apart, let the low tones stretch, and let the last echoes thin out to nothing." ] ➔ [ "Silence" ]` | `……仍在低鸣 / ……仍在低鸣—— / ......—— / [ "Silence" ]` | `α_10` 拉伸低音古銅殘弧<br>`β_10` Silence 靜默奇點 | [docs/sets/SET_10.md](docs/sets/SET_10.md) |
| **SET_11** _(Post-Outro)_ | `Glitch Burst → 0` | `[ "Post-Outro: Final glitch burst, then immediate stop. One last fractured tail, then total black." ] ➔ DU—— ➔ [ "Sudden Abrupt Cold Stop" ]` | `—心——斷——連—— / 落塵——穿——透—— / 靜电——沉降—— / 花(華)——(FL—OW—ER——) ×4 / DU—— / ...—` | `α_11` 四相花 360° 蛻變鎖<br>`β_11` 莫比烏斯迴環微塵 (`∞`) | [docs/sets/SET_11.md](docs/sets/SET_11.md) |

---

## 🎛️ 4. 結構化 JSON / CSV 欄位說明 (`prompts/`)

為了讓你在自動化生成腳本（如 ComfyUI、Python API batch runner）中無需手動拆解字串，`prompts/json/keyframes_99.json` 與 `prompts/csv/keyframes_99.csv` 已經為每一張關鍵幀預先分離出三種可直接投餵的 Prompt 欄位：

- `prompt_heroine_lambda_1`：已自動移除 `OR (Mode λ_H=0 ...)` 分支，純粹保留 **有女主模式 ($\lambda_H=1$)** 描述。
- `prompt_abstract_lambda_0`：已自動移除 `(Mode λ_H=1 ...) OR` 分支，純粹保留 **無女主純抽象幾何模式 ($\lambda_H=0$)** 描述。
- `prompt_dual`：保留完整雙模態同構對照描述。
