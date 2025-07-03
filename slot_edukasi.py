import streamlit as st
import random
import time

st.set_page_config(page_title="🎰 Chinese Luck Slot - Edukasi Anti Judi", layout="centered")

symbols = ['🍒', '💎', '7️⃣', '🍋', '🔔']
weights_awal = [0.4, 0.3, 0.15, 0.1, 0.05]
weights_sulit = [0.5, 0.3, 0.15, 0.049, 0.001]

st.markdown("""
<style>
.slot-grid {
    display: grid;
    grid-template-columns: repeat(3, 80px);
    grid-template-rows: repeat(1, 80px);
    grid-gap: 8px;
    justify-content: center;
    margin: 15px 0;
}
.slot-cell {
    border: 3px solid #DAA520;
    border-radius: 6px;
    font-size: 36px;
    text-align: center;
    line-height: 80px;
    height: 80px;
    width: 80px;
    background-color: #442200;
    color: white;
}
.balance-box {
    background-color: #222;
    padding: 8px;
    color: gold;
    text-align: center;
    border-radius: 5px;
    margin-bottom: 10px;
}
.big-win {
    font-size: 28px;
    color: gold;
    text-align: center;
    animation: blink 1s infinite;
}
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

st.title("🎰 Chinese Luck - Slot Edukasi Anti Judi")

if "modal" not in st.session_state:
    st.session_state.modal = 3000
if "grid_display" not in st.session_state:
    st.session_state.grid_display = random.choices(symbols, weights_awal, k=3)
if "jackpot_ke" not in st.session_state:
    st.session_state.jackpot_ke = random.randint(1, 100_000)
if "jackpot_terjadi" not in st.session_state:
    st.session_state.jackpot_terjadi = False
if "total_kembali" not in st.session_state:
    st.session_state.total_kembali = 0

modal_awal = st.number_input("Modal Awal", min_value=100, value=3000, step=100)
harga_per_spin = st.number_input("Harga per Spin", min_value=10, value=100, step=10)
target_rtp = st.slider("Target RTP (%)", min_value=50, max_value=99, value=96)

prize_table = {
    '🍒': 5 * harga_per_spin,
    '💎': 10 * harga_per_spin,
    '7️⃣': 50 * harga_per_spin,
    '🍋': 15 * harga_per_spin,
    '🔔': 5000 * harga_per_spin
}

if st.button("Reset Modal"):
    st.session_state.modal = modal_awal
    st.session_state.total_kembali = 0
    st.session_state.jackpot_ke = random.randint(1, 100_000)
    st.session_state.jackpot_terjadi = False

saldo_area = st.empty()
grid_area = st.empty()
hasil_area = st.empty()

# Grid selalu tampil
grid_html = "<div class='slot-grid'>"
for s in st.session_state.grid_display:
    grid_html += f"<div class='slot-cell'>{s}</div>"
grid_html += "</div>"
grid_area.markdown(grid_html, unsafe_allow_html=True)
saldo_area.markdown(f"<div class='balance-box'>Balance: {st.session_state.modal} credit</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
if col1.button("Spin Sekali"):
    if st.session_state.modal < harga_per_spin:
        st.error("Modal tidak cukup untuk spin.")
    else:
        st.session_state.modal -= harga_per_spin

        weights = weights_sulit if st.session_state.jackpot_terjadi else weights_awal
        hasil_final = random.choices(symbols, weights, k=3)
        hadiah = 0

        if st.session_state.jackpot_ke == 1:
            hasil_final = ['🔔', '🔔', '🔔']
            hadiah = prize_table['🔔']
            st.session_state.jackpot_terjadi = True
        elif hasil_final[0] == hasil_final[1] == hasil_final[2]:
            simbol_menang = hasil_final[0]
            hadiah = prize_table.get(simbol_menang, 0)

        if st.session_state.total_kembali + hadiah <= (harga_per_spin * target_rtp * 0.01):
            st.session_state.modal += hadiah
            st.session_state.total_kembali += hadiah

        st.session_state.grid_display = hasil_final

        grid_html = "<div class='slot-grid'>"
        for i, s in enumerate(hasil_final):
            warna = "gold" if hadiah > 0 else "white"
            grid_html += f"<div class='slot-cell' style='color:{warna};'>{s}</div>"
        grid_html += "</div>"
        grid_area.markdown(grid_html, unsafe_allow_html=True)

        saldo_area.markdown(f"<div class='balance-box'>Balance: {st.session_state.modal} credit</div>", unsafe_allow_html=True)

        if hadiah > 0:
            hasil_area.markdown(f"<div class='big-win'>YOU WIN {hadiah} credit!</div>", unsafe_allow_html=True)
        else:
            hasil_area.empty()

with st.expander("Auto Spin (Advanced Setting)"):
    total_spin_auto = st.number_input("Jumlah Spin Auto", min_value=1, max_value=500, value=50, step=1)
    if st.button("Start Auto Spin"):
        for spin in range(total_spin_auto):
            if st.session_state.modal < harga_per_spin:
                st.warning("Modal habis, auto spin berhenti.")
                break

            st.session_state.modal -= harga_per_spin

            weights = weights_sulit if st.session_state.jackpot_terjadi else weights_awal
            hasil_final = random.choices(symbols, weights, k=3)
            hadiah = 0

            if st.session_state.jackpot_ke == 1:
                hasil_final = ['🔔', '🔔', '🔔']
                hadiah = prize_table['🔔']
                st.session_state.jackpot_terjadi = True
            elif hasil_final[0] == hasil_final[1] == hasil_final[2]:
                simbol_menang = hasil_final[0]
                hadiah = prize_table.get(simbol_menang, 0)

            if st.session_state.total_kembali + hadiah <= (harga_per_spin * target_rtp * 0.01):
                st.session_state.modal += hadiah
                st.session_state.total_kembali += hadiah

            st.session_state.grid_display = hasil_final

            grid_html = "<div class='slot-grid'>"
            for i, s in enumerate(hasil_final):
                warna = "gold" if hadiah > 0 else "white"
                grid_html += f"<div class='slot-cell' style='color:{warna};'>{s}</div>"
            grid_html += "</div>"
            grid_area.markdown(grid_html, unsafe_allow_html=True)

            saldo_area.markdown(f"<div class='balance-box'>Balance: {st.session_state.modal} credit</div>", unsafe_allow_html=True)

            if hadiah > 0:
                hasil_area.markdown(f"<div class='big-win'>YOU WIN {hadiah} credit!</div>", unsafe_allow_html=True)
            else:
                hasil_area.empty()

            time.sleep(0.1)

with st.expander("Simulasi Tanpa Animasi"):
    total_spin_sim = st.number_input("Total Spin Simulasi", min_value=10, value=1000, step=100)
    if st.button("Simulate"):
        modal = st.session_state.modal
        total_kembali = 0
        jackpot_ke = random.randint(1, total_spin_sim)
        jackpot_terjadi = False
        total_menang = 0

        st.info(f"🎯 Jackpot besar akan keluar di spin ke-{jackpot_ke} (backend tersembunyi)")

        for spin in range(1, total_spin_sim + 1):
            if modal < harga_per_spin:
                st.warning(f"Modal habis di spin ke-{spin}")
                break

            modal -= harga_per_spin

            weights = weights_sulit if jackpot_terjadi else weights_awal
            hasil_final = random.choices(symbols, weights, k=3)
            hadiah = 0

            if spin == jackpot_ke:
                hasil_final = ['🔔', '🔔', '🔔']
                hadiah = prize_table['🔔']
                jackpot_terjadi = True
            elif hasil_final[0] == hasil_final[1] == hasil_final[2]:
                simbol_menang = hasil_final[0]
                hadiah = prize_table.get(simbol_menang, 0)

            if total_kembali + hadiah <= (harga_per_spin * total_spin_sim * target_rtp * 0.01):
                if hadiah > 0:
                    modal += hadiah
                    total_kembali += hadiah
                    total_menang += 1

        st.session_state.modal = modal
        saldo_area.markdown(f"<div class='balance-box'>Balance: {modal} credit</div>", unsafe_allow_html=True)

        rtp_real = (total_kembali / (spin * harga_per_spin)) * 100 if spin > 0 else 0
        st.info(f"Total Kemenangan: {total_kembali} credit | Total Menang: {total_menang} | RTP Realisasi: {rtp_real:.2f}%")
        st.info(f"Jackpot besar keluar di spin ke-{jackpot_ke}")


