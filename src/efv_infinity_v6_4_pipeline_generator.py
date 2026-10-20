#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EFV∞《永不退電的一朵花》V6.4 終極原詞與編曲標籤全對位規格書 & 自動化編譯器
Upgrades V6.3 spec to V6.4 by integrating the exact verbatim lyrics and arrangement prompt tags
across all 11 SETs, 99 Keyframes, 88 Intra-SET Morphs, and 11 Inter-SET Bridges.

Paths (repo-relative; override with env EFV_INPUT_MD / EFV_OUTPUT_MD):
  INPUT  : docs/efv_infinity_v6_3_base.md
  OUTPUT : docs/efv_infinity_v6_4_chaincontinuity_1080p_full_spec.md
"""
import hashlib
import json
import os
import re

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_MD = os.environ.get(
    "EFV_INPUT_MD",
    os.path.join(_BASE, "docs", "efv_infinity_v6_3_base.md"),
)
OUTPUT_MD = os.environ.get(
    "EFV_OUTPUT_MD",
    os.path.join(_BASE, "docs", "efv_infinity_v6_4_chaincontinuity_1080p_full_spec.md"),
)
OUTPUT_PY = os.path.join(_BASE, "src", "efv_infinity_v6_4_pipeline_generator.py")

# 1. Define the Verbatim Lyrics, Arrangement Directives, BPMs, and 9-Cell Lyric-Cue Mappings for all 11 SETs
SET_V64_CONFIG = {
    1: {
        "title_header": "## SET_01｜靜電沉降・斷訊之中仍不退電的一朵花 (Intro｜58 BPM ➔ Hard Cut｜4/4)",
        "section_tag": '[ "Intro: 58 BPM. Sparse electric piano, low synth haze, a soft pulse that never fully lands. Tiny glassy accents drift at the edges." ] ➔ [ "Hard Cut" ]',
        "tempo_short": "58 BPM ➔ Hard Cut",
        "tempo_bridge_from": "Post-Outro Cold Stop (0 BPM) ➔ 58 BPM",
        "tempo_bridge_to": "58 BPM (Hard Cut) ➔ 62 BPM",
        "verbatim_lyrics_block": (
            '[ "Intro: 58 BPM. Sparse electric piano, low synth haze, a soft pulse that never fully lands. Tiny glassy accents drift at the edges." ]\n'
            '靜电—沉降\n'
            '声断连—\n'
            '闪烁的印記 灑落——\n'
            '永不退電的一朵—花\n'
            '[ "Hard Cut" ]'
        ),
        "speed_mode": "58 BPM 懸浮慢脈搏 ➔ 結尾 [ \"Hard Cut\" ] 瞬間硬切｜Sparse electric piano 疏落電鋼琴單音起落 × Low synth haze 低頻合成器迷霧鋪底 × A soft pulse that never fully lands 從不完全落地的輕柔脈搏 × Tiny glassy accents 邊緣漂移的細碎玻璃泛音。",
        "timbre": "58 BPM 稀疏電鋼琴（Sparse Electric Piano）＋ 低頻合成器迷霧（Low Synth Haze）＋ 邊緣漂移細碎玻璃泛音（Tiny Glassy Accents）＋ 結尾 [ \"Hard Cut\" ] 斷訊硬切。",
        "cells_lyric_sync": [
            ("「靜电—」", "58 BPM Sparse electric piano (疏落電鋼琴第一聲單音與靜電雪浮現)"),
            ("「—沉降 / 声断连—」", "Low synth haze & broken connection (低頻合成器迷霧中斷銅線微弧隔空連綴)"),
            ("「闪烁的印記」", "Tiny glassy accents drift at the edges (邊緣漂移玻璃泛音壓出閃爍無字光印)"),
            ("「灑落——」", "A soft pulse that never fully lands (從不完全落地的輕柔脈搏凝為琥珀花心)"),
            ("「永不退電的—」(前導氣口)", "Sparse electric piano & low synth haze swell (電鋼琴疏落和弦與低頻迷霧共振擴散)"),
            ("「—一朵—」", "Glassy accents reflection on rain window (細碎玻璃泛音於雨窗映出微笑暖弧/新月弧)"),
            ("「永不退電的一朵—花」", "Unlanding soft pulse illuminates unplugged socket (無源空插槽自發亮起，永不退電)"),
            ("「—花」(尾音灑落)", "Glassy accents & synth haze radiation (缺口光環向外灑落玻璃泛音光網)"),
            ('[ "Hard Cut" ]', "Abrupt Hard Cut at 58 BPM end -> Verse 1 (58 BPM 懸浮尾音瞬間硬切接入 62 BPM 霓虹脈絡)"),
        ],
    },
    2: {
        "title_header": "## SET_02｜午夜金屬・曲折重載・精準呼吸與輕哼 (Verse 1 (Part A)｜62 BPM｜4/4)",
        "section_tag": '[ "Verse 1: 62 BPM. Thin groove, brushed percussion, sub bass holding back. Voice stays close, almost conversational, with a few breathy lifts." ]',
        "tempo_short": "62 BPM",
        "tempo_bridge_to": "62 BPM ➔ 62 BPM (Verse 1 Part B)",
        "verbatim_lyrics_block": (
            '[ "Verse 1: 62 BPM. Thin groove, brushed percussion, sub bass holding back. Voice stays close, almost conversational, with a few breathy lifts." ]\n'
            '——霓虹脉络流淌在——午夜的各金属下——\n'
            '我在網格——曲折—重載間—漫步— (huh-hum!) [ "humming" ]\n'
            '你的精准呼吸，記下了分秒'
        ),
        "speed_mode": "62 BPM (纖細律動・近距私語人聲與氣音上揚)｜Thin groove 纖細律動骨架 × Brushed percussion 刷製打擊樂輕刷金屬 × Sub bass holding back 克制隱忍的超低音；人聲保持極近距離（Close, almost conversational），穿插幾處氣音上揚（Breathy lifts）與 `(huh-hum!) [ \"humming\" ]` 鼻音輕哼。",
        "timbre": "62 BPM 纖細律動（Thin Groove）＋ 刷製打擊樂（Brushed Percussion）＋ 克制隱忍 Sub-bass ＋ 近距對話式人聲與 `(huh-hum!) [ \"humming\" ]` 氣音輕哼。",
        "cells_lyric_sync": [
            ("「——霓虹脉络流淌在——」", "62 BPM Thin groove & sub bass holding back (克制低音與纖細律動下黑鉻霓虹脈流淌)"),
            ("「——午夜的各金属下—— / 我在網格——」", "Brushed percussion over metallic grid (刷製打擊樂輕刷午夜各金屬下的受壓網格橋)"),
            ("「——曲折—重載間—漫步—」", "Close conversational voice & delayed step (近距對話感人聲，在曲折重載間踏出慢半拍靴底光)"),
            ('「(huh-hum!) [ "humming" ]」', "Breathy lift & intimate humming (貼耳氣音上揚與輕哼吐出溫熱半圓呼吸白霧環)"),
            ("「你的精准呼吸，」", "Brushed percussion tic-tak pulse (精準呼吸化為無數字刻度的懸浮光點矩陣)"),
            ("「記下了分秒」(前段・詩眼)", "Humming warmth & breathy lift thread (輕哼餘韻化為重載夜風中微揚的風衣暖金縫線)"),
            ("「曲折—重載間」對位「精准呼吸」", "Held-back sub bass tension vs. breath arc (克制超低音重載壓迫下，同心呼吸光弧堅韌回彈)"),
            ("「記下了分秒」(後段・滲光)", "Thin groove seeping through cold metal seam (62 BPM 纖細律動與微暖光穿透冰冷堡壘門縫)"),
            ("Verse 1A ➔ 1B 呼吸轉磁帶交接", "Breathy humming mist wheel -> Tape spindle (精準呼吸白霧捲為同軸霧輪，交接塵封磁帶機)"),
        ],
    },
    3: {
        "title_header": "## SET_03｜底噪磁帶・昔日凝視・溫柔脈搏穿堡 (Verse 1 (Part B)｜62 BPM｜4/4)",
        "section_tag": '[ "Verse 1: 62 BPM. Thin groove, brushed percussion, sub bass holding back. Voice stays close, almost conversational, with a few breathy lifts." ] (Part B)',
        "tempo_short": "62 BPM",
        "tempo_bridge_to": "62 BPM ➔ 64–138 BPM (Pre-Chorus Accelerando)",
        "verbatim_lyrics_block": (
            '底噪的磁带悄然泛起(喚起)——昔日沉睡的凝視\n'
            '一道溫柔的脉搏，正穿透这冰冷堡垒'
        ),
        "speed_mode": "62 BPM (底噪磁帶甦醒・溫柔脈搏穿透聲學堡壘)｜延續 62 BPM Thin groove 與 Brushed percussion（刷鼓聲與類比磁帶底噪無縫同構），Sub-bass 在地底深處克制蓄力，近距人聲在「泛起(喚起)」處帶出雙層氣音上揚（Breathy lift），化為穿透冰冷堡壘的溫柔脈搏。",
        "timbre": "老磁帶氧化層底噪（Tape Hiss）＋ 62 BPM 刷製打擊樂 ＋「泛起(喚起)」雙層氣音疊影 ＋ 穿透混凝土厚牆的溫暖紅金合成器暗脈。",
        "cells_lyric_sync": [
            ("「底噪的磁带—」", "62 BPM Brushed percussion & tape hiss awakening (刷鼓與底噪同構，喚醒塵封磁帶轉盤)"),
            ("「—悄然泛起(喚起)——」", "Breathy lift on \"泛起(喚起)\" (伴隨「泛起/喚起」雙層氣音上揚，帶面泛起閃光磁粉弧)"),
            ("「——昔日沉睡的凝視」", "Close conversational gaze & sub bass depth (氧化磁粉於帶面匯聚為昔日沉睡的凝視光瞳)"),
            ("「底噪」化為白氣絲", "Analog tape hiss filaments in 62 BPM groove (磁帶底噪化為發光白蠶絲，種下穿牆韌性伏筆)"),
            ("「一道溫柔的脉搏，」", "Warm pulse over held-back sub bass (一道溫柔紅金光脈直接穿透多層混凝土裝甲切面)"),
            ("「正穿透—」", "Thin groove illuminating parallel corridor lamps (堡壘內雙側孤燈隨 62 BPM 脈搏錯位亮起)"),
            ("「—这冰冷堡垒」(時間差疊影)", "Breathy lift shadow-lead hand (「泛起/喚起」時間差疊影手比本體快半拍伸出斷崖)"),
            ("「穿透这冰冷堡垒」(跨空成橋)", "Glowing tape ribbon & pulse suspension bridge (發光磁帶與溫柔脈搏交織為跨空懸索光橋)"),
            ("Verse 1 ➔ Pre-Chorus 齒輪壓頂交接", "62 BPM bridge end meeting 64 BPM gear rim (磁帶橋盡頭上方浮現巨型齒輪外環，預備 64→138 BPM 急加速)"),
        ],
    },
    4: {
        "title_header": "## SET_04｜冷漠運轉・只量承受多久 (Pre-Chorus｜64 → 138 BPM｜Fast Tightening & Climbing Tension)",
        "section_tag": '[ "Pre-Chorus: 64 to 138 BPM. The pattern tightens fast; percussion stacks, synths lean forward, tension keeps climbing." ]',
        "tempo_short": "64 → 138 BPM",
        "tempo_bridge_to": "138 BPM ➔ 140 BPM (Chorus Full Lift)",
        "verbatim_lyrics_block": (
            '[ "Pre-Chorus: 64 to 138 BPM. The pattern tightens fast; percussion stacks, synths lean forward, tension keeps climbing." ]\n'
            '运转从未过问我们为何存在\n'
            '只在乎我们究竟能承受多久的运——转——'
        ),
        "speed_mode": "64 → 138 BPM (節奏型急速收緊・打擊樂堆疊・合成器前傾・張力持續攀升)｜由 64 BPM 一路狂飆收緊至 138 BPM（The pattern tightens fast）；打擊樂逐層密集堆疊（Percussion stacks），合成器音牆大幅向前傾壓（Synths lean forward），戲劇與聲學張力持續攀升至副歌臨界點（Tension keeps climbing）。",
        "timbre": "64→138 BPM 急速收緊節奏型 ＋ 層層堆疊打擊樂（Stacked Percussion）＋ 前傾加壓合成器（Forward-Leaning Synths）＋ 臨界高壓共振。",
        "cells_lyric_sync": [
            ("「运转—」", "64→74 BPM The pattern tightens fast (節奏型開始迅速收緊，天頂黑鋼巨齒輪壓下)"),
            ("「—从未过问—」", "74→86 BPM Percussion stacks (打擊樂層層堆疊切入，無字耐受計時圈頓挫縮緊)"),
            ("「—我们为何存在」", "86→98 BPM Cold spindle vs. vocal question (光滑無臉冷鉻轉軸切開倒影，從不過問存在意義)"),
            ("「只在乎—」", "98→110 BPM Synths lean forward (合成器大幅前傾加壓，激起同軸暗紅抗壓波紋)"),
            ("「—我们究竟—」", "110→120 BPM Stacked percussion & synth stabs (堆疊打擊樂縫隙中炸開高能金色閃光斑)"),
            ("「—能承受多久的—」", "120→128 BPM Tension keeps climbing — counter-stop (張力攀升中逆向急停半步擦出金白火花)"),
            ("「—运——」", "128→134 BPM Overloaded structural resonance (134 BPM 鋼構在堆疊鼓與前傾合成器下劇烈共振)"),
            ("「——转——」", "134→138 BPM Peak climbing tension silhouette (138 BPM 臨界高壓下垂手靜立，放棄向系統求問)"),
            ("「运——转——」尾音衝入 140 BPM", "138→140 BPM Full lift slingshot threshold (胸口撕開純白閃光弧，全速撞開 140 BPM 副歌)"),
        ],
    },
    5: {
        "title_header": "## SET_05｜沉默腳本・心促讚歌・殘缺呼吸再次載入 (Chorus 1｜140 BPM｜Full Lift & Forward-Driving Hook)",
        "section_tag": '[ "Chorus: 140 BPM. Full lift, wide drums, bright brass layers, guitars opening up hard. Keep the hook direct and forward-driving." ]',
        "tempo_short": "140 BPM",
        "tempo_bridge_to": "140 BPM ➔ 65 BPM (Hard Drop to Break)",
        "verbatim_lyrics_block": (
            '[ "Chorus: 140 BPM. Full lift, wide drums, bright brass layers, guitars opening up hard. Keep the hook direct and forward-driving." ]\n'
            '当自我遗忘了沉默的脚本，\n'
            '节奏低吟出心促—的赞歌——\n'
            '不再是光芒里纯粹的折算，\n'
            '而是带着残缺、深沉的每一次呼吸。\n'
            '在苦甜参半的深夜里—— (EH)，\n'
            '我们又—載——入再次启程。'
        ),
        "speed_mode": "140 BPM (全面升空 Full Lift・寬廣鼓組・明亮銅管層・吉他猛烈大開)｜140 BPM 第一個副歌能量峰值！寬廣鼓組（Wide drums）、明亮銅管疊層（Bright brass layers）與猛烈大開的電吉他（Guitars opening up hard）全面托起；主旋律 Hook 保持直接且強勁向前驅動（Direct and forward-driving）。",
        "timbre": "140 BPM 寬廣立體鼓組（Wide Drums）＋ 明亮合成銅管層（Bright Brass Layers）＋ 猛烈大開電吉他（Hard-Opening Guitars）＋ `(EH)` 氣音切分。",
        "cells_lyric_sync": [
            ("「当自我遗忘了沉默的脚本，」", "140 BPM Full lift & wide drums (140 BPM 全面升空與寬廣鼓組，雨夜多重玻璃幕牆中掙脫沉默腳本)"),
            ("「节奏低吟出心促—的赞歌——」", "Bright brass layers & direct hook (明亮銅管層與直接向前驅動的主旋律，點亮胸口心促讚歌脈)"),
            ("「不再是光芒里纯粹的折算，」", "Guitars opening up hard (電吉他猛烈大開，45度蜜金斜光劈開暗巷折算格線)"),
            ("「而是带着残缺、深沉的每一次呼吸。」", "Deep breath over wide drums & sub bass (寬廣鼓組支撐下呼出殘缺卻深沉的暖金呼吸霧團)"),
            ("「在苦甜参半的深夜里——」", "Brass & guitar reflections in midnight water (苦甜參半的深夜積水同時映出冷青霓虹與暖金銅管光)"),
            ("「—— (EH)，」", "Direct vocal \"(EH)\" accent on rain glass (標誌性「(EH)」氣音切分將積水倒影翻轉躍上雨夜車窗)"),
            ("「我们又—載——入—」", "140 BPM Full lift climax — self-reloading flower (鼓、銅管、吉他全開巔峰，掌心琥珀玻璃花自主再次載入)"),
            ("「—再次启程。」", "Forward-driving 140 BPM streak (140 BPM 直接向前驅動的流光奔影衝出畫框再次啟程)"),
            ("140 BPM ➔ 65 BPM Hard Drop 臨界斷崖", "140→65 BPM Hard drop freeze threshold (140 BPM 熾金光軌在瞬間被截斷凍結為靜電銀霜，直墜 65 BPM Break)"),
        ],
    },
    6: {
        "title_header": "## SET_06｜靜電重返・聲斷連・裸脈與單一延音和弦 (Break｜Hard Drop to 65 BPM｜Bare Pulse & Air Around Vocal)",
        "section_tag": '[ "Break: Hard drop to 65 BPM. Strip everything back to a bare pulse, a single sustained chord, and air around the vocal." ]',
        "tempo_short": "140 → 65 BPM (Hard Drop)",
        "tempo_bridge_to": "65 BPM (Break) ➔ 65 BPM (Verse 2 Denser Low End)",
        "verbatim_lyrics_block": (
            '[ "Break: Hard drop to 65 BPM. Strip everything back to a bare pulse, a single sustained chord, and air around the vocal." ]\n'
            '靜电—沉降\n'
            '声断连—(降)——(连)——(降)(断)'
        ),
        "speed_mode": "140 → 65 BPM (Hard Drop 驟降斷崖・剝離一切僅留裸脈搏與單一延音和弦)｜從 140 BPM 瞬間驟降至 65 BPM（Hard drop to 65 BPM）；剝離所有寬廣鼓組、銅管與吉他音牆（Strip everything back），僅留極簡赤裸脈搏（A bare pulse）、單一延音和弦（A single sustained chord）與人聲周圍透明的空氣感（Air around the vocal）。",
        "timbre": "65 BPM 極簡赤裸脈搏（Bare Pulse）＋ 單一延音和弦（Single Sustained Chord）＋ 人聲周圍透明空氣感（Air Around the Vocal）＋「(降)——(连)——(降)(断)」空間切分。",
        "cells_lyric_sync": [
            ('[ "Break: Hard drop to 65 BPM" ] / 「靜电—」', "140→65 BPM Hard drop, strip everything back (驟降至 65 BPM 剝離一切音牆，靜電銀霜花在真空中緩降)"),
            ("「—沉降」", "Air around the vocal & bare pulse filament (人聲周圍包裹透明空氣感，極細沉降銀絲隨裸脈搏垂直下墜)"),
            ("「声断连—」", "Bare pulse spanning empty space (65 BPM 赤裸脈搏跨越空曠深淵，跨空細微光橋時斷時連)"),
            ("「—(降)——」", "A single sustained chord levitating amber dust (單一延音和弦如溫柔掌心托底，琥珀花心微塵逆重力聚攏)"),
            ("「——(连)——」", "Sustained chord harmonics & bare pulse ring (延音和弦泛音在虛空中重新連起無字半透明古銅光環)"),
            ("「——(降)」(水面遠距回聲)", "Air around the vocal skimming mirror water (人聲周圍空氣感掠過薄水鏡面，倒影與遠影虛實對望)"),
            ("「(断)」(肩頭霜花落定)", "Bare pulse heartbeat cut on \"(断)\" (在「(断)」字切分處，裸脈搏如心跳般將暖珀霜花落定肩頭)"),
            ("Break 尾韻：不滅玻璃花心", "65 BPM Single sustained chord inside crystal core (透明玻璃花瓣包裹熾熱琥珀花心，在延音和弦中不滅)"),
            ("65 BPM Break ➔ Verse 2 低音湧動交接", "Bare pulse diving into 65 BPM denser low-end tide (玻璃花根潮絲刺入透明地面，交接 Verse 2 濃密低音暗潮)"),
        ],
    },
    7: {
        "title_header": "## SET_07｜低音湧動・敲碎沙漏・已淘汰文件夾與導線溫度 (Verse 2｜65 BPM｜Denser Low End & Static)",
        "section_tag": '[ "Verse 2: 65 BPM. Denser low end, rougher edges, more movement in the bassline and percussion, like the track has picked up static." ]',
        "tempo_short": "65 BPM",
        "tempo_bridge_to": "65 BPM ➔ Suspended Weightless Bridge",
        "verbatim_lyrics_block": (
            '[ "Verse 2: 65 BPM. Denser low end, rougher edges, more movement in the bassline and percussion, like the track has picked up static." ]\n'
            '心情浮沉如低音涌动\n'
            '如潮汐玻璃下——\n'
            '故障打擊樂敲碎了沙漏的流轉——\n'
            '我將名字留在一個標為“已淘汰”的文件夾中\n'
            '卻發現它正以更慢的節拍閃著微光\n'
            '未來降臨得如此疲憊—— (huh)\n'
            '於是我們學會了，如何感知導線的溫度'
        ),
        "speed_mode": "65 BPM (更濃密低頻・更粗糙邊緣・貝斯與打擊樂更具動感如拾取靜電)｜維持 65 BPM 慢速，但注入更濃密深沉的低頻（Denser low end）、更粗糙的音色邊緣（Rougher edges），貝斯線與打擊樂展現更多游走動感（More movement in the bassline and percussion），整首曲子彷彿吸附了真實的靜電顆粒（Like the track has picked up static）。",
        "timbre": "65 BPM 濃密湧動低音（Denser Moving Bassline）＋ 粗糙靜電顆粒邊緣（Rougher Static Edges）＋ 故障打擊樂（Glitch Percussion）＋ 慢節拍淘汰文件夾微光與導線熱輻射。",
        "cells_lyric_sync": [
            ("「心情浮沉如低音涌动」", "65 BPM Denser low end & moving bassline tide (濃密低音與流動貝斯線在腳下玻璃地面深處翻湧)"),
            ("「如潮汐玻璃下——」", "Rougher edges & static-charged cracked glass (粗糙邊緣與拾取靜電的質感，潮汐玻璃裂紋映出雙重折影)"),
            ("「故障打擊樂敲碎了沙漏的流轉——」", "Glitch percussion shattering the hourglass (故障打擊樂敲碎玻璃沙漏，流沙在靜電中違反重力凝滯)"),
            ("「我將名字留在一個標為“已淘汰”的文件夾中」", "Archiving into the obsolete folder (發光流沙滑入標為「已淘汰」的無字舊文件夾/封套)"),
            ("「卻發現它正以更慢的節拍閃著微光」", "Glowing at a tempo slower than 65 BPM (文件夾內的琥珀記憶盒以比 65 BPM 更慢的節拍閃著微光)"),
            ("「未來降臨得如此疲憊—— (huh)」", "Weary \"(huh)\" exhale in static-charged fog (白灰靜電濃霧中一聲疲憊真實的「(huh)」嘆息氣口)"),
            ("「於是我們學會了，如何感知導線的溫度」", "Sensing the thermal radiation of the glowing wire (手背/霧滴隔著幾毫米空氣感知橙金導線的真實溫度)"),
            ("導線溫度染金懸停沙漏裂片", "Static-charged golden hourglass shards levitating (65 BPM 故障碎拍中染上導線暖金的沙漏裂片靜止懸停)"),
            ("Verse 2 ➔ Suspended Bridge 邊界交接", "Warm fingertips touching the weightless night boundary (帶著導線餘溫觸碰透明夜色邊界牆，交接失重 Bridge)"),
        ],
    },
    8: {
        "title_header": "## SET_08｜夜色釋懷・無宏大藍圖・溫柔抗拒與最後推進 (Bridge｜Suspended Weightless ➔ Last Push to 160 BPM)",
        "section_tag": '[ "Bridge: Suspended, almost weightless. Leave space between phrases; let the harmony breathe before the last push." ]',
        "tempo_short": "65 BPM 懸置失重 → 160 BPM Last Push",
        "tempo_bridge_to": "Last Push (160 BPM) ➔ 160 BPM (Chorus 2 Release Valve)",
        "verbatim_lyrics_block": (
            '[ "Bridge: Suspended, almost weightless. Leave space between phrases; let the harmony breathe before the last push." ]\n'
            '夜色中的释怀\n'
            '没有宏大的蓝图\n'
            '只有温柔的抗拒——\n'
            '拒绝永远停留在边界之内'
        ),
        "speed_mode": "前半懸置失重（Suspended, almost weightless・樂句留白與和聲呼吸）➔ 後半最後推進（Before the last push：65 → 160 BPM 蓄力衝刺）｜前半段（格01–04）懸置且近乎失重，在樂句之間留出充裕空間（Leave space between phrases），讓和聲自由呼吸（Let the harmony breathe）；後半段（格05–09）啟動最後推進（The last push），將速度與張力一路推向 160 BPM 最終副歌洩壓閥！",
        "timbre": "前半：失重懸置透明和聲（Weightless Breathing Harmony）＋ 樂句間深空留白；後半：65→160 BPM 最後推進（The Last Push）點火加速。",
        "cells_lyric_sync": [
            ("「夜色中的释怀」", "Suspended, almost weightless night boundary (懸置失重的透明夜色邊界牆，樂句間留出深邃呼吸空間)"),
            ("「没有宏大的蓝图」", "Leave space between phrases — unmapped starlight (樂句留白間無任何系統宏大藍圖，唯見自由散光絲)"),
            ("「只有温柔的抗拒——」(貼界呼吸)", "Let the harmony breathe across glass (和聲在透明邊界內外自由呼吸，手掌平穩貼合玻璃邊界)"),
            ("「只有温柔的抗拒——」(穿縫滲霧)", "Gentle resistance mist seeping through 1mm seam (溫柔抗拒金霧從 1mm 玻璃細縫堅定滲向牆外夜空)"),
            ("「拒绝永远停留在—」(Before the last push 點火)", "The last push ignition (65→105 BPM) (最後推進正式點火，紅白聲波在邊界縫隙炸亮奇點)"),
            ("「—边界之内」(加速破風尖絲)", "105→130 BPM Last push acceleration (溫柔微笑弧線在加速推進中拉長為破風金色流光尖絲)"),
            ("「拒绝永远停留在边界之内」(跨出一寸)", "130→148 BPM Stepping one inch beyond the boundary (靴尖/光楔正式跨出邊界線一寸，震碎圍牆)"),
            ("Last Push 臨界透光 (148→156 BPM)", "148→156 BPM Luminous hand piercing barrier (整隻手掌化為半透明白金光體完全穿透邊界屏障)"),
            ("160 BPM Release Valve 衝天交接", "160 BPM Release valve sky-rocket stem (巨型發光花莖破界瘋長直衝雲霄，頂入 160 BPM 最終副歌)"),
        ],
    },
    9: {
        "title_header": "## SET_09｜躍下的讚歌・光穿呼吸・非運轉錯誤的微風數字 (Chorus 2｜160 BPM｜Bigger, Wider, Overloaded Release Valve)",
        "section_tag": '[ "Chorus 2: 160 BPM. Bigger, wider, more overloaded. Everything feels opened to the top end; final chorus should hit like a release valve." ]',
        "tempo_short": "160 BPM",
        "tempo_bridge_to": "160 BPM ➔ Outro (Decay and Dissolve)",
        "verbatim_lyrics_block": (
            '[ "Chorus 2: 160 BPM. Bigger, wider, more overloaded. Everything feels opened to the top end; final chorus should hit like a release valve." ]\n'
            '当自我——遗忘了沉默的脚本，\n'
            '节奏吟唱出——躍下的赞歌。\n'
            '不是完美的契合，不是严丝合缝的算法——\n'
            '只是让光穿透而入的呼吸。\n'
            '我们不是拒绝终止的运转错误，\n'
            '也不是游荡的\n'
            '模拟的\n'
            '幽灵的\n'
            '微风裡的\n'
            '数字—— (EH)'
        ),
        "speed_mode": "160 BPM (更宏大・更寬廣・更過載・高頻全開如洩壓閥爆發)｜160 BPM 全曲最大能量釋放！音場比第一段副歌更龐大、更寬廣、更過載（Bigger, wider, more overloaded），所有頻段向最高頻徹底敞開（Opened to the top end），整段最終副歌如高壓洩壓閥全面衝開般震撼（Hit like a release valve），並在最後一字「数字—— (EH)」徹底震碎數字符號！",
        "timbre": "160 BPM 超寬過載音牆（Overloaded Wide Wall of Sound）＋ 高頻全開璀璨泛音（Opened Top End）＋ 洩壓閥式爆發（Release Valve Hit）＋「数字—— (EH)」無語義星塵爆破。",
        "cells_lyric_sync": [
            ("「当自我——遗忘了沉默的脚本，」", "160 BPM Bigger, wider, opened to the top end (160 BPM 宏大過載高空，掙脫沉默腳本的錯位方格殘影)"),
            ("「节奏吟唱出——躍下的赞歌。」", "Final chorus hits like a release valve (如洩壓閥全面衝開般，從高空光格主動縱身躍下)"),
            ("「不是完美的契合，不是严丝合缝的算法——」", "Imperfect fit defying the seamless algorithm (落地時與嚴絲合縫的算法故意相差一指寬，裂開生命缺口)"),
            ("「只是让光穿透而入的呼吸。」", "Top-end overloaded light piercing breath (全開的高頻白金光束從缺口噴湧，直接穿透半透明呼吸)"),
            ("「我们不是拒绝终止的运转错误，」", "Not a runtime error — voluntary 1-beat rest (160 BPM 狂飆機械環主動空出一格休止符，非運轉錯誤)"),
            ("「也不是游荡的 / 模拟的」", "Wandering & simulated dual-layer convergence (「游荡的」本體與「模拟的」殘影在過載音場中逼近合一)"),
            ("「幽灵的 / 微风裡的」", "Ghostly silhouettes in the breeze (化為「幽灵的、微风裡的」發光輪廓絲奔向核心奇點)"),
            ("「数字—— (EH)」", "Release valve climax shattering \"数字—— (EH)\" (最後一字「数字——(EH)」引爆漫天無語義純白金微點星塵)"),
            ("160 BPM 巔峰轉入 Decay & Dissolve 交接", "From 160 BPM release valve to decay & dissolve (星塵落回掌心化為不同步琥珀花，節奏開始拆解拉開)"),
        ],
    },
    10: {
        "title_header": "## SET_10｜節奏拆解・低音延展・仍在低鳴至完全靜默 (Outro｜Decay & Dissolve ➔ [ \"Silence\" ])",
        "section_tag": '[ "Outro: Decay and dissolve. Pull the rhythm apart, let the low tones stretch, and let the last echoes thin out to nothing." ] ➔ [ "Silence" ]',
        "tempo_short": "160 BPM → Decay & Dissolve → Silence",
        "tempo_bridge_to": '[ "Silence" ] ➔ Post-Outro (Final Glitch Burst)',
        "verbatim_lyrics_block": (
            '[ "Outro: Decay and dissolve. Pull the rhythm apart, let the low tones stretch, and let the last echoes thin out to nothing." ]\n'
            '……仍在低鸣\n'
            '……仍在低鸣——\n'
            '......——\n'
            '[ "Silence" ]'
        ),
        "speed_mode": "160 BPM → 衰減消融（Decay and dissolve）→ 拆解節奏（Pull the rhythm apart）→ 低音延展（Let the low tones stretch）→ 回聲變薄歸零（Thin out to nothing）→ `[ \"Silence\" ]`｜不作煽情流行收尾，而是將節奏骨架徹底拆解拉開，讓低音無限拉伸延展，最後的回聲一層層變薄直至完全歸零，進入乾淨的 `[ \"Silence\" ]`。",
        "timbre": "拆解拉開的稀疏節奏殘片 ＋ 無限拉伸的暗金低音（Stretched Low Tones）＋ 逐層變薄歸零的回聲（Echoes Thinning to Nothing）＋ `[ \"Silence\" ]` 絕對靜默。",
        "cells_lyric_sync": [
            ("「……仍在低鸣」(第1次)", "Decay and dissolve, pull the rhythm apart (節奏被拆解拉開，只剩琥珀色慢速低鳴光環失重懸浮)"),
            ("「……仍在低鸣」(高頻回聲率先消融)", "High overtones dissolving into silver dust (外圈高頻銀白光環率先衰減消散，僅留內圈低鳴)"),
            ("「……仍在低鸣——」(第2次・低音拉伸)", "Let the low tones stretch (低音無限拉伸延展，兩側城市建築光網向中心退潮隱沒)"),
            ("「——」(拉伸低音懸空長弧)", "Stretched low-tone bronze residual arc (被拉伸的低音在空氣中留下一道懸空古銅色殘響長音弧)"),
            ("「......——」(回聲變薄 Part A：微笑失真)", "Last echoes thinning out into fine gold dust (玻璃上的微笑暖弧隨衰減化為細粒，在黑絲絨中變薄抹除)"),
            ("「......——」(回聲變薄 Part B：雙光靜定)", "Echoes thinning to the chiaroscuro edge (半邊冷銀半邊暖珀在明暗日蝕交界處靜定傾聽最後低鳴)"),
            ("回聲變薄至無形前夕 (Thin out to nothing)", "Monochrome charcoal sketch subtraction (色彩與混響被徹底抽乾，三維世界壓平為炭筆手稿單線)"),
            ("最後一絲延音收束為單銀線", "Last stretched low tone collapsing to a single line (萬物與回聲徹底變薄歸一，收束為橫貫黑場的單一銀線)"),
            ('[ "Silence" ]', "Complete [ \"Silence\" ] before final glitch burst (99.5% 純黑的絕對靜默中唯留極微琥珀奇點，蓄勢待發)"),
        ],
    },
    11: {
        "title_header": "## SET_11｜終極故障爆裂・四相花／華／FLOWER・突發親密 DU—— 與零殘響冷停 (Post-Outro｜Final Glitch Burst ➔ Sudden Abrupt Cold Stop)",
        "section_tag": '[ "Post-Outro: Final glitch burst, then immediate stop. One last fractured tail, then total black." ] ➔ [ "Vocalizing: sudden, intimate" ] DU—— ➔ [ "Sustained Synth Note" ] ➔ [ "Electronic Drone" ] ...— ➔ [ "Sudden Abrupt Cold Stop" ]',
        "tempo_short": "Final Glitch Burst ➔ Immediate Cold Stop",
        "tempo_bridge_to": "Cold Stop (0 BPM) ➔ 58 BPM (SET_01 Intro Moebius Loop)",
        "verbatim_lyrics_block": (
            '[ "Post-Outro: Final glitch burst, then immediate stop. One last fractured tail, then total black." ]\n'
            '—心——斷——連——\n'
            '落塵——穿——透——\n'
            '靜电——沉降——\n'
            '花(華)——(FL—OW—ER——) 花(華)——(FL—OW—ER——) 花(華)——(FL—OW—ER——) 花(華)——(FL—OW—ER——)\n'
            '[ "Vocalizing: sudden, intimate" ]\n'
            'DU——\n'
            '[ "Sustained Synth Note" ]\n'
            '[ "Electronic Drone" ]\n'
            '...—\n'
            '[ "Sudden Abrupt Cold Stop" ]'
        ),
        "speed_mode": "Final Glitch Burst（終極故障爆裂極速彈射）➔ 四次「花(華)——(FL—OW—ER——)」360° 四相閃頻蛻變 ➔ `[ \"Vocalizing: sudden, intimate\" ] DU——` ➔ `[ \"Sustained Synth Note\" ]` ＋ `[ \"Electronic Drone\" ] ...—`（最後一道破碎尾音 One last fractured tail）➔ `[ \"Sudden Abrupt Cold Stop\" ]`（瞬間冷停切入全黑 Total black）！",
        "timbre": "終極故障爆裂（Final Glitch Burst）＋ 四連「花(華)——(FL—OW—ER——)」閃頻對位 ＋ 突發親密人聲「DU——」＋ 延音合成器單音（Sustained Synth Note）＋ 電子低鳴（Electronic Drone `...—`）＋ 零殘響突然冷停（Sudden Abrupt Cold Stop）。",
        "cells_lyric_sync": [
            ('[ "Post-Outro: Final glitch burst" ] / 「—心——斷——連——」', "Final glitch burst ricochet on \"—心——斷——連——\" (破開靜默，終極故障爆裂將心斷連化為極速折線彈射光脈)"),
            ("「落塵——穿——透——」", "Counter-rotating beams piercing falling dust (上行金束與逆行銀束在漫天落塵中交叉穿透成 X 型光軸)"),
            ("「靜电——沉降——」", "Immediate stop before 4-phase flower bloom (靜電微粒瞬間垂直沉降定格於中軸線)"),
            ("第1次「花(華)——(FL—OW—ER——)」", "Phase 1 Circuit Flower (0°➔90° Strobe Orbit) (第1聲綻放為精密發光紫銅電路花)"),
            ("第2次「花(華)——(FL—OW—ER——)」", "Phase 2 Dust Flower (90°➔180° Strobe Orbit) (第2聲震散重組為懸浮琥珀光塵凝聚的落塵花)"),
            ("第3次「花(華)——(FL—OW—ER——)」", "Phase 3 Static Arc Flower (180°➔270° Strobe Orbit) (第3聲高壓電離為銀白紫藍交織的靜電電弧花)"),
            ("第4次「花(華)——(FL—OW—ER——)」", "Phase 4 Living Flower (270°➔360° Extreme Macro) (第4聲完成環繞盛開具真實體溫的半透明琥珀活體花)"),
            ('[ "Vocalizing: sudden, intimate" ] 「DU——」 + [ "Sustained Synth Note" ] + [ "Electronic Drone" ] 「...—」', "Sudden intimate \"DU——\" + Sustained Synth Note & Electronic Drone tail (耳畔突發親密「DU——」與合成器單音、電子低鳴拉出最後破碎尾音)"),
            ('[ "Sudden Abrupt Cold Stop" ] (Total black)', "Sudden Abrupt Cold Stop -> Total black & 1 undischarged speck (零殘響突然冷停切入全黑，唯留一粒微塵迴環至 SET_01 58 BPM)"),
        ],
    },
}


def main() -> None:
    if not os.path.isfile(INPUT_MD):
        raise SystemExit(
            f"❌ 找不到輸入規格書: {INPUT_MD}\n"
            "請確認 docs/efv_infinity_v6_3_base.md 存在，或設環境變數 EFV_INPUT_MD。"
        )

    with open(INPUT_MD, "r", encoding="utf-8") as f:
        orig_text = f.read()

    # Split into Chapter 0 and SET_01..SET_11
    parts = re.split(r"(?=^## SET_\d\d｜)", orig_text, flags=re.M)
    chap0 = parts[0]
    set_blocks = parts[1:]
    assert len(set_blocks) == 11, f"Expected 11 SET blocks, got {len(set_blocks)}"

    # Helper for targeted text replacements inside each SET block
    def upgrade_set_text(set_idx: int, text: str) -> str:
        cfg = SET_V64_CONFIG[set_idx]
        lines = text.splitlines()

        # 1. Replace L00 Header, L02 Speed Mode, L03 Timbre, and inject Verbatim Lyrics Block
        lines[0] = cfg["title_header"]
        lines[2] = (
            f"- **編曲導引標籤（Arrangement Directive Tag）：** `{cfg['section_tag']}`\n"
            f"- **【本段完整原詞（Verbatim Lyrics）】：**\n"
            + "\n".join([f"  > `{l}`" for l in cfg["verbatim_lyrics_block"].splitlines()])
            + f"\n- **速度與律動/聲部模式：** {cfg['speed_mode']}"
        )
        lines[3] = f"- **標誌音色：** {cfg['timbre']}"

        for c_i in range(9):
            lyric_phrase, arr_cue = cfg["cells_lyric_sync"][c_i]

            # Table 1A row is at line 15 + c_i
            row_1a = lines[15 + c_i].split("|")
            old_thesis = row_1a[3].strip()
            old_thesis = old_thesis.replace("168 BPM 機械底盤", "58 BPM 懸浮電鋼琴與低頻合成器迷霧")
            old_thesis = old_thesis.replace("戰鬥號角與擊弦切開死寂，震散金屬冷霧", "疏落電鋼琴和弦與低頻迷霧共振，邊緣漂移細碎玻璃泛音")
            old_thesis = old_thesis.replace("號角震霧：", "電鋼琴泛音霧：")
            old_thesis = old_thesis.replace("168➔175 BPM", "64➔74 BPM")
            old_thesis = old_thesis.replace("195 BPM", "134 BPM")
            old_thesis = old_thesis.replace("196 BPM", "140 BPM" if set_idx == 5 else "138 BPM")
            old_thesis = old_thesis.replace("196➔70 BPM 鼓與銅管瞬間消失", "140➔65 BPM 驟降剝離一切音牆（僅留裸脈搏與延音和弦）")
            old_thesis = old_thesis.replace("Dry Tenor 單線懸垂於 90% 純黑負空間，如聽見赤裸脈搏", "人聲周圍包裹透明空氣感（Air around the vocal），極細沉降銀絲隨 65 BPM 赤裸脈搏下墜")
            old_thesis = old_thesis.replace("管風琴長音如溫柔掌心", "單一延音和弦（Single sustained chord）如溫柔掌心")
            old_thesis = old_thesis.replace("70 BPM", "65 BPM")
            old_thesis = old_thesis.replace("100➔135 BPM", "105➔130 BPM")
            old_thesis = old_thesis.replace("135➔170 BPM", "130➔148 BPM")
            old_thesis = old_thesis.replace("170➔190 BPM", "148➔156 BPM")
            old_thesis = old_thesis.replace("200 BPM", "160 BPM")
            old_thesis = old_thesis.replace("200➔316 BPM", "Final Glitch Burst 極速爆裂")
            row_1a[3] = f" **原詞對位：{lyric_phrase}**<br>{old_thesis} "
            lines[15 + c_i] = "|".join(row_1a)

            # Table 2 row is at line 45 + c_i
            row_t2 = lines[45 + c_i].split("|")
            row_t2[7] = f" **{lyric_phrase}**<br>`{arr_cue}` "
            lines[45 + c_i] = "|".join(row_t2)

            # Table 3 row is at line 59 + c_i
            row_t3 = lines[59 + c_i].split("|")
            metric_lines_part = row_t3[6].strip().split("<br>")
            if c_i < 8:
                next_lyric, next_cue = cfg["cells_lyric_sync"][c_i + 1]
                metric_lines_part[-1] = f"{lyric_phrase} (`{arr_cue.split('(')[0].strip()}`) ➔ {next_lyric} (`{next_cue.split('(')[0].strip()}`)"
            else:
                next_set_idx = (set_idx % 11) + 1
                next_lyric, next_cue = SET_V64_CONFIG[next_set_idx]["cells_lyric_sync"][0]
                metric_lines_part[-1] = f"{lyric_phrase} ➔ 跨段交接 `{SET_V64_CONFIG[next_set_idx]['tempo_short']}`：{next_lyric}"
            row_t3[6] = " " + "<br>".join(metric_lines_part) + " "
            lines[59 + c_i] = "|".join(row_t3)

            # Keyframe Prompt
            k_line_idx = 75 + c_i * 2
            k_prompt = lines[k_line_idx]
            k_prompt = k_prompt.replace(
                "[V6.3 Dramaturgical Phase & Lyrical Abstraction]:",
                f"[V6.4 Dramaturgical Phase, Verbatim Lyric & Arrangement Cue]: Lyric Line: {lyric_phrase} | Arrangement Cue: {arr_cue} —"
            )
            lines[k_line_idx] = k_prompt

            # Morph / Bridge prompts
            if c_i < 8:
                p_line_idx = 94 + c_i * 2
                p_prompt = lines[p_line_idx]
                next_lyric, next_cue = cfg["cells_lyric_sync"][c_i + 1]
                p_prompt = p_prompt.replace(
                    "[V6.3 QCTH-F Dramaturgical Progression & Frontal/Lateral Shift]:",
                    f"[V6.4 QCTH-F Dramaturgical & Lyrical Progression ({lyric_phrase} -> {next_lyric})]:"
                )
                p_prompt = re.sub(
                    r"\[Canon Audio-Visual Sync\]: .*?\. Zero hard cuts",
                    f"[Audio-Visual & Lyrical Sync]: Transitioning from {lyric_phrase} ({arr_cue}) into {next_lyric} ({next_cue}) [{cfg['tempo_short']}]. Zero hard cuts",
                    p_prompt
                )
                lines[p_line_idx] = p_prompt
            else:
                b_line_idx = 110
                b_prompt = lines[b_line_idx]
                next_set_idx = (set_idx % 11) + 1
                next_lyric, next_cue = SET_V64_CONFIG[next_set_idx]["cells_lyric_sync"][0]
                b_prompt = b_prompt.replace(
                    "[V6.3 Inter-SET Foreshadowing Harvest & Operator Shift]:",
                    f"[V6.4 Inter-SET Foreshadowing Harvest & Lyrical Handoff ({lyric_phrase} -> {next_lyric})]:"
                )
                b_prompt = re.sub(
                    r"\[Musical Handoff\]: .*?\. Seamless topological continuity",
                    f"[Musical & Lyrical Handoff]: {lyric_phrase} ({cfg['tempo_short']}) locking into SET_{next_set_idx:02d} opening {next_lyric} ({SET_V64_CONFIG[next_set_idx]['tempo_short']}: {next_cue}). Seamless topological continuity",
                    b_prompt
                )
                lines[b_line_idx] = b_prompt

        lines[72] = lines[72].replace(
            "[V6.3 Lyrical Recursive Abstraction & QCTH-F Dramaturgy]:",
            f"[V6.4 Lyrical Recursive Abstraction, Arrangement Directive ({cfg['section_tag']}) & QCTH-F Dramaturgy]:"
        )
        lines[69] = lines[69].replace("V6.3", "V6.4")

        out = "\n".join(lines)
        if set_idx == 1:
            out = out.replace("Cold Open｜168 BPM｜4/4", "Intro｜58 BPM ➔ Hard Cut｜4/4")
            out = out.replace("Tempo 168", "Tempo 58 BPM (Intro -> Hard Cut)")
            out = out.replace("168 BPM 高速機械底盤", "58 BPM 疏落電鋼琴與低頻合成器迷霧")
            out = out.replace("168 BPM 機械底盤", "58 BPM 稀疏電鋼琴與低頻迷霧")
            out = out.replace("兩小節號角震波環", "58 BPM 輕柔脈搏與電鋼琴泛音環")
            out = out.replace("戰鬥號角與擊弦", "疏落電鋼琴與邊緣玻璃泛音")
            out = out.replace("Slap-Bass 擊弦引起的垂直水霧駐波", "低頻合成器迷霧與邊緣漂移的細碎玻璃泛音駐波")
            out = out.replace("隨 Slap-Bass 擊弦瞬間", "隨電鋼琴泛音與玻璃微光閃爍瞬間")
            out = out.replace("隨 Slap-Bass 擊弦拾音", "隨邊緣漂移的玻璃泛音切分")
            out = out.replace("(168 BPM)", "(58 BPM ➔ Hard Cut 瞬間切換至 62 BPM)")
            out = out.replace("168 BPM 重新切入", "58 BPM 疏落電鋼琴重新切入")
        elif set_idx == 2:
            out = out.replace("Verse 1 (Part A)｜168 BPM｜4/4", "Verse 1 (Part A)｜62 BPM｜4/4")
            out = out.replace("Tempo 168", "Tempo 62 BPM (Thin Groove & Brushed Percussion)")
            out = out.replace("168➔196 BPM", "62➔64 BPM")
        elif set_idx == 3:
            out = out.replace("Verse 1 (Part B)｜168 BPM｜4/4", "Verse 1 (Part B)｜62 BPM｜4/4")
            out = out.replace("Tempo 168", "Tempo 62 BPM (Analog Tape Hiss & Warm Pulse)")
            out = out.replace("168➔196 BPM", "62➔64–138 BPM")
        elif set_idx == 4:
            out = out.replace("Pre-Chorus｜168 → 196 BPM｜4 小節 Accelerando", "Pre-Chorus｜64 → 138 BPM｜Fast Tightening & Climbing Tension")
            out = out.replace("Tempo 168", "Tempo 64➔138 BPM (Accelerando)")
            out = out.replace("168➔196 BPM", "64➔138 BPM")
            out = out.replace("168→196 BPM", "64→138 BPM")
            out = out.replace("168→175 BPM", "64→74 BPM")
            out = out.replace("168 推向 175 BPM", "64 推向 74 BPM")
            out = out.replace("182→189 BPM", "98→110 BPM")
            out = out.replace("182➔189 BPM", "98➔110 BPM")
            out = out.replace("189→192 BPM", "120→128 BPM")
            out = out.replace("195 BPM", "134 BPM")
            out = out.replace("196 BPM", "138 BPM (衝入 140 BPM 副歌)")
        elif set_idx == 5:
            out = out.replace("Chorus 1｜196 BPM｜第一個高速峰值", "Chorus 1｜140 BPM｜Full Lift & Forward-Driving Hook")
            out = out.replace("Tempo 196", "Tempo 140 BPM (Full Lift Chorus)")
            out = out.replace("196➔70 BPM", "140➔65 BPM")
            out = out.replace("196→70 BPM", "140→65 BPM")
            out = out.replace("196 → 70 BPM", "140 → 65 BPM")
            out = out.replace("196 BPM", "140 BPM")
            out = out.replace("70 BPM", "65 BPM")
        elif set_idx == 6:
            out = out.replace("Hard Cut｜196 → 70 BPM，瞬間切換", "Break｜Hard Drop to 65 BPM，剝離至裸脈與單一延音和弦")
            out = out.replace("Tempo 196", "Tempo 65 BPM (Hard Drop Break)")
            out = out.replace("196➔70 BPM", "140➔65 BPM")
            out = out.replace("196→70 BPM", "140→65 BPM")
            out = out.replace("196 → 70 BPM", "140 → 65 BPM")
            out = out.replace("196 BPM", "140 BPM")
            out = out.replace("70 BPM", "65 BPM")
        elif set_idx == 7:
            out = out.replace("Verse 2｜70 BPM｜4/4", "Verse 2｜65 BPM｜Denser Low End & Static")
            out = out.replace("Tempo 70", "Tempo 65 BPM (Denser Low End & Picked-Up Static)")
            out = out.replace("70 BPM", "65 BPM")
        elif set_idx == 8:
            out = out.replace("Bridge (70 BPM 低密度懸置) ＋ Re-ignition (70 → 200 BPM 4–8 小節加速)", "Bridge (Suspended Weightless 懸置失重) ＋ Last Push (65 → 160 BPM 最後推進)")
            out = out.replace("Tempo 70", "Tempo 65 BPM Suspended ➔ 160 BPM Last Push")
            out = out.replace("70➔200 BPM", "65➔160 BPM")
            out = out.replace("70→200 BPM", "65→160 BPM")
            out = out.replace("70 → 200 BPM", "65 → 160 BPM")
            out = out.replace("70➔135 BPM", "65➔130 BPM")
            out = out.replace("100→135 BPM", "105→130 BPM")
            out = out.replace("135→170 BPM", "130→148 BPM")
            out = out.replace("170→190 BPM", "148→156 BPM")
            out = out.replace("190 BPM", "156 BPM")
            out = out.replace("200 BPM", "160 BPM")
            out = out.replace("70 BPM", "65 BPM")
        elif set_idx == 9:
            out = out.replace("Final Chorus｜200 BPM｜4/4", "Chorus 2｜160 BPM｜Bigger, Wider, Overloaded Release Valve")
            out = out.replace("Tempo 200", "Tempo 160 BPM (Overloaded Release Valve Chorus 2)")
            out = out.replace("200 BPM", "160 BPM")
        elif set_idx == 10:
            out = out.replace("Outro / Subtraction｜節奏組抽離・逆序卡農消退・1拍絕對靜默", "Outro｜Decay and Dissolve・節奏拆解・低音拉伸・回聲變薄至 [ \"Silence\" ]")
            out = out.replace("Tempo 200", "Tempo 160 BPM ➔ Decay & Dissolve ➔ Silence")
            out = out.replace("200 BPM", "160 BPM")
            out = out.replace("316 BPM", "Final Glitch Burst (終極故障爆裂)")
        elif set_idx == 11:
            out = out.replace("Extreme Coda｜200 → 316 BPM｜最後 1–2 小節 → Sudden Abrupt Cold Stop", "Post-Outro｜Final Glitch Burst ➔ DU—— ➔ Sustained Synth & Drone ➔ Sudden Abrupt Cold Stop")
            out = out.replace("Tempo 200", "Tempo Final Glitch Burst ➔ Sudden Abrupt Cold Stop")
            out = out.replace("200→316 BPM", "Final Glitch Burst (終極故障爆裂)")
            out = out.replace("200 → 316 BPM", "Final Glitch Burst (終極故障爆裂)")
            out = out.replace("316 BPM", "Final Glitch Burst")
            out = out.replace("168 BPM 重新切入", "58 BPM 疏落電鋼琴重新切入")
        return out

    upgraded_sets = [upgrade_set_text(i, b) for i, b in enumerate(set_blocks, 1)]

    chap0_v64 = chap0.replace(
        "# EFV∞《永不退電的一朵花》V6.3 終極歌詞抽遞・正側術式・起承轉合伏筆與抽象/理性度量衡交融規格書",
        "# EFV∞《永不退電的一朵花》V6.4 終極原詞與編曲標籤全對位・三階抽遞・正側術式・起承轉合伏筆與抽象/理性度量衡交融規格書"
    ).replace(
        "6.3.0 (3-Order Lyrical Recursive Abstraction",
        "6.4.0 (Full Verbatim Lyrics & Arrangement Tag Alignment × 58→62→64–138→140→65→160 BPM Curve × 3-Order Lyrical Recursive Abstraction"
    ).replace(
        "V6.3 四大核心升級重點",
        "V6.4 五大核心升級重點"
    ).replace(
        "Core Equations of V6.3",
        "Core Equations of V6.4"
    )

    highlight_5 = (
        "  5. **全曲 11 段原詞與編曲導引標籤（`[ \"Intro: 58 BPM...\" ]` 等）100% 逐格精確咬合（V6.4 新增）：** "
        "全面對齊最新定稿歌詞與曲速/配器結構——從 **`SET_01 Intro (58 BPM 疏落電鋼琴、低頻合成器迷霧、不落地輕柔脈搏、邊緣玻璃泛音 ➔ Hard Cut)`**、"
        "**`SET_02/03 Verse 1 (62 BPM 纖細律動、刷製打擊樂、克制 Sub-bass、近距對話感氣音人聲與 (huh-hum!) humming)`**、"
        "**`SET_04 Pre-Chorus (64→138 BPM 節奏急速收緊、打擊樂堆疊、合成器前傾、張力攀升)`**、"
        "**`SET_05 Chorus 1 (140 BPM 全面升空、寬廣鼓組、明亮銅管層、吉他猛烈大開)`**、"
        "**`SET_06 Break (Hard drop to 65 BPM 剝離至赤裸脈搏、單一延音和弦與人聲空氣感)`**、"
        "**`SET_07 Verse 2 (65 BPM 更濃密低頻、粗糙靜電邊緣、故障打擊樂敲碎沙漏、已淘汰文件夾微光與導線溫度)`**、"
        "**`SET_08 Bridge (懸置失重、樂句留白與和聲呼吸 ➔ 最後推進 Last Push)`**、"
        "**`SET_09 Chorus 2 (160 BPM 更宏大寬廣過載、高頻全開如洩壓閥爆發)`**、"
        "**`SET_10 Outro (衰減消融、拆解節奏、低音延展、回聲變薄歸零 ➔ Silence)`**，直至 "
        "**`SET_11 Post-Outro (終極故障爆裂 Final glitch burst、四連花(華)—FLOWER、突發親密 DU——、Sustained Synth Note、Electronic Drone ...— ➔ Sudden Abrupt Cold Stop)`**。"
    )
    chap0_v64 = chap0_v64.replace(
        "## 第零章｜歌詞意味三階抽遞法",
        highlight_5 + "\n\n## 第零章｜歌詞意味三階抽遞法"
    )

    chap0_v64 = chap0_v64.replace("196 BPM 副歌心促讚歌脈", "140 BPM 副歌心促讚歌脈")
    chap0_v64 = chap0_v64.replace("70 BPM 故障打擊樂敲碎沙漏", "65 BPM 故障打擊樂敲碎沙漏")
    chap0_v64 = chap0_v64.replace("316 BPM 四音主題極速彈射", "Post-Outro 終極故障爆裂（Final Glitch Burst）極速彈射")
    chap0_v64 = chap0_v64.replace("β_04【196 BPM 空拍穿鏡閃光弧】", "β_04【138➔140 BPM 空拍穿鏡閃光弧】")
    chap0_v64 = chap0_v64.replace("β_05【196➔70 BPM 臨界靜電銀霜】", "β_05【140➔65 BPM Hard Drop 臨界靜電銀霜】")
    chap0_v64 = chap0_v64.replace("掉入 70 BPM 真空深淵", "掉入 65 BPM Break 真空深淵")
    chap0_v64 = chap0_v64.replace("β_08【200 BPM 衝天發光花莖光橋】", "β_08【160 BPM 洩壓閥衝天發光花莖光橋】")
    chap0_v64 = chap0_v64.replace("『200 BPM 舊腳本錯位方格陣（55%）』", "『160 BPM 舊腳本錯位方格陣（55%）』")
    chap0_v64 = chap0_v64.replace("200 BPM 垂直衝天搖臂", "160 BPM 垂直衝天搖臂")
    chap0_v64 = chap0_v64.replace("在 200 BPM 巔峰後", "在 160 BPM 洩壓閥巔峰後")
    chap0_v64 = chap0_v64.replace("β_10【一拍靜默核心的 316 BPM 彈射奇點】", "β_10【Silence 靜默核心的 Final Glitch Burst 故障爆裂奇點】")
    chap0_v64 = chap0_v64.replace("以 316 BPM 極速折線彈射", "以 Final Glitch Burst 終極故障爆裂折線彈射")
    chap0_v64 = chap0_v64.replace("`A=0.70 ➔ A=0.65`｜`168 ➔ 168`", "`A=0.70 ➔ A=0.65`｜`58 (Hard Cut) ➔ 62 BPM`")
    chap0_v64 = chap0_v64.replace("`A=0.60 ➔ A=0.45`｜`168 ➔ 168`", "`A=0.60 ➔ A=0.45`｜`62 ➔ 62 BPM`")
    chap0_v64 = chap0_v64.replace("`A=0.50 ➔ A=0.55`｜`168 ➔ 168`", "`A=0.50 ➔ A=0.55`｜`62 ➔ 64–138 BPM`")
    chap0_v64 = chap0_v64.replace("`A=0.85 ➔ A=0.60`｜`168 ➔ 196`", "`A=0.85 ➔ A=0.60`｜`138 ➔ 140 BPM`")
    chap0_v64 = chap0_v64.replace("`A=0.85 ➔ A=0.65`｜`196 ➔ 196`", "`A=0.85 ➔ A=0.65`｜`140 ➔ 65 BPM (Hard Drop)`")
    chap0_v64 = chap0_v64.replace("`A=0.70 ➔ A=0.60`｜`196 ➔ 70`", "`A=0.70 ➔ A=0.60`｜`65 (Break) ➔ 65 BPM (Verse 2)`")
    chap0_v64 = chap0_v64.replace("`A=0.50 ➔ A=0.55`｜`70 ➔ 70`", "`A=0.50 ➔ A=0.55`｜`65 BPM ➔ Suspended Bridge`")
    chap0_v64 = chap0_v64.replace("`A=0.65 ➔ A=0.65`｜`70 ➔ 200`", "`A=0.65 ➔ A=0.65`｜`Last Push ➔ 160 BPM`")
    chap0_v64 = chap0_v64.replace("`A=0.55 ➔ A=0.70`｜`200 ➔ 200`", "`A=0.55 ➔ A=0.70`｜`160 BPM ➔ Decay & Dissolve`")
    chap0_v64 = chap0_v64.replace("`A=0.98 ➔ A=0.85`｜`200 ➔ 200`", "`A=0.98 ➔ A=0.85`｜`Silence ➔ Final Glitch Burst`")
    chap0_v64 = chap0_v64.replace("`A=0.95 ➔ A=0.65`｜`200 ➔ 168`", "`A=0.95 ➔ A=0.65`｜`Cold Stop (0) ➔ 58 BPM (∞ Loop)`")

    sec5_lines = [
        "### 5. 全曲 11 SET 定稿原詞 × 編曲導引標籤 (`[ ... ]`) × BPM 曲線 × 九宮格逐格抽遞總表（V6.4 Verbatim Lyric Master Map）",
        "",
        "| SET 編號與段落 | 編曲導引標籤 (`Arrangement Directive`) 與曲速 (`BPM`) | 本段完整定稿原詞 (`Verbatim Lyrics`) | 九宮格 9 鏡逐詞/逐句抽遞對位 (`K01..K09`) |",
        "| --- | --- | --- | --- |"
    ]
    for s_i in range(1, 12):
        cfg = SET_V64_CONFIG[s_i]
        set_name = cfg["title_header"].replace("## ", "")
        lyrics_html = "<br>".join([f"`{l}`" for l in cfg["verbatim_lyrics_block"].splitlines()])
        cells_html = "<br>".join([f"**K0{idx+1}**: {lp} _({ac.split('(')[0].strip()})_" for idx, (lp, ac) in enumerate(cfg["cells_lyric_sync"])])
        sec5_lines.append(f"| **{set_name}** | `{cfg['section_tag']}`<br>**{cfg['tempo_short']}** | {lyrics_html} | {cells_html} |")

    chap0_v64 = chap0_v64.rstrip() + "\n\n" + "\n".join(sec5_lines) + "\n\n"

    chap12 = """
