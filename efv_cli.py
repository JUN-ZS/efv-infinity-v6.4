#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EFV∞《永不退電的一朵花》V6.4 互動式 Prompt 檢索與雙模態切換 CLI 工具 (efv_cli.py)

支援功能：
  1. 列出全曲 11 個 SET 段落、原詞、編曲標籤與 BPM 資訊：`python3 efv_cli.py list`
  2. 檢索指定 SET 的所有 Prompt（九宮格母圖 + 9張關鍵幀 + 8段運鏡 + 跨SET橋接）：
     `python3 efv_cli.py set 1 --mode heroine`
  3. 精準查詢單一 Prompt ID（支援雙模態 / 有女主 λ_H=1 / 無女主純抽象 λ_H=0）：
     `python3 efv_cli.py get SET_01_K01_1080P --mode abstract`
  4. 依關鍵字或原詞搜尋對應鏡號與 Prompt：
     `python3 efv_cli.py search "沙漏"`
  5. 一鍵匯出純文字 Prompt 清單（供 Midjourney / Flux / Runway / Kling / Veo 批次生成）：
     `python3 efv_cli.py export --type keyframes --mode heroine --out batch_keyframes_heroine.txt`
"""

import argparse
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MANIFEST_CANDIDATES = [
    os.path.join(BASE_DIR, "prompts", "json", "efv_v6_4_prompts_manifest.json"),
    os.path.join(BASE_DIR, "efv_v6_4_prompts_manifest.json"),
]


def load_manifest() -> dict:
    for path in MANIFEST_CANDIDATES:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    sys.exit("❌ 找不到 efv_v6_4_prompts_manifest.json，請確認工作目錄。")


def select_mode_prompt(item: dict, mode: str) -> str:
    if mode == "heroine":
        return (
            item.get("prompt_heroine_lambda_1")
            or item.get("prompt_dual")
            or item.get("prompt")
            or ""
        )
    elif mode == "abstract":
        return (
            item.get("prompt_abstract_lambda_0")
            or item.get("prompt_dual")
            or item.get("prompt")
            or ""
        )
    return item.get("prompt_dual") or item.get("prompt") or ""


def cmd_list(data: dict) -> None:
    print("=" * 100)
    print(f"🌸 {data.get('project', 'EFV∞ V6.4')}｜全曲 11 SET 總覽 (共 209 組 Prompt)")
    print("=" * 100)
    for s in data["sets"]:
        print(f"• [{s['set_id']}] {s['title']}")
        print(f"  ├─ 編曲導引標籤: {s['arrangement_tag']}")
        lyrics_preview = " / ".join([line.strip() for line in s["verbatim_lyrics"] if line.strip() and not line.strip().startswith('[')])
        print(f"  └─ 定稿原詞: {lyrics_preview}")
    print("=" * 100)


def cmd_set(data: dict, set_num: int, mode: str) -> None:
    set_id = f"SET_{set_num:02d}"
    set_meta = next((s for s in data["sets"] if s["set_id"] == set_id), None)
    if not set_meta:
        sys.exit(f"❌ 找不到 {set_id}（請輸入 1 ~ 11）")

    print("=" * 100)
    print(f"🎬 [{set_id}] {set_meta['title']}  (Mode: {mode})")
    print(f"🎵 編曲標籤: {set_meta['arrangement_tag']}")
    print("📜 本段完整原詞:")
    for line in set_meta["verbatim_lyrics"]:
        print(f"   > {line}")
    print("=" * 100)

    mg = next((m for m in data["master_grids"] if m["set_id"] == set_id), None)
    if mg:
        print(f"\n[1] 九宮格母圖 ({mg['id']}):")
        print(f"    {select_mode_prompt(mg, mode)}")

    kfs = [k for k in data["keyframes_1080p"] if k["set_id"] == set_id]
    print(f"\n[2] 1080P 關鍵幀 ({len(kfs)} 張):")
    for k in kfs:
        print(f"  • [{k['id']}] ({k.get('title', '')} | {k.get('phase', '')})")
        print(f"    {select_mode_prompt(k, mode)}")

    mps = [m for m in data["intra_set_morphs"] if m["set_id"] == set_id]
    print(f"\n[3] SET 內首尾幀連續運鏡影片 ({len(mps)} 段):")
    for m in mps:
        print(f"  • [{m['id']}] ({m.get('transition', '')})")
        print(f"    {select_mode_prompt(m, mode)}")

    br = next((b for b in data["inter_set_bridges"] if b.get("from_set") == set_id), None)
    if br:
        print(f"\n[4] 跨 SET 伏筆交接影片 ({br['id']}):")
        print(f"    {select_mode_prompt(br, mode)}")


def cmd_get(data: dict, prompt_id: str, mode: str) -> None:
    target = prompt_id.strip().upper()
    all_items = (
        data["master_grids"]
        + data["keyframes_1080p"]
        + data["intra_set_morphs"]
        + data["inter_set_bridges"]
    )
    for item in all_items:
        if item["id"].upper() == target:
            print(select_mode_prompt(item, mode))
            return
    sys.exit(f"❌ 找不到 Prompt ID: {prompt_id}")


def cmd_search(data: dict, keyword: str, mode: str) -> None:
    kw = keyword.lower()
    all_items = (
        data["master_grids"]
        + data["keyframes_1080p"]
        + data["intra_set_morphs"]
        + data["inter_set_bridges"]
    )
    matches = [
        item for item in all_items
        if kw in json.dumps(item, ensure_ascii=False).lower()
    ]
    print(f"🔍 關鍵字「{keyword}」共找到 {len(matches)} 筆結果 (Mode: {mode})：")
    for item in matches:
        label = item.get("title") or item.get("transition") or item.get("set_id", "")
        print(f"\n• [{item['id']}] ({label})")
        print(f"  {select_mode_prompt(item, mode)}")


def cmd_export(data: dict, ptype: str, mode: str, out_path: str) -> None:
    bucket_map = {
        "all": data["master_grids"] + data["keyframes_1080p"] + data["intra_set_morphs"] + data["inter_set_bridges"],
        "grids": data["master_grids"],
        "keyframes": data["keyframes_1080p"],
        "morphs": data["intra_set_morphs"],
        "bridges": data["inter_set_bridges"],
    }
    items = bucket_map[ptype]
    lines = []
    for item in items:
        lines.append(f"# [{item['id']}]")
        lines.append(select_mode_prompt(item, mode))
        lines.append("")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ 已成功匯出 {len(items)} 組 Prompt (type={ptype}, mode={mode}) 至: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="EFV∞ V6.4 Prompt 檢索與雙模態切換 CLI 工具")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="列出全曲 11 個 SET 段落、編曲標籤與定稿原詞")

    p_set = sub.add_parser("set", help="檢索指定 SET (1~11) 的完整 Prompt")
    p_set.add_argument("number", type=int, help="SET 編號 (1 ~ 11)")
    p_set.add_argument("--mode", choices=["dual", "heroine", "abstract"], default="dual")

    p_get = sub.add_parser("get", help="透過 Prompt ID 取得單一 Prompt")
    p_get.add_argument("id", type=str, help="例如 SET_01_K01_1080P 或 SET_01_p00_MORPH")
    p_get.add_argument("--mode", choices=["dual", "heroine", "abstract"], default="dual")

    p_search = sub.add_parser("search", help="搜尋包含指定原詞或關鍵字的 Prompt")
    p_search.add_argument("keyword", type=str, help="搜尋關鍵字，例如：沙漏、靜電、DU")
    p_search.add_argument("--mode", choices=["dual", "heroine", "abstract"], default="dual")

    p_export = sub.add_parser("export", help="批次匯出指定類型的 Prompt 清單")
    p_export.add_argument("--type", choices=["all", "grids", "keyframes", "morphs", "bridges"], default="all")
    p_export.add_argument("--mode", choices=["dual", "heroine", "abstract"], default="heroine")
    p_export.add_argument("--out", type=str, default="exported_prompts.txt")

    args = parser.parse_args()
    data = load_manifest()

    if args.cmd == "list":
        cmd_list(data)
    elif args.cmd == "set":
        cmd_set(data, args.number, args.mode)
    elif args.cmd == "get":
        cmd_get(data, args.id, args.mode)
    elif args.cmd == "search":
        cmd_search(data, args.keyword, args.mode)
    elif args.cmd == "export":
        cmd_export(data, args.type, args.mode, args.out)


if __name__ == "__main__":
    main()
