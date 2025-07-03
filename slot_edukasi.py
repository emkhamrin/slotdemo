import streamlit as st
import random
import time

st.set_page_config(page_title="🎰 Slot Edukasi Anti Judi", layout="centered")

symbols = ['🍒', '💎', '7️⃣', '🍋', '🔔']
weights_awal = [0.4, 0.3, 0.15, 0.1, 0.05]
weights_sulit = [0.5, 0.3, 0.15, 0.049, 0.001]

st.title("🎰 Slot Edukasi - Anti Judi")

harga_per_spin = st.number_input("Harga per Spin", min_value=10, value=100, step=10)
total_spin_sim = st.number_input("Total Spin Simulasi", min_value=10, value=1000, step=100)
target_rtp = st.slider("Target RTP (%)", min_value=50, max_value=99, value=96)
modal_awal = st.number_input("Modal Awal (Kelipatan Harga Spin)", min_value=10, value=300, step=10)

prize_table = {
    '🍒': 5 * harga_per_spin,
    '💎': 10 * harga_per_spin,
    '7️⃣': 50 * harga_per_spin,
    '🍋': 15 * harga_per_spin,
    '🔔': 5000 * harga_per_spin
}

if "modal" not in st.session_state:
    st.session_state.modal = harga_per_spin * modal_awal
if "grid_display" not in st.session_state:
    st.session_state.grid_display = random.choices(symbols, weights_awal, k=3)
if "jackpot_ke" not in st.session_state:
    st.session_state.jackpot_ke = random.randint(1, 100_000)
if "jackpot_terjadi" not in st.session_state:
    st.session_state.jackpot_terjadi = False
if "total_kembali" not in st.session_state:
    st.session_state.total_kembali = 0

saldo_area = st.empty()
grid_area = st.empty()
hasil_area = st.empty()

saldo_area.markdown(f"**Balance:** {st.session_state.modal} credit")
grid_html = "<div class='slot-grid'>"
for s in st.session_state.grid_display:
    grid_html += f"<div class='slot-cell'>{s}</div>"
grid_html += "</div>"
grid_area.markdown(grid_html, unsafe_allow_html=True)

if st.button("Spin Sekali"):
    if st.session_state.modal < harga_per_spin:
        st.error("Modal tidak cukup!")
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
            hadiah = prize_table.get(hasil_final[0], 0)

        total_biaya = harga_per_spin * 1
        max_total_kembali = total_biaya * (target_rtp / 100)

        if st.session_state.total_kembali + hadiah <= max_total_kembali:
            st.session_state.modal += hadiah
            st.session_state.total_kembali += hadiah

        st.session_state.grid_display = hasil_final
        grid_html = "<div class='slot-grid'>"
        for s in hasil_final:
            grid_html += f"<div class='slot-cell'>{s}</div>"
        grid_html += "</div>"

        grid_area.markdown(grid_html, unsafe_allow_html=True)
        saldo_area.markdown(f"**Balance:** {st.session_state.modal} credit")
        if hadiah > 0:
            hasil_area.success(f"YOU WIN {hadiah} credit!")
        else:
            hasil_area.empty()

if st.button("Reset Modal"):
    st.session_state.modal = harga_per_spin * modal_awal
    st.session_state.grid_display = random.choices(symbols, weights_awal, k=3)
    st.session_state.jackpot_ke = random.randint(1, 100_000)
    st.session_state.jackpot_terjadi = False
    st.session_state.total_kembali = 0

st.markdown("---")

if st.button("Simulate Tanpa Animasi"):
    modal = harga_per_spin * modal_awal
    jackpot_ke = random.randint(1, total_spin_sim)
    jackpot_terjadi = False

    total_kembali = 0
    total_menang = 0

    total_biaya = total_spin_sim * harga_per_spin
    max_total_kembali = total_biaya * (target_rtp / 100)

    st.info(f"🎯 Jackpot 5000x akan keluar di spin ke-{jackpot_ke} (backend tersembunyi)")

    for spin in range(1, total_spin_sim + 1):
        if modal < harga_per_spin:
            st.warning(f"💸 Modal habis di spin ke-{spin}")
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
            hadiah = prize_table.get(hasil_final[0], 0)

        if total_kembali + hadiah <= max_total_kembali:
            modal += hadiah
            total_kembali += hadiah
            total_menang += 1

    rtp_real = (total_kembali / (spin * harga_per_spin)) * 100 if spin > 0 else 0

    st.success(f"Simulasi selesai!")
    st.info(f"Total Spin: {spin}")
    st.info(f"Total Menang: {total_menang}")
    st.info(f"Total Kemenangan: {total_kembali} credit")
    st.info(f"Modal Akhir: {modal} credit")
    st.info(f"RTP Realisasi: {rtp_real:.2f}%")
    st.info(f"Jackpot besar keluar di spin ke-{jackpot_ke}")

