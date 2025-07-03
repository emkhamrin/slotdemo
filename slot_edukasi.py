import streamlit as st
import random
import time

st.set_page_config(page_title="🎰 Chinese Luck Slot - Edukasi Anti Judi", layout="centered")

symbols = ['🐉', '💎', '❤️', '🔷', '🀄️', '🎴', '🔶', '🔶', '💰', '🎊', '🎎', '🎯']
symbol_names = ["WILD", "SCATTER", "HEART", "BLUE", "RED", "CARD", "GREEN", "BONUS", "JACKPOT", "10", "Q", "K"]
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
.spin-btn {
    background-color: red;
    color: white;
    padding: 10px 20px;
    font-size: 20px;
    border-radius: 50%;
    border: none;
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

saldo_area = st.empty()
grid_area = st.empty()
hasil_area = st.empty()

col1, col2 = st.columns(2)
with col1:
    harga_per_spin = st.number_input("Harga per Spin", min_value=10, value=100, step=10)
    total_spin = st.number_input("Total Spin", min_value=10, value=50, step=10)
with col2:
    target_rtp = st.slider("Target RTP (%)", min_value=50, max_value=99, value=96)
    modal_awal = st.number_input("Modal Awal", min_value=100, value=3000, step=100)

if st.button("SPIN", key="spinbtn"):

    total_biaya = total_spin * harga_per_spin
    max_total_kembali = total_biaya * (target_rtp / 100)

    jackpot_ke = random.randint(1, total_spin)
    jackpot_terjadi = False

    modal = modal_awal
    total_kembali = 0
    total_menang = 0
    total_jackpot = 0

    saldo_area.markdown(f"<div class='balance-box'>Balance: {modal} credit</div>", unsafe_allow_html=True)

    for spin in range(1, total_spin + 1):
        modal -= harga_per_spin

        for _ in range(6):
            grid_data = random.choices(symbols, weights_awal, k=12)
            grid_html = "<div class='slot-grid'>"
            for s in grid_data:
                grid_html += f"<div class='slot-cell'>{s}</div>"
            grid_html += "</div>"
            grid_area.markdown(grid_html, unsafe_allow_html=True)
            time.sleep(0.1)

        weights = weights_sulit if jackpot_terjadi else weights_awal
        hasil_final = random.choices(symbols, weights, k=12)

        hadiah = 0
        if spin == jackpot_ke:
            hasil_final = ['💰'] * 12
            hadiah = prize_table['💰'] * harga_per_spin
            jackpot_terjadi = True
        elif hasil_final[4] == hasil_final[5] == hasil_final[6]:
            simbol_menang = hasil_final[4]
            hadiah = prize_table.get(simbol_menang, 0) * harga_per_spin

        grid_html = "<div class='slot-grid'>"
        for i, s in enumerate(hasil_final):
            warna = "gold" if hadiah > 0 and i in [4,5,6] else "white"
            grid_html += f"<div class='slot-cell' style='color:{warna};'>{s}</div>"
        grid_html += "</div>"

        grid_area.markdown(grid_html, unsafe_allow_html=True)

        if total_kembali + hadiah <= max_total_kembali:
            if hadiah > 0:
                modal += hadiah
                total_kembali += hadiah
                total_menang += 1
                if hasil_final[4] == '💰':
                    total_jackpot += 1

        saldo_area.markdown(f"<div class='balance-box'>Balance: {modal} credit</div>", unsafe_allow_html=True)

        if hadiah > 0:
            hasil_area.markdown(f"<div class='big-win'>YOU WIN {hadiah} credit!</div>", unsafe_allow_html=True)
            time.sleep(1)
        else:
            hasil_area.empty()
            time.sleep(0.3)

        if modal <= 0:
            st.error(f"Modal habis di spin ke-{spin}")
            break

    rtp_real = (total_kembali / (spin * harga_per_spin)) * 100

    st.success(f"Selesai! Total Spin: {spin}, Menang: {total_menang}, Jackpot: {total_jackpot}")
    st.info(f"Total Kemenangan: {total_kembali} credit | Modal Akhir: {modal} | RTP Realisasi: {rtp_real:.2f}%")
    st.warning("⚠️ Simulasi edukasi. Slot sengaja dikontrol merugikan pemain jangka panjang.")


