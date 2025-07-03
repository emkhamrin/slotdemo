import streamlit as st
import random
import time

st.set_page_config(page_title="🎰 Slot Edukasi Anti Judi", layout="centered")

symbols = ['🍒', '💎', '7️⃣', '🍋', '🔔']
weights_awal = [0.4, 0.3, 0.15, 0.1, 0.05]
weights_sulit = [0.5, 0.3, 0.15, 0.049, 0.001]

prize_table = {
    '🍒': 5,
    '💎': 10,
    '7️⃣': 50,
    '🍋': 15,
    '🔔': 5000
}

st.markdown("""
<style>
.slot-grid {
    display: grid;
    grid-template-columns: repeat(3, 80px);
    grid-gap: 10px;
    justify-content: center;
    margin-bottom: 20px;
}
.slot-cell {
    border: 3px solid #FFD700;
    border-radius: 8px;
    font-size: 36px;
    text-align: center;
    line-height: 80px;
    height: 80px;
    width: 80px;
    background-color: black;
    color: white;
}
.big-win {
    font-size: 32px;
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

st.title("🎰 Slot Edukasi Old School - Anti Judi")

col1, col2 = st.columns(2)
with col1:
    harga_per_spin = st.number_input("Harga per Spin (credit)", min_value=1, value=100)
    total_spin = st.number_input("Total Spin", min_value=10, value=50, step=10)
with col2:
    target_rtp = st.slider("Target RTP (%)", min_value=50, max_value=99, value=96)

if st.button("Mulai Spin"):
    st.markdown("---")
    grid_area = st.empty()
    hasil_area = st.empty()
    saldo_area = st.empty()

    total_biaya = total_spin * harga_per_spin
    max_total_kembali = total_biaya * (target_rtp / 100)

    jackpot_ke = random.randint(1, total_spin)
    jackpot_terjadi = False

    modal = harga_per_spin * 300
    total_kembali = 0
    total_menang = 0
    total_jackpot = 0

    grid_data = ["" for _ in range(9)]

    for spin in range(1, total_spin + 1):
        modal -= harga_per_spin

        for _ in range(8):
            grid_data = random.choices(symbols, weights_awal, k=9)
            grid_html = "<div class='slot-grid'>"
            for s in grid_data:
                grid_html += f"<div class='slot-cell'>{s}</div>"
            grid_html += "</div>"
            grid_area.markdown(grid_html, unsafe_allow_html=True)
            time.sleep(0.1)

        weights = weights_sulit if jackpot_terjadi else weights_awal
        hasil_final = random.choices(symbols, weights, k=9)

        hadiah = 0
        if spin == jackpot_ke:
            hasil_final = ['🔔'] * 9
            hadiah = prize_table['🔔'] * harga_per_spin
            jackpot_terjadi = True
        elif hasil_final[3] == hasil_final[4] == hasil_final[5]:
            simbol_menang = hasil_final[4]
            hadiah = prize_table.get(simbol_menang, 0) * harga_per_spin

        grid_html = "<div class='slot-grid'>"
        for i, s in enumerate(hasil_final):
            warna = "gold" if hadiah > 0 and i in [3,4,5] else "white"
            grid_html += f"<div class='slot-cell' style='color:{warna};'>{s}</div>"
        grid_html += "</div>"
        grid_area.markdown(grid_html, unsafe_allow_html=True)

        if total_kembali + hadiah <= max_total_kembali:
            if hadiah > 0:
                modal += hadiah
                total_kembali += hadiah
                total_menang += 1
                if hasil_final[4] == '🔔':
                    total_jackpot += 1

        saldo_area.info(f"Balance: {modal} credit")

        if hadiah > 0:
            hasil_area.markdown(f"<div class='big-win'>YOU WIN: {hadiah} credit!</div>", unsafe_allow_html=True)
            time.sleep(1)
        else:
            hasil_area.empty()
            time.sleep(0.3)

        if modal <= 0:
            st.error(f"Modal habis di spin ke-{spin}")
            break

    rtp_real = (total_kembali / (spin * harga_per_spin)) * 100

    st.success(f"Selesai! Total Spin: {spin}, Total Menang: {total_menang}, Jackpot 5000x: {total_jackpot}")
    st.info(f"Total Kemenangan: {total_kembali} credit | Modal Akhir: {modal} credit | RTP Realisasi: {rtp_real:.2f}%")
    st.warning("⚠️ Ini simulasi edukasi. Slot dirancang merugikan pemain jangka panjang.")

