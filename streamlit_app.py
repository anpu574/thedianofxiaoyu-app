import streamlit as st
import random
import time

# --- 页面配置 ---
st.set_page_config(page_title="小玉的店模拟器", page_icon="💃", layout="wide")

# --- 初始化游戏状态 ---
if 'money' not in st.session_state:
    st.session_state.money = 1200.0  
    st.session_state.reputation = 85  
    st.session_state.staff = ["店主小玉", "收银员"] 
    st.session_state.logs = []
    st.session_state.energy = 100 # 新增：店长体力值
    st.session_state.role = None  # 新增：玩家角色身份

def add_log(msg, type="info"):
    icon = {"info": "💬", "success": "✨", "warning": "🔔", "danger": "🔥"}[type]
    st.session_state.logs.insert(0, f"{icon} {time.strftime('%H:%M')} - {msg}")

# --- 1. 角色代入系统 ---
if st.session_state.role is None:
    st.title("💃 欢迎来到【小玉的店】")
    st.subheader("在开店之前，请选择你的店长人设：")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("牛马型店长 (大厂背景，擅长熬夜加班"):
            st.session_state.role = "Scholar"
            st.session_state.reputation += 10
            st.rerun()
    with col2:
        if st.button("文艺型店长 (口才极佳，从风花雪夜到人生哲学)"):
            st.session_state.role = "Social"
            st.rerun()
    with col3:
        if st.button("硬核型店长 (眼神犀利，自带杀鱼师傅气质)"):
            st.session_state.role = "Hardcore"
            st.rerun()
    st.stop()

# --- 侧边栏：状态看板 ---
st.sidebar.header(f"🏪 小玉的店 ({st.session_state.role})")
st.sidebar.metric("营业额", f"￥{st.session_state.money:,.1f}")
st.sidebar.metric("店长体力", f"{st.session_state.energy}%")
st.sidebar.metric("店铺声望", f"{st.session_state.reputation}%")
st.sidebar.write(f"**在岗：** {', '.join(st.session_state.staff)}")

# --- 2. 店内午餐大转盘 (互动功能) ---
st.sidebar.markdown("---")
st.sidebar.subheader("🍴 店长能量补给")
if st.sidebar.button("🎡 开启午餐大转盘"):
    lunches = [
        ("豪华和牛宴", 50, -100), # (体力增加, 金钱消耗)
        ("麻辣烫", 20, -25),
        ("便利店饭团", 10, -10),
        ("饿肚子省钱", -10, 0),
        ("杀鱼师傅分你的盒饭", 30, 0)
    ]
    food, e_gain, m_cost = random.choice(lunches)
    st.session_state.energy += e_gain
    st.session_state.money += m_cost
    add_log(f"大转盘抽中了【{food}】！体力{e_gain}，花费￥{abs(m_cost)}", "success")

# --- 主界面 ---
st.title("💃 小玉的店：沉浸式模拟经营")

# --- 3. 特殊员工招聘 ---
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
    if "保洁" not in st.session_state.staff: st.button("招募保洁", on_click=hire, args=("保洁",))
with c2:
    if "保安" not in st.session_state.staff: st.button("招募保安", on_click=hire, args=("保安",))
with c3:
    if "售货员" not in st.session_state.staff: st.button("招募售货员", on_click=hire, args=("售货员",))
with c4:
    if "前大润发杀鱼的" not in st.session_state.staff: st.button("请杀鱼师傅", on_click=hire, args=("前大润发杀鱼的",))

st.markdown("---")

# --- 4. 营业逻辑与剧情互动 ---
st.subheader("🚀 营业中...")
if st.button("🕒 推进时间段 (消耗10%体力)"):
    if st.session_state.energy <= 0:
        st.error("店长体力透支，请先去转盘吃午饭！")
    else:
        st.session_state.energy -= 10
        events = ["大客户", "小偷", "逛了不买的人", "普通顾客", "特殊对话"]
        # 根据角色调整概率
        w = [10, 5, 35, 40, 10]
        if st.session_state.role == "Social": w[0] += 10 # 社牛大客户多
        if st.session_state.role == "Hardcore": w[1] = 1 # 硬核小偷不敢来
        
        event = random.choices(events, weights=w)[0]
        
        if event == "大客户":
            deal = random.randint(800, 2500)
            st.session_state.money += deal
            st.balloons()
            add_log(f"大客户进店！小玉亲自接待，谈成一笔￥{deal}的大单！", "success")
        
        elif event == "小偷":
            if any(x in st.session_state.staff for x in ["保安", "前大润发杀鱼的"]):
                add_log("小偷瞄了一眼杀鱼师傅寒气逼人的眼神，吓得当场自首。", "info")
            else:
                loss = random.randint(300, 600)
                st.session_state.money -= loss
                add_log(f"🚨 店内失窃！损失了价值￥{loss}的货品！", "danger")

        elif event == "特殊对话":
            dialogs = [
                "顾客问：‘老板，你长得像我一个喜欢安溥的朋友。’ (声望+5)",
                "隔壁铺位想蹭你的Wi-Fi。 (声望-2)",
                "保洁阿姨捡到了50元交还柜台。 (声望+10)"
            ]
            add_log(random.choice(dialogs))

        else:
            deal = random.randint(50, 200)
            st.session_state.money += deal
            add_log(f"生意平稳，入账￥{deal}")

# --- 日志与重置 ---
st.markdown("---")
st.write("📜 **店铺经营志**")
for log in st.session_state.logs[:8]:
    st.write(log)

if st.sidebar.button("🧨 倒闭重来"):
    for key in st.session_state.keys(): del st.session_state[key]
    st.rerun()
