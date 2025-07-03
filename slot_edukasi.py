import streamlit as st
import random
import time

st.set_page_config(page_title="🎰 Chinese Luck Slot Edukasi", layout="centered")

symbols = ['🍒', '💎', '7️⃣', '🍋', '🔔']
weights_awal = [0.4, 0.3, 0.15, 0.1, 0.05]
weights_sulit = [0.5, 0.3, 0.15, 0.049, 0.001]

if "modal" not in st.session_state:
    st.session_state.modal = 3000
if "grid_display" not in st.session_state:
    st.session_state.grid_display = random.choices(symbols, weights_awal, k=3)
if "jackpot_spin" not in st.session_state:
    st.session_state.jackpot_spin = random.randint(1, 100_000)
if "jackpot_terjadi" not in st.session_state:
    st.session_state.jackpot_terjadi = False
if "total_kembali" not in st.session_state:
    st.session_state.total_kembali = 0
if "counter_spin" not in st.session_state:
    st.session_state.counter_spin = 0

modal_awal = st.number_input("Modal Awal", 100, 100_000, 3000, 100)
harga_per_spin = st.number_input("Harga per Spin", 10, 10_000, 100, 10)
target_rtp = st.slider("Target RTP (%)", 50, 99, 96)

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
    st.session_state.jackpot_spin = random.randint(1, 100_000)
    st.session_state.jackpot_terjadi = False
    st.session_state.counter_spin = 0

def tampilkan_grid(hasil, warna="white"):
    grid_html = "<div style='display:grid;grid-template-columns:repeat(3,80px);gap:5px;'>"
    for s in hasil:
        grid_html += f"<div style='border:2px solid gold;padding:10px;text-align:center;font-size:30px;color:{warna};'>{s}</div>"
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)

st.markdown(f"**Balance: {st.session_state.modal} credit**")
tampilkan_grid(st.session_state.grid_display)

if st.button("Spin Sekali"):
    if st.session_state.modal < harga_per_spin:
        st.error("Modal tidak cukup")
    else:
        st.session_state.modal -= harga_per_spin
        st.session_state.counter_spin += 1

        weights = weights_sulit if st.session_state.jackpot_terjadi else weights_awal
        hasil = random.choices(symbols, weights, k=3)
        hadiah = 0

        if st.session_state.counter_spin == st.session_state.jackpot_spin:
            hasil = ['🔔', '🔔', '🔔']
            hadiah = prize_table['🔔']
            st.session_state.jackpot_terjadi = True
        elif hasil[0] == hasil[1] == hasil[2]:
            hadiah = prize_table.get(hasil[0], 0)

        if st.session_state.total_kembali + hadiah <= (harga_per_spin * target_rtp * 0.01 * st.session_state.counter_spin):
            st.session_state.modal += hadiah
            st.session_state.total_kembali += hadiah

        tampilkan_grid(hasil, "gold" if hadiah > 0 else "white")
        st.markdown(f"**Balance: {st.session_state.modal} credit**")
        if hadiah > 0:
            st.success(f"🎉 Menang {hadiah} credit!")

with st.expander("Auto Spin (Atur Jumlah Spin)"):
    total_spin_auto = st.number_input("Jumlah Spin", 1, 500, 50, 1)
    if st.button("Start Auto Spin"):
        for _ in range(total_spin_auto):
            if st.session_state.modal < harga_per_spin:
                st.warning("Modal habis, Auto Spin berhenti.")
                break

            st.session_state.modal -= harga_per_spin
            st.session_state.counter_spin += 1

            weights = weights_sulit if st.session_state.jackpot_terjadi else weights_awal
            hasil = random.choices(symbols, weights, k=3)
            hadiah = 0

            if st.session_state.counter_spin == st.session_state.jackpot_spin:
                hasil = ['🔔', '🔔', '🔔']
                hadiah = prize_table['🔔']
                st.session_state.jackpot_terjadi = True
            elif hasil[0] == hasil[1] == hasil[2]:
                hadiah = prize_table.get(hasil[0], 0)

            if st.session_state.total_kembali + hadiah <= (harga_per_spin * target_rtp * 0.01 * st.session_state.counter_spin):
                st.session_state.modal += hadiah
                st.session_state.total_kembali += hadiah

            tampilkan_grid(hasil, "gold" if hadiah > 0 else "white")
            st.markdown(f"**Balance: {st.session_state.modal} credit**")

            time.sleep(0.1)

with st.expander("Simulasi Tanpa Animasi"):
    total_simulasi = st.number_input("Jumlah Spin Simulasi", 10, 100_000, 1000, 100)
    if st.button("Mulai Simulasi"):

        modal = st.session_state.modal
        total_kembali = 0
        jackpot_ke = random.randint(1, total_simulasi)
        jackpot_terjadi = False
        total_menang = 0

        for spin in range(1, total_simulasi + 1):
            if modal < harga_per_spin:
                st.warning(f"Modal habis di spin ke-{spin}")
                break

            modal -= harga_per_spin

            weights = weights_sulit if jackpot_terjadi else weights_awal
            hasil = random.choices(symbols, weights, k=3)
            hadiah = 0

            if spin == jackpot_ke:
                hasil = ['🔔', '🔔', '🔔']
                hadiah = prize_table['🔔']
                jackpot_terjadi = True
            elif hasil[0] == hasil[1] == hasil[2]:
                hadiah = prize_table.get(hasil[0], 0)

            if total_kembali + hadiah <= (harga_per_spin * total_simulasi * target_rtp * 0.01):
                modal += hadiah
                total_kembali += hadiah
                total_menang += 1

        st.session_state.modal = modal
        st.markdown(f"**Balance: {modal} credit**")
        rtp_real = (total_kembali / (spin * harga_per_spin)) * 100
        st.info(f"Total Menang: {total_menang} | Total Kembali: {total_kembali} credit | RTP Realisasi: {rtp_real:.2f}%")
        st.info(f"Jackpot besar muncul di spin ke-{jackpot_ke}")







