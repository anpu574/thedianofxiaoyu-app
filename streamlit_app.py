import streamlit as st
import random
import time

# --- 页面配置 ---
st.set_page_config(page_title="小王的店模拟器", page_icon="🏪", layout="wide")

# --- 初始化游戏状态 ---
if 'money' not in st.session_state:
    st.session_state.money = 1000.0  # 初始资金
    st.session_state.reputation = 80  # 声望
    st.session_state.staff = ["店主小王", "收银员", "售货员"] # 初始员工
    st.session_state.logs = []
    st.session_state.day = 1

def add_log(msg, type="info"):
    icon = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "danger": "🚨"}[type]
    st.session_state.logs.insert(0, f"{icon} {time.strftime('%H:%M:%S')} - {msg}")

# --- 侧边栏：状态面板 ---
st.sidebar.header("🏪 小王的店 - 经营看板")
st.sidebar.metric("营业额 (元)", f"{st.session_state.money:,.2f}")
st.sidebar.metric("店铺声望", f"{st.session_state.reputation}%")
st.sidebar.write(f"**当前员工**: {', '.join(st.session_state.staff)}")

if st.sidebar.button("♻️ 重置店铺"):
    for key in st.session_state.keys(): del st.session_state[key]
    st.rerun()

# --- 主界面 ---
st.title("小王的店：沉浸式模拟经营")
st.write(f"📅 **第 {st.session_state.day} 天经营中...**")

# --- 第一步：招募特殊员工 ---
st.subheader("💡 招聘与准备")
col1, col2, col3 = st.columns(3)
with col1:
    if "保安" not in st.session_state.staff:
        if st.button("招募保安 (-200元)"):
            if st.session_state.money >= 200:
                st.session_state.money -= 200
                st.session_state.staff.append("保安")
                add_log("招募了保安，店铺安全性提升！")
                st.rerun()
with col2:
    if "前大润发杀鱼的" not in st.session_state.staff:
        if st.button("请杀鱼师傅坐镇 (-500元)"):
            if st.session_state.money >= 500:
                st.session_state.money -= 500
                st.session_state.staff.append("前大润发杀鱼的")
                add_log("杀鱼师傅就位，那眼神，小偷看了都发憷。", "success")
                st.rerun()
with col3:
    if "保洁" not in st.session_state.staff:
        if st.button("招募保洁 (-100元)"):
            if st.session_state.money >= 100:
                st.session_state.money -= 100
                st.session_state.staff.append("保洁")
                add_log("店面变得干净整洁了。")
                st.rerun()

st.markdown("---")

# --- 第二步：开始营业（触发随机角色事件） ---
st.subheader("🚀 营业互动区")
if st.button("🕒 推进时间（迎接下一波客人）"):
    # 角色库及触发概率
    events = ["大客户", "小偷", "逛了不买的人", "普通顾客"]
    weights = [10, 5, 40, 45] # 初始概率
    
    # 角色逻辑修正
    if "前大润发杀鱼的" in st.session_state.staff:
        weights[1] = 0.5 # 小偷概率骤降
    
    event = random.choices(events, weights=weights)[0]
    
    if event == "大客户":
        deal = random.randint(500, 2000)
        st.session_state.money += deal
        st.balloons()
        add_log(f"大客户进店！由【收银员】结账，入账 {deal} 元！", "success")
        
    elif event == "小偷":
        if "保安" in st.session_state.staff or "前大润发杀鱼的" in st.session_state.staff:
            add_log("小偷刚伸手，就被盯得心里发虚，溜了。", "info")
        else:
            loss = random.randint(200, 500)
            st.session_state.money -= loss
            add_log(f"🚨 糟糕！小偷光顾，损失了价值 {loss} 元的商品！", "danger")
            
    elif event == "逛了不买的人":
        if "保洁" not in st.session_state.staff:
            st.session_state.reputation -= 2
            add_log("逛了不买的人吐了口痰走了，地面变脏，声望下降。", "warning")
        else:
            add_log("有人逛了一圈没买，【保洁】立刻上前清理了地面。")
            
    elif event == "普通顾客":
        deal = random.randint(20, 100)
        st.session_state.money += deal
        add_log(f"普通顾客消费了 {deal} 元。")

# --- 第三步：结算与评语 ---
st.markdown("---")
st.write("📜 **店铺动态日志**")
for log in st.session_state.logs[:10]: # 只显示最近10条
    st.write(log)

if st.session_state.money <= 0:
    st.error("💀 店铺破产了！小王决定回实验室继续算湍流级联...")
    if st.button("重新创业"):
        for key in st.session_state.keys(): del st.session_state[key]
        st.rerun()
