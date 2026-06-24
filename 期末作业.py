# -*- coding: utf-8 -*-
"""
沉浸式海龟汤悬疑推理室
========================
技术栈：Python + Streamlit 原生组件
运行方式：streamlit run haiguitang.py
"""

import re
import time
import random
from pathlib import Path

import streamlit as st

# ============================================================
# 一、页面基础配置
# ============================================================
st.set_page_config(
    page_title="沉浸式海龟汤悬疑推理室",
    page_icon="🕯️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# 一·五、自定义 CSS（深色霓虹 / 动画 / 发光 / 渐变）
# ============================================================
def inject_css():
    """注入全局 CSS：深色主题、霓虹光晕、动画背景。"""
    st.markdown(
        """
        <style>
        /* ---------- 全局 ---------- */
        html, body, [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(ellipse at 20% 0%, rgba(60,0,120,0.35) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 100%, rgba(0,80,120,0.35) 0%, transparent 60%),
                linear-gradient(180deg, #05060d 0%, #0a0f1e 50%, #050308 100%);
            color: #e6e6f0;
        }
        [data-testid="stHeader"] { background: rgba(0,0,0,0); }

        /* ---------- 侧边栏 ---------- */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(10,10,25,0.95), rgba(5,5,15,0.95));
            border-right: 1px solid rgba(120,80,200,0.3);
            box-shadow: 4px 0 20px rgba(100,50,200,0.15);
        }
        section[data-testid="stSidebar"] * { color: #dcdcff !important; }

        /* ---------- 标题霓虹 ---------- */
        .neon-title {
            font-size: 2.4em;
            font-weight: 900;
            text-align: center;
            background: linear-gradient(90deg, #8a2be2, #00e5ff, #ff4dff, #8a2be2);
            background-size: 300% auto;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: neonFlow 6s linear infinite;
            text-shadow: 0 0 20px rgba(138,43,226,0.4);
            letter-spacing: 2px;
        }
        @keyframes neonFlow {
            0% { background-position: 0% center; }
            100% { background-position: 300% center; }
        }
        .neon-sub {
            text-align: center;
            color: #9adfff;
            text-shadow: 0 0 8px rgba(0,200,255,0.6);
            letter-spacing: 4px;
            font-size: 0.9em;
        }

        /* ---------- 场景图容器 ---------- */
        .scene-frame {
            position: relative;
            border-radius: 16px;
            overflow: hidden;
            box-shadow:
                0 0 30px rgba(0,200,255,0.25),
                0 0 60px rgba(150,50,255,0.15),
                inset 0 0 50px rgba(0,0,0,0.6);
            border: 1px solid rgba(120,200,255,0.3);
            animation: scenePulse 4s ease-in-out infinite;
        }
        @keyframes scenePulse {
            0%, 100% { box-shadow: 0 0 30px rgba(0,200,255,0.25), 0 0 60px rgba(150,50,255,0.15), inset 0 0 50px rgba(0,0,0,0.6); }
            50%      { box-shadow: 0 0 50px rgba(0,200,255,0.45), 0 0 90px rgba(150,50,255,0.30), inset 0 0 50px rgba(0,0,0,0.4); }
        }
        .scene-caption {
            position: absolute;
            bottom: 8px; left: 12px;
            color: #fff;
            font-size: 0.85em;
            text-shadow: 0 0 6px #000, 0 0 12px rgba(0,200,255,0.6);
            letter-spacing: 2px;
        }

        /* ---------- 线索卡片（玻璃拟态 + 悬停发光） ---------- */
        .clue-card {
            position: relative;
            padding: 14px 16px;
            margin-bottom: 12px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(40,20,80,0.55), rgba(10,20,50,0.55));
            border: 1px solid rgba(120,180,255,0.25);
            backdrop-filter: blur(8px);
            color: #e6f0ff;
            box-shadow: 0 4px 18px rgba(0,0,0,0.4), inset 0 0 12px rgba(80,120,255,0.05);
            transition: all 0.35s ease;
            animation: slideIn 0.6s ease both;
        }
        .clue-card::before {
            content: "";
            position: absolute; top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(0,200,255,0.18), transparent);
            transition: left 0.8s;
        }
        .clue-card:hover {
            transform: translateY(-3px) scale(1.02);
            border-color: rgba(0,220,255,0.7);
            box-shadow: 0 6px 30px rgba(0,200,255,0.35);
        }
        .clue-card:hover::before { left: 100%; }
        @keyframes slideIn {
            from { opacity: 0; transform: translateX(20px); }
            to   { opacity: 1; transform: translateX(0); }
        }

        /* ---------- 进度条 ---------- */
        [data-testid="stProgress"] > div > div > div > div {
            background: linear-gradient(90deg, #8a2be2, #00e5ff, #ff4dff) !important;
            box-shadow: 0 0 12px rgba(0,200,255,0.7);
            animation: barGlow 2s ease-in-out infinite alternate;
        }
        @keyframes barGlow {
            from { filter: brightness(1); }
            to   { filter: brightness(1.4); }
        }

        /* ---------- 按钮 ---------- */
        .stButton > button {
            background: linear-gradient(135deg, #2a0a4a, #0a2a4a) !important;
            color: #bdf0ff !important;
            border: 1px solid rgba(0,200,255,0.5) !important;
            border-radius: 10px !important;
            box-shadow: 0 0 12px rgba(0,150,255,0.25) !important;
            transition: all 0.3s !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #4a1a7a, #0a4a7a) !important;
            box-shadow: 0 0 22px rgba(0,200,255,0.7) !important;
            transform: translateY(-1px);
        }

        /* ---------- Toggle ---------- */
        [data-testid="stSidebar"] [data-testid="stToggle"] label span {
            color: #00e5ff !important;
        }

        /* ---------- 聊天气泡 ---------- */
        [data-testid="stChatMessage"] {
            background: rgba(20,20,40,0.6) !important;
            border: 1px solid rgba(120,180,255,0.2);
            border-radius: 12px;
            backdrop-filter: blur(6px);
        }

        /* ---------- 粒子背景（纯 CSS） ---------- */
        .particles {
            position: fixed; top: 0; left: 0;
            width: 100vw; height: 100vh;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        .particles span {
            position: absolute;
            display: block;
            width: 6px; height: 6px;
            background: rgba(0,200,255,0.6);
            border-radius: 50%;
            box-shadow: 0 0 10px rgba(0,200,255,0.8);
            animation: rise 12s linear infinite;
        }
        .particles span:nth-child(2n) {
            background: rgba(180,80,255,0.5);
            box-shadow: 0 0 10px rgba(180,80,255,0.8);
            animation-duration: 16s;
        }
        .particles span:nth-child(3n) {
            background: rgba(255,80,200,0.4);
            box-shadow: 0 0 10px rgba(255,80,200,0.8);
            animation-duration: 20s;
        }
        @keyframes rise {
            0%   { transform: translateY(100vh) translateX(0)   scale(0.5); opacity: 0; }
            10%  { opacity: 1; }
            90%  { opacity: 1; }
            100% { transform: translateY(-10vh) translateX(40px) scale(1.2); opacity: 0; }
        }

        /* ---------- 结局横幅 ---------- */
        .ending-banner {
            text-align: center;
            padding: 24px;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(120,30,180,0.4), rgba(0,180,255,0.4));
            border: 1px solid rgba(180,120,255,0.6);
            box-shadow: 0 0 40px rgba(180,80,255,0.4);
            font-size: 1.3em;
            color: #fff;
            text-shadow: 0 0 12px rgba(0,200,255,0.8);
            animation: bannerIn 1s ease;
        }
        @keyframes bannerIn {
            from { opacity: 0; transform: scale(0.9); }
            to   { opacity: 1; transform: scale(1); }
        }

        /* ---------- 剧本卡片 ---------- */
        .case-tag {
            display: inline-block;
            padding: 2px 8px;
            font-size: 0.75em;
            border-radius: 6px;
            background: linear-gradient(135deg, #8a2be2, #00e5ff);
            color: #fff;
            letter-spacing: 1px;
            box-shadow: 0 0 8px rgba(0,200,255,0.6);
        }

        /* ---------- 文字可读性强化 ---------- */
        html, body, [data-testid="stAppViewContainer"] {
            color: #f3f6ff !important;
            font-size: 16px;
            line-height: 1.7;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown li,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li {
            color: #f3f6ff !important;
            font-weight: 500;
            text-shadow: 0 0 2px rgba(0,0,0,0.5);
        }
        .stMarkdown strong, [data-testid="stMarkdownContainer"] strong,
        [data-testid="stChatMessage"] strong { color: #ffe066 !important; }
        h1, h2, h3, h4 {
            color: #ffffff !important;
            text-shadow: 0 0 8px rgba(0,200,255,0.5);
            letter-spacing: 1px;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #ffffff !important;
            text-shadow: 0 0 6px rgba(180,80,255,0.5);
        }
        label, .stRadio label, [data-testid="stWidgetLabel"] {
            color: #e6ecff !important;
        }
        input, textarea { color: #ffffff !important; }
        [data-testid="stChatInput"] textarea {
            background: rgba(20,15,40,0.7) !important;
            color: #ffffff !important;
            border: 1px solid rgba(0,200,255,0.4) !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color: #aab4d4 !important;
        }
        .stCaption, [data-testid="stCaptionContainer"] {
            color: #c9d4f5 !important;
        }
        .stInfo, [data-testid="stAlert"] {
            background: rgba(0,80,160,0.4) !important;
            color: #ffffff !important;
            border: 1px solid rgba(0,200,255,0.4) !important;
        }

        /* ---------- 新消息渐入动画 ---------- */
        @keyframes msgFadeIn {
            0%   { opacity: 0; transform: translateY(8px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        [data-testid="stChatMessage"] {
            animation: msgFadeIn 0.45s ease-out both;
        }

        /* ---------- 成就横幅 ---------- */
        .achievement {
            position: fixed;
            top: 80px; right: 30px;
            z-index: 9999;
            padding: 14px 22px;
            border-radius: 12px;
            background: linear-gradient(135deg, #ffb700, #ff5e9c, #8a2be2);
            color: #fff;
            font-weight: 800;
            letter-spacing: 1px;
            box-shadow: 0 0 30px rgba(255,150,0,0.7);
            animation: achIn 0.5s ease, achOut 0.6s ease 2.6s forwards;
        }
        @keyframes achIn {
            from { transform: translateX(120%) scale(0.6); opacity: 0; }
            to   { transform: translateX(0) scale(1); opacity: 1; }
        }
        @keyframes achOut {
            to { transform: translateX(120%); opacity: 0; }
        }

        /* ---------- 快捷提问按钮 ---------- */
        .quick-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 8px 0 4px 0;
        }
        .quick-btn {
            padding: 6px 14px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(0,150,200,0.4), rgba(120,50,200,0.4));
            color: #ffffff !important;
            font-size: 0.88em;
            font-weight: 600;
            border: 1px solid rgba(0,220,255,0.45);
            cursor: pointer;
            transition: all 0.25s ease;
            text-shadow: 0 0 4px rgba(0,0,0,0.5);
        }
        .quick-btn:hover {
            background: linear-gradient(135deg, rgba(0,180,255,0.7), rgba(180,80,255,0.7));
            box-shadow: 0 0 14px rgba(0,200,255,0.7);
            transform: translateY(-1px);
        }

        /* ---------- 线索追问区 ---------- */
        .followup-area {
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px dashed rgba(120,180,255,0.25);
        }
        .followup-btn {
            display: inline-block;
            margin: 3px 4px 0 0;
            padding: 4px 10px;
            font-size: 0.78em;
            border-radius: 12px;
            background: rgba(0,200,255,0.15);
            color: #9adfff !important;
            border: 1px solid rgba(0,200,255,0.3);
            cursor: pointer;
            transition: all 0.2s;
        }
        .followup-btn:hover {
            background: rgba(0,200,255,0.35);
            color: #ffffff !important;
        }

        /* ---------- 隐藏装饰元素 ---------- */
        #MainMenu, footer { visibility: hidden; }

        /* ============================================== */
        /*         动态天气层（雨 / 雪 / 灯光闪烁）         */
        /* ============================================== */
        .weather-layer {
            position: fixed;
            top: 0; left: 0;
            width: 100vw;
            height: 100vh;
            pointer-events: none;
            z-index: 9999;
            overflow: hidden;
        }

        /* 雨（用 box-shadow 大量克隆随机位置雨丝） */
        .weather-rain {
            background: linear-gradient(180deg,
                rgba(10, 20, 40, 0.18) 0%,
                rgba(20, 30, 60, 0.30) 100%);
        }
        .weather-rain::before {
            content: '';
            position: absolute;
            top: -100px;
            left: 0;
            width: 1px;
            height: 22px;
            background: linear-gradient(to bottom,
                rgba(180, 220, 255, 0.0) 0%,
                rgba(180, 220, 255, 0.6) 50%,
                rgba(180, 220, 255, 0.9) 100%);
            box-shadow: var(--rain-shadows, none);
            animation: rainFall 0.7s linear infinite;
        }
        .weather-rain::after {
            content: '';
            position: absolute;
            top: -100px;
            left: 0;
            width: 1px;
            height: 16px;
            background: linear-gradient(to bottom,
                rgba(200, 230, 255, 0.0) 0%,
                rgba(200, 230, 255, 0.5) 50%,
                rgba(200, 230, 255, 0.8) 100%);
            box-shadow: var(--rain-shadows-2, none);
            animation: rainFall 0.5s linear infinite;
        }
        @keyframes rainFall {
            from { transform: translate3d(0, 0, 0); }
            to   { transform: translate3d(-15px, 1100px, 0); }
        }

        /* 雪 */
        .weather-snow::before,
        .weather-snow::after {
            content: '';
            position: absolute;
            top: -10%;
            left: 0;
            width: 100%;
            height: 110%;
            background:
                radial-gradient(circle, #ffffff 1.2px, transparent 1.5px) 0 0 / 30px 30px,
                radial-gradient(circle, #d0e8ff 0.8px, transparent 1px) 10px 10px / 50px 50px;
            animation: snowFall 8s linear infinite;
            opacity: 0.85;
        }
        .weather-snow::after {
            animation: snowFall 13s linear infinite;
            animation-delay: -3s;
            opacity: 0.5;
        }
        @keyframes snowFall {
            from { transform: translateY(-50px) translateX(0); }
            to   { transform: translateY(100vh) translateX(30px); }
        }

        /* 灯光闪烁 */
        .weather-flicker::before {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            background:
                radial-gradient(ellipse at 30% 20%, rgba(255,200,100,0.35) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 70%, rgba(180,200,255,0.20) 0%, transparent 60%);
            animation: flicker 3s ease-in-out infinite;
        }
        .weather-flicker::after {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            animation: dimFlicker 3s ease-in-out infinite;
        }
        @keyframes flicker {
            0%, 100% { opacity: 0.9; }
            10% { opacity: 0.3; }
            18% { opacity: 0.95; }
            25% { opacity: 0.5; }
            40% { opacity: 1.0; }
            55% { opacity: 0.4; }
            70% { opacity: 0.85; }
            85% { opacity: 0.6; }
        }
        @keyframes dimFlicker {
            0%, 100% { opacity: 0.0; }
            10% { opacity: 0.4; }
            18% { opacity: 0.0; }
            25% { opacity: 0.3; }
            40% { opacity: 0.0; }
            55% { opacity: 0.35; }
            70% { opacity: 0.05; }
            85% { opacity: 0.2; }
        }

        /* 天气指示徽章 */
        .weather-tag {
            display: inline-block;
            margin: 6px 0 10px 0;
            padding: 4px 14px;
            background: rgba(0, 0, 0, 0.55);
            color: #ffe066;
            border: 1px solid rgba(255,224,102,0.5);
            border-radius: 14px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 1px;
            box-shadow: 0 0 12px rgba(255,224,102,0.3);
        }

        /* 证据板 */
        .evidence-board {
            margin: 8px 0 16px 0;
            padding: 12px 14px;
            background: linear-gradient(135deg, rgba(20,15,40,0.85), rgba(40,20,60,0.85));
            border: 1px solid rgba(180,140,255,0.45);
            border-radius: 12px;
            box-shadow: 0 0 18px rgba(140,100,255,0.25);
        }
        .evidence-board .eb-title {
            color: #e8d8ff;
            font-size: 14px;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 8px;
            text-align: center;
            text-shadow: 0 0 8px rgba(180,140,255,0.7);
        }
        .evidence-board .eb-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 6px;
            margin-top: 6px;
        }
        .evidence-board .eb-node {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 8px 4px;
            background: rgba(255,255,255,0.04);
            border: 1px solid rgba(180,140,255,0.25);
            border-radius: 8px;
            font-size: 12px;
            color: #b9a5d8;
            text-align: center;
            transition: all 0.4s;
        }
        .evidence-board .eb-node.unlocked {
            background: linear-gradient(135deg, rgba(100,200,255,0.18), rgba(180,140,255,0.18));
            border-color: rgba(140,220,255,0.7);
            color: #ffffff;
            box-shadow: 0 0 10px rgba(140,220,255,0.5);
            transform: scale(1.04);
        }
        .evidence-board .eb-node .eb-icon {
            font-size: 22px;
            margin-bottom: 2px;
        }
        .evidence-board .eb-node.locked .eb-icon {
            filter: grayscale(1) brightness(0.5);
        }
        .evidence-board .eb-tip {
            text-align: center;
            color: #8a7aa8;
            font-size: 11px;
            margin-top: 6px;
        }
        </style>

        <!-- 粒子层（50 个漂浮光点） -->
        <div class="particles">
        """ + "".join(
            f'<span style="left:{i*2}%;animation-delay:{(i%10)*0.6}s;width:{4+(i%5)}px;height:{4+(i%5)}px;"></span>'
            for i in range(50)
        ) + """
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 注入动态雨丝 box-shadow（240 条随机位置的雨滴）
    shadows_1 = gen_rain_shadows(count=140, seed=42)
    shadows_2 = gen_rain_shadows(count=100, seed=137)
    st.markdown(
        f"""
        <style>
        :root {{
            --rain-shadows: {shadows_1};
            --rain-shadows-2: {shadows_2};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# 二、谜题剧本库（多个案件 / 用户可自由选择）
# ============================================================
# 公共元素：明确"是/不是/无关"的引导关键词
YES_KEYWORDS = [
    "是", "是的", "对的", "正确", "有", "是有关", "是有关联",
    "吗", "是不是", "是否",
]
NO_KEYWORDS = ["不是", "没有", "不对", "否", "没", "并非"]
IRRELEVANT_HINTS = [
    "今天", "天气", "你好", "你是谁", "名字", "你好吗", "在吗", "hello", "hi",
    "股票", "基金", "工资", "房价", "游戏", "电影", "吃饭",
]
BANNED_KEYWORDS = ["脏话", "骂人", "政治", "宗教", "色情"]

# ----------------------------------------------------------
# 案件 ① 海角灯塔的最后一夜
# ----------------------------------------------------------
CASE_LIGHTHOUSE = {
    "id": "lighthouse",
    "icon": "🕯️",
    "title": "海角灯塔的最后一夜",
    "tag": "悬疑 / 失忆",
    "weather": "rain",            # 动态天气：rain / snow / flicker
    "weather_label": "🌧 暴雨",
    "bg": "一座孤零零的灯塔矗立在海角悬崖之上，今夜风暴席卷，灯塔看守人离奇失踪……",
    "intro": "🌊 欢迎来到「海角灯塔的最后一夜」。\n\n今夜海雾弥漫，灯塔看守人艾文离奇失踪。\n请通过提问还原真相，你的回答将限于 **是 / 不是 / 无关** 的引导式提示。\n\n👉 在下方输入你的第一个问题开始调查。",
    "scene_start": "scene_start.jpg",
    "scene_end": "scene_end.jpg",
    "truth": (
        "看守人艾文在风暴夜中曾目睹走私船搁浅，他记下船号准备报警。"
        "走私头目伪装成访客登塔，逼迫艾文交出笔记本。"
        "搏斗中艾文头部受击坠海，被冲到下游浅滩，被人救起后失去记忆。"
        "他醒来时以为自己只是普通的灯塔守夜人，于是回到塔中继续守夜——"
        "但此时的他其实已经是被通缉的关键证人。"
    ),
    "endings": {
        "good": "你成功还原了风暴夜的真相，艾文的记忆逐渐恢复……【结局：真相大白】",
        "bad": "你错过了关键线索，案件将永远封存在大海的迷雾中……【结局：未解之谜】",
    },
    "truth_keywords": [
        "真相", "结局", "发生了什么", "发生了什么事", "事故",
        "艾文", "走私", "昏迷", "记忆", "失忆", "证人", "坠海",
    ],
    "truth_min_clues": 4,    # 至少解锁 4 条线索才能触发真相
    "clues": {
        "clue_storm": {
            "text": "🌩 线索①：风暴当夜的值班记录显示，灯塔灯光在凌晨2点曾短暂熄灭。",
            "keywords": ["风暴", "天气", "暴风雨", "风暴夜", "狂风", "下雨", "雨"],
            "image": "clue_storm.jpg",
        },
        "clue_lighthouse": {
            "text": "🗼 线索②：灯塔顶层的瞭望窗玻璃内侧有擦拭过的血指印。",
            "keywords": ["灯塔", "瞭望", "塔顶", "窗户", "玻璃", "顶层"],
            "image": "clue_lighthouse.jpg",
        },
        "clue_paper": {
            "text": "📜 线索③：艾文枕头下藏着半张被撕掉的纸条，上面写着船号 'N-307'。",
            "keywords": ["纸条", "纸", "笔迹", "船号", "字条", "字母", "数字", "307"],
            "image": "clue_paper.jpg",
        },
        "clue_cup": {
            "text": "☕ 线索④：厨房水槽里有一只沾有口红印的咖啡杯，但灯塔里只有艾文一个男人。",
            "keywords": ["咖啡", "杯子", "口红", "厨房", "水槽", "杯"],
            "image": "clue_cup.jpg",
        },
        "clue_log": {
            "text": "📖 线索⑤：值班日志的最近三天记录被撕掉了整整三页。",
            "keywords": ["日志", "记录", "值班", "三页", "撕掉", "本子"],
            "image": "clue_log.jpg",
        },
        "clue_glove": {
            "text": "🧤 线索⑥：灯塔外的小径上发现一只遗落的皮手套，里面缝着金线。",
            "keywords": ["手套", "皮手套", "金线", "小径", "路上"],
            "image": "clue_glove.jpg",
        },
        "clue_shoes": {
            "text": "👞 线索⑦：悬崖边的泥地有一双男鞋印，但只有去的方向，没有回来的。",
            "keywords": ["鞋印", "脚印", "悬崖", "泥地", "鞋"],
            "image": "clue_shoes.jpg",
        },
        "clue_weapon": {
            "text": "🩸 线索⑧：瞭望台栏杆上挂着一根带血的铜质望远镜背带。",
            "keywords": ["望远镜", "背带", "铜", "血", "瞭望台", "栏杆"],
            "image": "clue_weapon.jpg",
        },
    },
    "evidence_board": {
        "title": "🕯 海角灯塔 证据板",
        "nodes": [
            {"id": "aiwen",    "label": "艾文",     "icon": "👤"},
            {"id": "smuggler", "label": "走私头目", "icon": "🥷"},
            {"id": "ship",     "label": "N-307",   "icon": "🚢"},
            {"id": "tower",    "label": "灯塔",     "icon": "🗼"},
            {"id": "storm",    "label": "风暴夜",   "icon": "🌊"},
            {"id": "memory",   "label": "失忆",     "icon": "💭"},
        ],
        "unlock_map": {
            "aiwen":    ["clue_paper", "clue_cup", "clue_glove"],
            "smuggler": ["clue_glove", "clue_shoes"],
            "ship":     ["clue_paper", "clue_log"],
            "tower":    ["clue_lighthouse", "clue_weapon"],
            "storm":    ["clue_storm"],
            "memory":   ["clue_log", "clue_cup"],
        },
    },
}

# ----------------------------------------------------------
# 案件 ② 雪山木屋的三个人
# ----------------------------------------------------------
CASE_CABIN = {
    "id": "cabin",
    "icon": "🏔️",
    "title": "雪山木屋的三个人",
    "tag": "暴风雪 / 密室",
    "weather": "snow",
    "weather_label": "❄ 暴风雪",
    "bg": "暴风雪封山的第三个夜晚，三人小木屋里传来一声枪响，明早却少了一人……",
    "intro": "❄️ 欢迎来到「雪山木屋的三个人」。\n\n三名登山者被困木屋两个夜晚，第三天清晨你醒来发现少了一人。\n请通过提问还原真相。\n\n👉 在下方输入你的第一个问题开始调查。",
    "scene_start": "cabin_start.jpg",
    "scene_end": "cabin_end.jpg",
    "truth": (
        "三人为大学登山社社员：阿林、小柯、老周。"
        "老周欠下高利贷，雇了山下同伙假扮救援队想带阿林逃走，被小柯发现。"
        "争执中老周误杀小柯（以为对方是要挟的人），同伙连夜把尸体从烟囱运走。"
        "阿林第二天醒来以为小柯只是提前下山，便独自离开——"
        "他带走了凶器，却不知道自己的背包里藏着被血迹浸染的登山扣。"
    ),
    "endings": {
        "good": "你还原了暴风雪夜的枪声，三人命运终于真相大白……【结局：真相大白】",
        "bad": "暴风雪将一切掩埋，三人命运无人知晓……【结局：雪中悬案】",
    },
    "truth_keywords": [
        "真相", "结局", "发生了什么", "事故",
        "阿林", "小柯", "老周", "高利贷", "同伙", "误杀", "枪",
    ],
    "truth_min_clues": 4,
    "clues": {
        "clue_window": {
            "text": "🪟 线索①：木屋唯一的窗户玻璃从外侧被敲破，雪地上却没有脚印。",
            "keywords": ["窗", "玻璃", "破", "窗户"],
            "image": "cabin_window.jpg",
        },
        "clue_chimney": {
            "text": "🧱 线索②：烟囱内壁有明显的拖拽痕迹，灰烬里混着几根深色纤维。",
            "keywords": ["烟囱", "烟筒", "壁炉", "灰烬", "纤维", "拖拽"],
            "image": "cabin_chimney.jpg",
        },
        "clue_bullet": {
            "text": "🔫 线索③：地板上有一颗未击发的子弹，弹壳却在门口的雪里。",
            "keywords": ["子弹", "弹壳", "枪", "枪声", "射击", "未击发"],
            "image": "cabin_bullet.jpg",
        },
        "clue_snowprint": {
            "text": "👣 线索④：屋外雪地有两条来路、四条去路的鞋印，但木屋里原本只有三人。",
            "keywords": ["雪地", "鞋印", "脚印", "屋外", "雪"],
            "image": "cabin_snowprint.jpg",
        },
        "clue_diary": {
            "text": "📓 线索⑤：老周笔记本写着「22:30 收网，B 段完成」。",
            "keywords": ["笔记本", "日记", "本子", "收网", "B段"],
            "image": "cabin_diary.jpg",
        },
        "clue_phone": {
            "text": "📱 线索⑥：小柯手机信号记录显示，他在凌晨 1:12 收到一条求救短信。",
            "keywords": ["手机", "短信", "信号", "求救", "电话"],
            "image": "cabin_phone.jpg",
        },
        "clue_kit": {
            "text": "🎒 线索⑦：阿林背包里一个金属登山扣被深色液体染成红棕色。",
            "keywords": ["背包", "登山扣", "扣", "金属", "红棕"],
            "image": "cabin_kit.jpg",
        },
        "clue_card": {
            "text": "💳 线索⑧：木屋角落发现一张陌生名片，印着「救援·张师傅」。",
            "keywords": ["名片", "救援", "张师傅", "张"],
            "image": "cabin_card.jpg",
        },
    },
    "evidence_board": {
        "title": "🏔 雪山木屋 证据板",
        "nodes": [
            {"id": "alin",   "label": "阿林",     "icon": "🧗"},
            {"id": "xiaoke", "label": "小柯",     "icon": "🧗"},
            {"id": "laozhou","label": "老周",     "icon": "🧓"},
            {"id": "gun",    "label": "手枪",     "icon": "🔫"},
            {"id": "chimney","label": "烟囱",     "icon": "🧱"},
            {"id": "debt",   "label": "高利贷",   "icon": "💰"},
            {"id": "carabiner","label": "登山扣", "icon": "🪝"},
        ],
        "unlock_map": {
            "alin":      ["clue_kit", "clue_phone", "clue_diary"],
            "xiaoke":    ["clue_window", "clue_diary", "clue_phone"],
            "laozhou":   ["clue_phone", "clue_card"],
            "gun":       ["clue_bullet", "clue_chimney"],
            "chimney":   ["clue_chimney", "clue_diary"],
            "debt":      ["clue_phone", "clue_card"],
            "carabiner": ["clue_kit"],
        },
    },
}

# ----------------------------------------------------------
# 案件 ③ 末班地铁的消失者
# ----------------------------------------------------------
CASE_METRO = {
    "id": "metro",
    "icon": "🚇",
    "title": "末班地铁的消失者",
    "tag": "都市怪谈 / 监控",
    "weather": "flicker",
    "weather_label": "💡 灯光闪烁",
    "bg": "末班地铁关闭后，站台上只剩一名穿米色风衣的女人……下一站她消失了。",
    "intro": "🌃 欢迎来到「末班地铁的消失者」。\n\n深夜 23:55，最后一班地铁到站。一名穿米色风衣的女人上了车，"
            "三站之后车厢监控显示——她已不在车上。\n请通过提问还原真相。\n\n👉 在下方输入你的第一个问题开始调查。",
    "scene_start": "metro_start.jpg",
    "scene_end": "metro_end.jpg",
    "truth": (
        "女人其实根本没上车。她是十年前因地铁事故去世的值班员。"
        "当晚她值守的老站台因施工被短暂启用了一晚（断电测试），"
        "她的「出现」只是调度员老陈在监控里看到旧同事穿同款风衣路过工地时的错觉。"
        "——老陈记错了时间表，其实那晚末班车并未停靠事故站台。"
        "所谓「消失」只是没人下车的正常一站。"
    ),
    "endings": {
        "good": "你解开了都市怪谈背后的真实原因……【结局：真相大白】",
        "bad": "她仍徘徊在末班车的迷雾里……【结局：都市怪谈】",
    },
    "truth_keywords": [
        "真相", "结局", "发生了什么", "事故",
        "值班员", "调度", "老陈", "陈", "去世", "死了", "旧同事",
        "风衣", "错觉", "施工",
    ],
    "truth_min_clues": 4,
    "clues": {
        "clue_camera": {
            "text": "📹 线索①：站台监控在 23:59 出现 47 秒黑屏，无任何故障记录。",
            "keywords": ["监控", "黑屏", "摄像头", "47秒", "故障"],
            "image": "metro_camera.jpg",
        },
        "clue_ticket": {
            "text": "🎫 线索②：闸机记录显示她并未刷卡进站。",
            "keywords": ["闸机", "刷卡", "票", "车票", "进站", "记录"],
            "image": "metro_ticket.jpg",
        },
        "clue_schedule": {
            "text": "🕐 线索③：调度日志标注当晚 1 号站台「临时启用·断电测试」。",
            "keywords": ["调度", "日志", "1号站台", "站台", "断电", "测试"],
            "image": "metro_schedule.jpg",
        },
        "clue_photo": {
            "text": "🖼 线索④：站务室挂着十年前「优秀员工」合影，其中一人穿同款米色风衣。",
            "keywords": ["合影", "合照", "照片", "优秀员工", "十年前", "米色"],
            "image": "metro_photo.jpg",
        },
        "clue_news": {
            "text": "📰 线索⑤：旧报纸报道十年前「末班车追尾事故」造成 1 人死亡。",
            "keywords": ["报纸", "旧报", "新闻", "追尾", "事故", "十年前"],
            "image": "metro_news.jpg",
        },
        "clue_uniform": {
            "text": "👔 线索⑥：调度员老陈当晚穿的也是米色风衣。",
            "keywords": ["老陈", "陈", "风衣", "米色", "调度员", "穿"],
            "image": "metro_uniform.jpg",
        },
        "clue_footstep": {
            "text": "👞 线索⑦：站台尽头发现泥泞的 42 码鞋印。",
            "keywords": ["鞋印", "脚印", "42码", "泥泞", "站台"],
            "image": "metro_footstep.jpg",
        },
        "clue_voice": {
            "text": "🔊 线索⑧：站台广播里出现过一句「请勿越线」，但当晚并未触发该提示。",
            "keywords": ["广播", "越线", "提示", "请勿"],
            "image": "metro_voice.jpg",
        },
    },
    "evidence_board": {
        "title": "🚇 末班地铁 证据板",
        "nodes": [
            {"id": "woman",   "label": "风衣女子", "icon": "👩"},
            {"id": "driver",  "label": "司机老陈", "icon": "👨‍✈️"},
            {"id": "dispat",  "label": "调度员",   "icon": "🎛️"},
            {"id": "platform","label": "施工站台", "icon": "🚧"},
            {"id": "monitor", "label": "监控黑屏", "icon": "📹"},
            {"id": "coat",    "label": "米色风衣", "icon": "🧥"},
        ],
        "unlock_map": {
            "woman":   ["metro_ticket", "metro_photo"],
            "driver":  ["metro_news", "metro_uniform"],
            "dispat":  ["metro_schedule", "metro_voice"],
            "platform":["metro_footstep", "metro_schedule"],
            "monitor": ["metro_camera"],
            "coat":    ["metro_photo", "metro_uniform"],
        },
    },
}

# ----------------------------------------------------------
# 剧本总库
# ----------------------------------------------------------
CASES = {
    CASE_LIGHTHOUSE["id"]: CASE_LIGHTHOUSE,
    CASE_CABIN["id"]: CASE_CABIN,
    CASE_METRO["id"]: CASE_METRO,
}
CASE_LIST = list(CASES.values())
DEFAULT_CASE_ID = CASE_LIGHTHOUSE["id"]

# ============================================================
# 三、工具函数
# ============================================================
# 资源搜索目录（按优先级），空字符串表示脚本同目录
ASSET_SEARCH_DIRS = ["", "jpg", "images", "assets"]

def get_asset_path(filename: str) -> str:
    """
    获取素材路径。依次在以下位置查找，找到即返回：
      1. 脚本同目录
      2. jpg/  子目录
      3. images/  子目录
      4. assets/  子目录

    若所有位置都不存在，返回脚本同目录路径（让 st.image 正常报错占位）。
    """
    base_dir = Path(__file__).parent
    for sub in ASSET_SEARCH_DIRS:
        path = base_dir / sub / filename if sub else base_dir / filename
        if path.exists():
            return str(path)
    return str(base_dir / filename)

def has_asset(filename: str) -> bool:
    """判断素材文件是否存在（兼容子目录）。"""
    base_dir = Path(__file__).parent
    for sub in ASSET_SEARCH_DIRS:
        path = base_dir / sub / filename if sub else base_dir / filename
        if path.exists():
            return True
    return False

def get_current_case() -> dict:
    """根据 session_state 返回当前案件数据。"""
    cid = st.session_state.get("current_case", DEFAULT_CASE_ID)
    return CASES.get(cid, CASES[DEFAULT_CASE_ID])

def gen_rain_shadows(count: int = 120, seed: int = 42) -> str:
    """
    生成 N 条随机位置的"雨丝" box-shadow 字符串。
    每条雨丝是一个 1px×20px 的发光体，但通过 box-shadow
    复制出 count 个不同位置的"克隆"，形成自然下雨的视觉。
    """
    rng = random.Random(seed)
    shadows = []
    for _ in range(count):
        x = rng.randint(-100, 2100)        # 横向随机（覆盖整个视口 + 边缘缓冲）
        y = rng.randint(-200, 1200)        # 纵向随机
        alpha = round(rng.uniform(0.25, 0.75), 2)  # 透明度随机
        # 偏移 (x, y) 模糊 0 扩散 0 颜色
        shadows.append(f"{x}px {y}px 0 0 rgba(180,220,255,{alpha})")
    return ",\n            ".join(shadows)

def init_session_state():
    """初始化会话状态。"""
    defaults = {
        "current_case": DEFAULT_CASE_ID,
        "unlocked_clues": [],
        "asked_questions": [],
        "current_scene": CASES[DEFAULT_CASE_ID]["scene_start"],
        "progress": 0.0,
        "ended": False,
        "ending_type": None,
        "messages": [],
        "unlocked_count": 0,
        "_typed_count": 0,        # 打字机已播放过的消息数
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_for_new_case(case_id: str):
    """切换剧本时重置相关状态。"""
    st.session_state["current_case"] = case_id
    case = CASES[case_id]
    st.session_state["unlocked_clues"] = []
    st.session_state["unlocked_count"] = 0
    st.session_state["asked_questions"] = []
    st.session_state["current_scene"] = case["scene_start"]
    st.session_state["progress"] = 0.0
    st.session_state["ended"] = False
    st.session_state["ending_type"] = None
    st.session_state["messages"] = [
        {"role": "assistant", "content": case["intro"]}
    ]
    st.session_state["_typed_count"] = 0   # 重置打字机进度

def normalize(text: str) -> str:
    """文本归一化：去空格、转小写。"""
    return re.sub(r"\s+", "", text or "").lower()

def match_keywords(text: str, keywords: list) -> bool:
    """判断文本中是否包含任一关键词。"""
    nt = normalize(text)
    return any(normalize(kw) in nt for kw in keywords)

def judge_question(question: str) -> str:
    """
    核心判断逻辑（修复版：线索优先 + 真相关键词分级 + 门槛控制）。

    返回：
    - "banned"            触发禁用词
    - "clue:<id>"         命中关键线索
    - "truth"             触发真相（需满足解锁门槛）
    - "truth_gated"       含真相词但未达门槛，提示继续探索
    - "ask_more"          让玩家继续提问
    - "irrelevant"        完全无关
    """
    case = get_current_case()
    q = question.strip()

    if match_keywords(q, BANNED_KEYWORDS):
        return "banned"

    # —— 1. 线索优先：先尝试匹配线索 ——
    for cid, info in case["clues"].items():
        if cid in st.session_state["unlocked_clues"]:
            continue
        if match_keywords(q, info["keywords"]):
            return f"clue:{cid}"

    # —— 2. 真相关键词分级触发 ——
    truth_kw = case.get("truth_keywords", [])

    # 强真相词：只要命中就直接揭示真相
    strong = {"真相", "结局", "真凶", "凶手是谁", "到底怎么回事", "到底发生了什么"}
    if match_keywords(q, list(strong)):
        return _truth_with_gate(case)

    # 弱真相词：必须达到解锁门槛才揭示
    weak = [kw for kw in truth_kw if kw not in strong]
    if weak and match_keywords(q, weak):
        return _truth_with_gate(case)

    # —— 3. 肯定/否定词 → 引导继续 ——
    if match_keywords(q, YES_KEYWORDS):
        return "ask_more"
    if match_keywords(q, NO_KEYWORDS):
        return "ask_more"

    # —— 4. 无关问题 ——
    if match_keywords(q, IRRELEVANT_HINTS):
        return "irrelevant"

    return "irrelevant"

def _truth_with_gate(case: dict) -> str:
    """
    真相触发门槛：已解锁线索数 ≥ min_clues 才返回 "truth"，
    否则返回 "truth_gated"（提示继续探索）。
    """
    min_clues = case.get("truth_min_clues", 4)
    have = st.session_state.get("unlocked_count", 0)
    if have >= min_clues:
        return "truth"
    return "truth_gated"

def unlock_clue(clue_id: str):
    """解锁线索，更新进度与场景图。"""
    case = get_current_case()
    info = case["clues"][clue_id]
    st.session_state["unlocked_clues"].append(clue_id)
    st.session_state["unlocked_count"] = len(st.session_state["unlocked_clues"])
    st.session_state["current_scene"] = info["image"]
    st.session_state["progress"] = min(
        1.0, st.session_state["unlocked_count"] / len(case["clues"])
    )

def answer_for(judge: str) -> str:
    """根据判断结果返回给玩家的回答。"""
    case = get_current_case()
    min_clues = case.get("truth_min_clues", 4)
    have = st.session_state.get("unlocked_count", 0)
    need = max(0, min_clues - have)

    if judge == "banned":
        return "🚫 请专注于案件本身，提出与故事相关的问题。"
    if judge == "truth_gated":
        return (
            f"🔒 真相似乎就在眼前，但你还需要再收集 **{need}** 条关键线索……\n\n"
            f"💡 试着从「时间 / 地点 / 人物 / 物品」等方向继续提问。"
        )
    if judge == "truth":
        return (
            "🔍 真相浮现：\n\n"
            + case["truth"]
            + "\n\n"
            + case["endings"]["good"]
        )
    if judge == "irrelevant":
        return (
            f"🌀 这个问题与「{case['title']}」无关，请围绕"
            f"{case['tag']}方向的关键信息提问。"
        )
    if judge == "ask_more":
        return "🤔 还不能直接告诉你，请尝试更具体地描述你想确认的细节。"
    if judge.startswith("clue:"):
        cid = judge.split(":", 1)[1]
        return case["clues"][cid]["text"] + "\n\n（线索已解锁，场景已更新）"
    return "……"

def push_message(role: str, content: str):
    """向聊天记录追加消息。"""
    st.session_state["messages"].append({"role": role, "content": content})

def render_weather_layer():
    """
    在页面最顶层注入动态天气层。
    通过 case["weather"] 字段选择 rain / snow / flicker。
    """
    case = get_current_case()
    weather = case.get("weather")
    if not weather:
        return
    label = case.get("weather_label", "")
    # 天气指示徽章（在场景图下方）
    st.markdown(
        f'<span class="weather-tag">{label}</span>',
        unsafe_allow_html=True,
    )
    # 动态天气层（pointer-events: none 不影响操作）
    st.markdown(
        f'<div class="weather-layer weather-{weather}"></div>',
        unsafe_allow_html=True,
    )

def render_evidence_board():
    """
    渲染证据板：根据已解锁线索高亮对应节点。
    若剧本未配置 evidence_board 则跳过。
    """
    case = get_current_case()
    board = case.get("evidence_board")
    if not board:
        return

    nodes = board.get("nodes", [])
    unlock_map = board.get("unlock_map", {})
    unlocked = set(st.session_state.get("unlocked_clues", []))

    # 统计已解锁节点
    unlocked_node_ids = {
        nid for nid, deps in unlock_map.items()
        if any(dep in unlocked for dep in deps)
    }

    # 构建 HTML
    node_html = []
    for n in nodes:
        nid = n["id"]
        is_unlocked = nid in unlocked_node_ids
        cls = "eb-node unlocked" if is_unlocked else "eb-node locked"
        node_html.append(
            f'<div class="{cls}">'
            f'<div class="eb-icon">{n["icon"]}</div>'
            f'<div>{n["label"]}</div>'
            f'</div>'
        )

    total = len(nodes)
    unlocked_n = len(unlocked_node_ids)
    tip = (
        f"已点亮 <b>{unlocked_n}</b> / {total} 个节点"
        if unlocked_n > 0
        else "🔒 节点尚未解锁 —— 继续探索以点亮它们"
    )

    st.markdown(
        f"""
        <div class="evidence-board">
            <div class="eb-title">{board['title']}</div>
            <div class="eb-grid">
                {"".join(node_html)}
            </div>
            <div class="eb-tip">{tip}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def typewriter(placeholder, text: str, speed: float = 0.012):
    """
    打字机效果：在 placeholder 中逐字渲染 text。
    - 中文 / 标点 / 换行均按"字符"处理。
    - speed 越小越快，建议 0.008 ~ 0.025。
    """
    buf = ""
    # 把 \n 转成 <br/> 兼容 markdown 渲染
    safe_text = text.replace("\n", "<br/>")
    for ch in safe_text:
        buf += ch
        placeholder.markdown(buf + "▌", unsafe_allow_html=True)
        # 标点稍作停顿，模拟真人节奏
        if ch in "，。！？、；：…":
            time.sleep(speed * 3)
        else:
            time.sleep(speed)
    # 最终去掉光标
    placeholder.markdown(text)

def show_achievement(title: str, icon: str = "🏆"):
    """显示成就横幅（HTML 注入）。"""
    st.markdown(
        f"""
        <div class="achievement">{icon} 成就解锁：{title}</div>
        <script>
        setTimeout(() => {{
            const el = document.querySelector('.achievement');
            if (el) el.remove();
        }}, 3300);
        </script>
        """,
        unsafe_allow_html=True,
    )

def process_user_question(question: str):
    """处理一次用户提问：判重 / 判断 / 副作用 / 推送消息。"""
    question = (question or "").strip()
    if not question:
        return

    if question in st.session_state["asked_questions"]:
        push_message("user", question)
        push_message(
            "assistant",
            "🔁 你已经提过这个问题了，请尝试换一个角度。",
        )
        return

    st.session_state["asked_questions"].append(question)
    push_message("user", question)

    judge = judge_question(question)
    reply = answer_for(judge)

    # —— 分支：未达门槛的真相提问 → 不解锁、不结束，仅提示继续探索 ——
    if judge == "truth_gated":
        push_message("assistant", reply)
        return

    # 副作用：解锁线索
    if judge.startswith("clue:"):
        cid = judge.split(":", 1)[1]
        unlock_clue(cid)
        sfx = get_asset_path("unlock.mp3")
        if Path(sfx).exists():
            st.audio(sfx, format="audio/mp3", autoplay=True)
        # 成就提示
        case = get_current_case()
        info = case["clues"][cid]
        # 抽取线索简短名（去掉 emoji 和"线索X："前缀）
        short = re.sub(r"^[^\u4e00-\u9fa5]*线索[①②③④⑤⑥⑦⑧⑨]?[：:]?\s*", "", info["text"])
        show_achievement(f"新线索：{short[:18]}…", "🔍")

    # 真相结局
    if judge == "truth":
        case = get_current_case()
        st.session_state["ended"] = True
        st.session_state["ending_type"] = "good"
        st.session_state["progress"] = 1.0
        st.session_state["current_scene"] = case["scene_end"]
        show_achievement("真相大白", "🌟")

    push_message("assistant", reply)

def get_quick_questions() -> list:
    """根据当前剧本返回 4 个快捷提问示例。"""
    case = get_current_case()
    # 取前 4 条未解锁线索的第一个关键词
    examples = []
    for cid, info in case["clues"].items():
        if cid in st.session_state["unlocked_clues"]:
            continue
        # 抽取线索文本中的关键名词
        text = info["text"]
        # 简单策略：取 emoji 之后的第一个名词短语
        m = re.search(r"线索[①②③④⑤⑥⑦⑧⑨][：:]\s*([^，。；]+)", text)
        if m:
            phrase = m.group(1).strip()[:8]
            examples.append(f"与「{phrase}」有关吗？")
        if len(examples) >= 4:
            break
    if not examples:
        examples = ["真相是什么？", "你能再提示一下吗？"]
    return examples

def get_followup_for_clue(cid: str) -> list:
    """为某条线索生成 3 个追问模板。"""
    case = get_current_case()
    info = case["clues"][cid]
    # 抽取线索关键短语
    text = info["text"]
    m = re.search(r"线索[①②③④⑤⑥⑦⑧⑨][：:]\s*([^，。；]+)", text)
    phrase = m.group(1).strip()[:10] if m else "这条线索"
    return [
        f"「{phrase}」是被人故意留下的吗？",
        f"「{phrase}」和凶手有关吗？",
        f"「{phrase}」具体说明了什么？",
    ]

def render_chat():
    """
    渲染聊天区。

    打字机策略：
    - session_state["_typed_count"] 记录"已用打字机播放过的消息条数"。
    - 当消息数 > _typed_count 时，对**新增的 assistant 消息**走打字机播放，
      完成后 _typed_count += 1 并 rerun。
    - user 消息直接渲染，不走打字机。
    """
    messages = st.session_state["messages"]
    typed = st.session_state.get("_typed_count", 0)

    # 1) 已稳定渲染的消息：正常展示
    for m in messages[:typed]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    # 2) 边界处理：用户消息立即展示
    if typed < len(messages) and messages[typed]["role"] == "user":
        with st.chat_message("user"):
            st.markdown(messages[typed]["content"])
        st.session_state["_typed_count"] = typed + 1
        st.rerun()
        return

    # 3) 待打字机播放的 assistant 消息
    if typed < len(messages) and messages[typed]["role"] == "assistant":
        with st.chat_message("assistant"):
            placeholder = st.empty()
            typewriter(placeholder, messages[typed]["content"], speed=0.012)
        # 标记为已渲染
        st.session_state["_typed_count"] = typed + 1
        st.rerun()
        return

    # 4) 其余消息：直接渲染（兜底）
    for m in messages[typed:]:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

def render_sidebar():
    """渲染左侧侧边栏：剧本选择 / 进度 / 状态。"""
    case = get_current_case()
    with st.sidebar:
        st.markdown("## 🕯️ 案件档案")

        # —— 剧本选择 ——
        st.markdown("### 📚 选择剧本")
        ids = [c["id"] for c in CASE_LIST]
        try:
            cur_idx = ids.index(st.session_state["current_case"])
        except ValueError:
            cur_idx = 0
        chosen = st.radio(
            "案件库",
            options=ids,
            index=cur_idx,
            format_func=lambda x: f"{CASES[x]['icon']} {CASES[x]['title']}",
            label_visibility="collapsed",
        )
        if chosen != st.session_state["current_case"]:
            reset_for_new_case(chosen)
            st.rerun()

        st.markdown(
            f"<span class='case-tag'>{case['tag']}</span>",
            unsafe_allow_html=True,
        )
        st.markdown(f"**{case['title']}**")
        st.caption(case["bg"])

        st.markdown("---")
        st.markdown("### 🔎 线索收集进度")
        st.progress(st.session_state["progress"])
        st.markdown(
            f"已解锁 **{st.session_state['unlocked_count']} / {len(case['clues'])}** 条关键线索"
        )

        st.markdown("### 📜 已收集线索")
        if not st.session_state["unlocked_clues"]:
            st.caption("（尚无线索）")
        else:
            for cid in st.session_state["unlocked_clues"]:
                st.markdown(f"- {case['clues'][cid]['text']}")

        st.markdown("---")
        if st.button("🔄 重新开始当前案件", use_container_width=True):
            reset_for_new_case(st.session_state["current_case"])
            st.rerun()

def render_header():
    """渲染顶部：场景大图 + 霓虹标题 + 天气徽章。"""
    case = get_current_case()
    title_col, img_col = st.columns([1, 2])

    with title_col:
        st.markdown(
            f'<div class="neon-title">{case["icon"]} {case["title"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="neon-sub">{case["bg"]}</div>',
            unsafe_allow_html=True,
        )
    with img_col:
        scene_path = get_asset_path(st.session_state["current_scene"])
        st.markdown('<div class="scene-frame">', unsafe_allow_html=True)
        if has_asset(st.session_state["current_scene"]):
            st.image(scene_path, use_container_width=True, caption=None)
            st.markdown(
                '<div class="scene-caption">— 当前场景 —</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style='padding:60px 20px;text-align:center;
                background:linear-gradient(135deg,#1a0030,#001a30);
                color:#9adfff;letter-spacing:3px;'>
                📷 场景图占位<br/>
                <code style='color:#ff79c6'>{st.session_state['current_scene']}</code><br/>
                <small>请将同名图片放入脚本同目录即可生效</small>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

def render_hint():
    """渲染底部：思路提示（与当前剧本相关）。"""
    case = get_current_case()
    cid = case["id"]

    st.markdown("---")
    with st.expander("💡 不知道该问什么？点这里看思路提示", expanded=False):
        if cid == "lighthouse":
            tips = """
            你可以尝试围绕以下方向提问：
            - 当时的 **天气 / 风暴** 情况如何？
            - **灯塔** 里发生了什么？
            - 现场是否留下了 **纸 / 字条**？
            - 有没有 **杯子 / 咖啡 / 厨房** 相关的痕迹？
            - **值班日志** 是否有异常？
            - 户外是否有 **手套 / 鞋印** 等痕迹？
            - **望远镜 / 栏杆 / 瞭望台** 附近有什么？
            - 直接问 **真相 / 发生了什么 / 艾文** 也会触发结局。
            """
        elif cid == "cabin":
            tips = """
            你可以尝试围绕以下方向提问：
            - 暴风雪 **天气** 怎么样？
            - **木屋** 里发生了什么？
            - 听到 **枪声 / 子弹** 了吗？
            - **烟囱 / 窗户** 有没有异常？
            - 雪地 **鞋印 / 脚印** 是什么样？
            - 三人 **老周 / 小柯 / 阿林** 的笔记本 / 手机里有什么？
            - 有没有 **名片 / 救援** 相关人员？
            - 直接问 **真相 / 发生了什么 / 误杀** 也会触发结局。
            """
        else:  # metro
            tips = """
            你可以尝试围绕以下方向提问：
            - 站台 **监控 / 黑屏** 有异常吗？
            - 她 **刷卡 / 进站** 了吗？
            - **调度日志 / 时刻表** 有没有问题？
            - **调度员 / 老陈** 当晚穿了什么？
            - 站务室 **合影 / 照片** 里有什么？
            - **报纸 / 旧闻** 报道过什么？
            - 站台 **鞋印 / 广播** 有线索吗？
            - 直接问 **真相 / 发生了什么 / 值班员** 也会触发结局。
            """
        st.markdown(tips)

# ============================================================
# 四、主流程
# ============================================================
def main():
    # 全局霓虹主题 + 粒子背景
    inject_css()

    init_session_state()

    # 首次进入时插入欢迎语（来自当前剧本）
    if not st.session_state["messages"]:
        push_message("assistant", get_current_case()["intro"])

    # —— 1. 顶部沉浸式场景 ——
    render_header()

    # —— 1.5 动态天气层（覆盖全视口，不影响操作）——
    render_weather_layer()

    # —— 2. 主体三栏：中间聊天 / 右侧线索墙 ——
    mid, right = st.columns([2, 1])

    with mid:
        st.markdown("### 💬 推理对话")
        render_chat()

        # —— 快捷提问按钮（互动增强）——
        if not st.session_state["ended"]:
            st.markdown("#### ⚡ 试试这样问")
            quick_qs = get_quick_questions()
            # 用 form_submit_button 模拟多列按钮（每行 2 个）
            half = (len(quick_qs) + 1) // 2
            for row_start in range(0, len(quick_qs), half):
                row = quick_qs[row_start:row_start + half]
                cols = st.columns(len(row))
                for col, q in zip(cols, row):
                    if col.button(f"💡 {q}", key=f"quick_{hash(q)}_{row_start}", use_container_width=True):
                        process_user_question(q)
                        st.rerun()

        user_input = st.chat_input("向系统提问，例如：死者是自杀吗？")
        if user_input:
            process_user_question(user_input)
            st.rerun()

    with right:
        case = get_current_case()

        # —— 证据板（关联图谱）——
        render_evidence_board()

        st.markdown("### 🧩 线索墙")
        if not st.session_state["unlocked_clues"]:
            st.caption("尚未解锁任何线索。试试点击下方「⚡ 试试这样问」开始调查吧。")
        else:
            for cid in st.session_state["unlocked_clues"]:
                info = case["clues"][cid]
                st.markdown(
                    f"<div class='clue-card'>{info['text']}</div>",
                    unsafe_allow_html=True,
                )
                # —— 线索追问按钮（互动增强）——
                if not st.session_state["ended"]:
                    st.markdown('<div class="followup-area">', unsafe_allow_html=True)
                    st.markdown(
                        "<small style='color:#9adfff;'>🔎 基于这条线索继续问：</small>",
                        unsafe_allow_html=True,
                    )
                    followups = get_followup_for_clue(cid)
                    fcols = st.columns(len(followups))
                    for fc, fq in zip(fcols, followups):
                        if fc.button(fq, key=f"fu_{cid}_{hash(fq)}", use_container_width=True):
                            process_user_question(fq)
                            st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### ⏳ 状态")
        if st.session_state["ended"]:
            if st.session_state["ending_type"] == "good":
                st.markdown(
                    f"<div class='ending-banner'>✅ {case['endings']['good']}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='ending-banner'>⚠️ {case['endings']['bad']}</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.info("案件进行中……继续提问以推进剧情。")
            # —— 智能提示：当玩家卡住时 ——
            asked = st.session_state["unlocked_count"]
            if asked == 0:
                st.markdown(
                    "🧭 **建议方向**：从「时间 / 地点 / 人物」入手，例如问「事发时有几个人？」",
                )
            elif asked < 4:
                st.markdown(
                    f"🧭 **建议方向**：已收集 {asked} 条线索，可尝试问「现场还有什么异常？」或「凶手是谁？」",
                )

    # —— 3. 侧边栏 ——
    render_sidebar()

    # —— 4. 底部思路提示 ——
    render_hint()

if __name__ == "__main__":
    main()


