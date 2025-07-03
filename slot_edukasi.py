import streamlit as st
import random
import time

st.set_page_config(page_title="🎰 Chinese Luck Slot - Edukasi Anti Judi", layout="centered")

symbols = ['🐉', '💎', '❤️', '🔷', '🀄️', '🎴', '🔶', '🔶', '💰', '🎊', '🎎', '🎯']
prize_table = {
    '🐉': 20,
    '💰': 5000,
    '❤️': 10,
    '💎': 15,
    '🀄️': 25,
    '🎊': 50
}

weights_awal = [0.1, 0.05, 0.15, 0.2, 0.1, 0.1, 0.1, 0.05, 0.005, 0.05, 0.05, 0.05]
weights_sulit = [0.15, 0.05, 0.15, 0.2, 0.1, 0.1, 0.1, 0.049, 0.001, 0.05, 0.05, 0.05]

st.markdown("""
<style>
.slot-grid {
    display: grid;
    grid-template-columns: repeat(3, 80px);
    grid-template-rows: repeat(4, 80px);
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
    st.session_state.grid_display = random.choices(symbols, weights_awal, k=12)

modal_awal = st.number_input("Modal Awal", min_value=100, value=3000, step=100)
harga_per_spin = st.number_input("Harga per Spin", min_value=10, value=100, step=10)
target_rtp = st.slider("Target RTP (%)", min_value=50, max_value=99, value=96)

if st.button("Reset Modal"):
    st.session_state.modal = modal_awal

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
    hasil_final = random.choices(symbols, weights_awal, k=12)
    st.session_state.grid_display = hasil_final

    hadiah = 0
    if hasil_final[4] == hasil_final[5] == hasil_final[6]:
        simbol_menang = hasil_final[4]
        hadiah = prize_table.get(simbol_menang, 0) * harga_per_spin

    st.session_state.modal -= harga_per_spin
    st.session_state.modal += hadiah

    grid_html = "<div class='slot-grid'>"
    for i, s in enumerate(hasil_final):
        warna = "gold" if hadiah > 0 and i in [4,5,6] else "white"
        grid_html += f"<div class='slot-cell' style='color:{warna};'>{s}</div>"
    grid_html += "</div>"
    grid_area.markdown(grid_html, unsafe_allow_html=True)

    saldo_area.markdown(f"<div class='balance-box'>Balance: {st.session_state.modal} credit</div>", unsafe_allow_html=True)

    if hadiah > 0:
        hasil_area.markdown(f"<div class='big-win'>YOU WIN {hadiah} credit!</div>", unsafe_allow_html=True)
    else:
        hasil_area.empty()

with st.expander("Auto Spin Advanced Setting"):
    total_spin = st.number_input("Total Spin Auto", min_value=10, value=50, step=10)
    if st.button("Mulai Auto Spin"):
        total_biaya = total_spin * harga_per_spin
        max_total_kembali = total_biaya * (target_rtp / 100)

        modal = st.session_state.modal
        total_kembali = 0
        total_menang = 0

        for spin in range(1, total_spin + 1):
            hasil_final = random.choices(symbols, weights_awal, k=12)
            hadiah = 0

            if hasil_final[4] == hasil_final[5] == hasil_final[6]:
                simbol_menang = hasil_final[4]
                hadiah = prize_table.get(simbol_menang, 0) * harga_per_spin

            if modal < harga_per_spin:
                st.error(f"Modal habis di spin ke-{spin}")
                break

            modal -= harga_per_spin
            if total_kembali + hadiah <= max_total_kembali and hadiah > 0:
                modal += hadiah
                total_kembali += hadiah
                total_menang += 1

            saldo_area.markdown(f"<div class='balance-box'>Balance: {modal} credit</div>", unsafe_allow_html=True)
            st.session_state.grid_display = hasil_final

            grid_html = "<div class='slot-grid'>"
            for i, s in enumerate(hasil_final):
                warna = "gold" if hadiah > 0 and i in [4,5,6] else "white"
                grid_html += f"<div class='slot-cell' style='color:{warna};'>{s}</div>"
            grid_html += "</div>"
            grid_area.markdown(grid_html, unsafe_allow_html=True)

            time.sleep(0.2)

        st.session_state.modal = modal
        hasil_area.empty()
        st.success(f"Auto Spin selesai. Total Menang: {total_menang}")

st.markdown("---")

st.subheader("Simulasi Tanpa Animasi")
total_spin_sim = st.number_input("Total Spin Simulasi", min_value=10, value=1000, step=100)
if st.button("Simulate"):
    total_biaya = total_spin_sim * harga_per_spin
    max_total_kembali = total_biaya * (target_rtp / 100)

    modal = st.session_state.modal
    total_kembali = 0
    total_menang = 0

    for spin in range(1, total_spin_sim + 1):
        hasil_final = random.choices(symbols, weights_awal, k=12)
        hadiah = 0

        if hasil_final[4] == hasil_final[5] == hasil_final[6]:
            simbol_menang = hasil_final[4]
            hadiah = prize_table.get(simbol_menang, 0) * harga_per_spin

        if modal < harga_per_spin:
            st.warning(f"Modal habis di spin ke-{spin}")
            break

        modal -= harga_per_spin

        if total_kembali + hadiah <= max_total_kembali and hadiah > 0:
            modal += hadiah
            total_kembali += hadiah
            total_menang += 1

    st.session_state.modal = modal
    saldo_area.markdown(f"<div class='balance-box'>Balance: {modal} credit</div>", unsafe_allow_html=True)
    rtp_real = (total_kembali / (spin * harga_per_spin)) * 100 if spin > 0 else 0
    st.info(f"Total Kemenangan: {total_kembali} credit | Total Menang: {total_menang} | RTP Realisasi: {rtp_real:.2f}%")