## 第十二章｜V6.4 自動化歌詞三階抽遞與 1080P 首尾幀 Prompt 編譯程式（Python Compiler）

為確保未來若需微調任一拍號、歌詞字句、正側角度 $\\Theta_{\\text{FL}}$ 或雙模態參數 $\\lambda_H \\in \\{1,0\\}$ 時，皆能維持 **85% 跨幀基因守恆（55% 主體 + 30% 前鏡正側視差殘影）+ 15% 雙伏筆種子（$\\alpha_S$ 段內伏筆 / $\\beta_S$ 跨段伏筆）** 的嚴密拓撲，本規格書配備完整可執行的 Python 自動化編譯器 `efv_infinity_v6_4_pipeline_generator.py`。

### 1. 編譯器核心資料結構與執行方式

- **輸入配置（`SET_V64_CONFIG`）：** 內建全曲 11 個 SET 的定稿原詞、編曲導引標籤（`[ "Intro: 58 BPM..." ]` 至 `[ "Sudden Abrupt Cold Stop" ]`）、曲速曲線（`58 ➔ Hard Cut ➔ 62 ➔ 64–138 ➔ 140 ➔ 65 ➔ 65 ➔ Suspended Bridge ➔ 160 ➔ Decay/Silence ➔ Glitch Burst/Cold Stop`）及 99 格逐句抽遞微命題。
- **自動合寫引擎（`main()`）：** 讀取 `docs/efv_infinity_v6_3_base.md`，輸出：
  - `docs/efv_infinity_v6_4_chaincontinuity_1080p_full_spec.md`
  - 可透過 `EFV_INPUT_MD` / `EFV_OUTPUT_MD` 覆寫路徑
