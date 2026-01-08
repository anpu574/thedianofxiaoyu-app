import streamlit as st
import random
import time

# --- 页面配置 ---
st.set_page_config(page_title="小玉的店模拟器", page_icon="💃", layout="wide")

# --- 初始化游戏状态 (这是游戏的“大脑”，保证数据不丢) ---
if 'money' not in st.session_state:
    st.session_state.money = 1200.0  
    st.session_state.reputation = 85  
    st.session_state.staff = ["店主小玉", "收银员"] 
    st.session_state.logs = []
    st.session_state.energy = 100 
    st.session_state.role = None  
    st.session_state.lunch_result = "还没吃饭呢，快转转盘！" # 初始文字

# --- 日志函数 ---
def add_log(msg, type="info"):
    icon = {"info": "💬", "success": "✨", "warning": "🔔", "danger": "🔥"}[type]
    st.session_state.logs.insert(0, f"{icon} {time.strftime('%H:%M')} - {msg}")

# --- 转盘核心逻辑 (使用回调函数，确保 100% 运行) ---
def spin_roulette():
    lunches = [
        ("豪华和牛宴", 50, -100), 
        ("麻辣烫", 20, -25),
        ("便利店饭团", 10, -10),
        ("饿肚子省钱", -10, 0),
        ("杀鱼师傅分你的盒饭", 30, 0)
    ]
    food, e_gain, m_cost = random.choice(lunches)
    
    # 直接修改状态
    st.session_state.energy += e_gain
    st.session_state.money += m_cost
    result_text = f"🎡 抽中了【{food}】！体力+{e_gain}，花费￥{abs(m_cost)}"
    st.session_state.lunch_result = result_text # 永久保存结果
    add_log(result_text, "success")

# --- 1. 角色代入系统 ---
if st.session_state.role is None:
    st.title("💃 欢迎来到【小玉的店】")
    st.subheader("在开店之前，请选择你的店长人设：")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("牛马型店长 (大厂背景，擅长熬夜加班)"):
            st.session_state.role = "牛马型"
            st.session_state.reputation += 10
            st.rerun()
    with col2:
        if st.button("文艺型店长 (口才极佳，从风花雪夜到人生哲学)"):
            st.session_state.role = "文艺型"
            st.rerun()
    with col3:
        if st.button("硬核型店长 (眼神犀利，自带杀鱼师傅气质)"):
            st.session_state.role = "硬核型"
            st.rerun()
    st.stop()

# --- 侧边栏：状态面板 ---
st.sidebar.header(f"🏪 小玉的店 ({st.session_state.role})")
st.sidebar.metric("营业额", f"￥{st.session_state.money:,.1f}")
st.sidebar.metric("店长体力", f"{st.session_state.energy}%")
st.sidebar.metric("店铺声望", f"{st.session_state.reputation}%")
st.sidebar.write(f"**在岗：** {', '.join(st.session_state.staff)}")

# --- 2. 修复后的转盘 (关键修改点) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🍴 店长能量补给")
# 使用 on_click 绑定函数，这是最稳的方法
st.sidebar.button("🎡 点击开启转盘", on_click=spin_roulette)
# 始终显示上一次的结果
st.sidebar.info(st.session_state.lunch_result)

# --- 主界面 ---
st.title("💃 小玉的店：沉浸式经营")

# --- 3. 团队组建 ---
st.subheader("🧩 团队组建")
c1, c2, c3, c4 = st.columns(4)
staff_prices = {"保洁": 100, "保安": 200, "售货员": 150, "前大润发杀鱼的": 500}

def hire(name):
    if name not in st.session_state.staff and st.session_state.money >= staff_prices[name]:
        st.session_state.money -= staff_prices[name]
        st.session_state.staff.append(name)
        add_log(f"成功聘请了【{name}】！", "success")
        st.rerun()

with c1: 
    if "保洁" not in st.session_state.staff: st.button(f"招募保洁 (￥100)", on_click=hire, args=("保洁",))
with c2:
    if "保安" not in st.session_state.staff: st.button(f"招募保安 (￥200)", on_click=hire, args=("保安",))
with c3:
    if "售货员" not in st.session_state.staff: st.button(f"招募售货员 (￥150)", on_click=hire, args=("售货员",))
with c4:
    if "前大润发杀鱼的" not in st.session_state.staff: st.button(f"杀鱼师傅 (￥500)", on_click=hire, args=("前大润发杀鱼的",))

st.markdown("---")

# --- 4. 营业逻辑 ---
st.subheader("🚀 营业互动区")
if st.button("🕒 推进时间 (消耗10%体力)"):
    if st.session_state.energy <= 0:
        st.error("店长体力透支，请点击左侧转盘吃饭！")
    else:
        st.session_state.energy -= 10
        events = ["大客户", "小偷", "逛了不买", "普通顾客", "特殊对话", "扎心事件"]
        w = [10, 5, 25, 40, 10, 10]
        
        event = random.choices(events, weights=w)[0]
        
        if event == "大客户":
            deal = random.randint(800, 2500)
            st.session_state.money += deal
            st.balloons()
            add_log(f"大客户进店！小玉亲自接待，谈成￥{deal}大单！", "success")
        
        elif event == "小偷":
            if any(x in st.session_state.staff for x in ["保安", "前大润发杀鱼的"]):
                add_log("小偷看见杀鱼师傅的刀，吓得掉头就跑。", "info")
            else:
                loss = random.randint(300, 600)
                st.session_state.money -= loss
                add_log(f"🚨 店内失窃！损失￥{loss}！", "danger")

        elif event == "扎心事件":
            pains = ["外卖被偷了！ (体力-15)", "收银机死机 (体力-10)", "被恶意投诉 (声望-10)"]
            p = random.choice(pains)
            add_log(f"😵 {p}", "warning")
            if "-15" in p: st.session_state.energy -= 15
            if "-10" in p: st.session_state.energy -= 10

        elif event == "特殊对话":
            add_log("顾客：老板，你这店的装修风格真有品位。 (声望+5)")
        else:
            deal = random.randint(50, 200)
            st.session_state.money += deal
            add_log(f"入账￥{deal}")

# --- 5. 日志与重置 ---
st.markdown("---")
st.write("📜 **经营日志**")
for log in st.session_state.logs[:8]:
    st.write(log)

if st.sidebar.button("🧨 倒闭重来"):
    for key in st.session_state.keys(): del st.session_state[key]
    st.rerun()