"""

    full_v64_md = (
        chap0_v64
        + "## 第一章至第十一章｜全 11 SET 歌詞意味三階抽遞 × 正側術式 × 起承轉合伏筆 × 抽象/理性度量衡與完整 Prompt 庫\n\n"
        + "\n\n".join(upgraded_sets)
        + "\n"
        + chap12
    )
    full_v64_md = full_v64_md.replace("以 168 BPM 全速向前疾馳", "在 58 BPM Hard Cut 瞬間切換至 62 BPM 向前推進")
    full_v64_md = full_v64_md.replace("168➔175 BPM", "64➔74 BPM")
    full_v64_md = full_v64_md.replace("175→182 BPM", "74→86 BPM")
    full_v64_md = full_v64_md.replace("192→134 BPM", "128→134 BPM")
    full_v64_md = full_v64_md.replace("196 瞬間硬切至 65 BPM", "140 瞬間驟降（Hard Drop）至 65 BPM")
    full_v64_md = full_v64_md.replace("170➔156 BPM", "148➔156 BPM")
    full_v64_md = full_v64_md.replace("135➔170 BPM", "130➔148 BPM")
    full_v64_md = full_v64_md.replace("170➔190 BPM", "148➔156 BPM")
    full_v64_md = full_v64_md.replace("316 BPM Pinball Ricochet Whip-Pan", "Glitch-Burst Pinball Ricochet Whip-Pan")
    full_v64_md = full_v64_md.replace(
        "316 BPM Ricochet Snap（絕對零度腳架鎖死靜默 ➔ 316 BPM 彈射跨SET交接運鏡）",
        "Glitch-Burst Ricochet Snap（絕對零度腳架鎖死靜默 ➔ 終極故障爆裂彈射跨SET交接運鏡）",
    )

    new_sha = hashlib.sha256(full_v64_md.encode("utf-8")).hexdigest()
    full_v64_md = re.sub(
        r"- \*\*Batch SHA256：\*\* `[0-9a-f]+`",
        f"- **Batch SHA256：** `{new_sha}`",
        full_v64_md,
    )

    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(full_v64_md)

    print(f"✅ Successfully generated V6.4 Spec: {OUTPUT_MD}")
    print(
        f"Total lines: {len(full_v64_md.splitlines())}, "
        f"Total bytes: {len(full_v64_md.encode('utf-8'))}, SHA256: {new_sha}"
    )


if __name__ == "__main__":
    main()
