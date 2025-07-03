import streamlit as st
import random
import time

st.set_page_config(page_title="🎰 Slot Edukasi Anti Judi", layout="centered")

symbols = ['🍒', '💎', '7️⃣', '🍋', '🔔']
weights_awal = [0.4, 0.3, 0.15, 0.1, 0.05]
weights_sulit = [0.5, 0.3, 0.15, 0.049, 0.001]

# Setting dasar
target_rtp = st.slider("Target RTP (%)", 50, 99, 96)
modal_awal = st.number_input("Modal Awal", 100, 100_000, 3000, 100)
harga_per_spin = st.number_input("Harga per Spin", 10, 10_000, 100, 10)

prize_table = {
    '🍒': 5 * harga_per_spin,
    '💎': 10 * harga_per_spin,
    '7️⃣': 50 * harga_per_spin,
    '🍋': 15 * harga_per_spin,
    '🔔': 5000 * harga_per_spin
}

# Inisialisasi State
if "modal" not in st.session_state:
    st.session_state.modal = 3000
if "grid_display" not in st.session_state:
    st.session_state.grid_display = random.choices(symbols, weights_awal, k=3)
if "jackpot_terjadi" not in st.session_state:
    st.session_state.jackpot_terjadi = False
if "total_kembali" not in st.session_state:
    st.session_state.total_kembali = 0
if "counter_spin" not in st.session_state:
    st.session_state.counter_spin = 0
if "total_biaya" not in st.session_state:
    st.session_state.total_biaya = 0
if "jackpot_min_biaya" not in st.session_state:
    jackpot_payout = prize_table['🔔']
    total_bet_minimal = int(jackpot_payout / (target_rtp / 100))
    st.session_state.jackpot_min_biaya = total_bet_minimal

st.title("🎰 Slot Edukasi Anti Judi 💸")

if st.button("Reset Modal & Setup"):
    st.session_state.modal = modal_awal
    st.session_state.total_kembali = 0
    st.session_state.jackpot_terjadi = False
    st.session_state.counter_spin = 0
    st.session_state.grid_display = random.choices(symbols, weights_awal, k=3)
    st.session_state.total_biaya = 0
    jackpot_payout = prize_table['🔔']
    total_bet_minimal = int(jackpot_payout / (target_rtp / 100))
    st.session_state.jackpot_min_biaya = total_bet_minimal

# Area Tampilan
grid_area = st.empty()
balance_area = st.empty()
notif_area = st.empty()

def tampilkan_grid(hasil, warna="white"):
    grid_html = "<div style='display:grid;grid-template-columns:repeat(3,80px);gap:5px;'>"
    for s in hasil:
        grid_html += f"<div style='border:2px solid gold;padding:10px;text-align:center;font-size:30px;color:{warna};'>{s}</div>"
    grid_html += "</div>"
    grid_area.markdown(grid_html, unsafe_allow_html=True)

tampilkan_grid(st.session_state.grid_display)
balance_area.markdown(f"**Balance: {st.session_state.modal} credit**")

# Spin Sekali
if st.button("Spin Sekali"):
    if st.session_state.modal < harga_per_spin:
        notif_area.error("Modal tidak cukup")
    else:
        st.session_state.modal -= harga_per_spin
        st.session_state.counter_spin += 1
        st.session_state.total_biaya += harga_per_spin

        weights = weights_sulit if st.session_state.jackpot_terjadi else weights_awal
        hasil = random.choices(symbols, weights, k=3)
        hadiah = 0

        if st.session_state.total_biaya >= st.session_state.jackpot_min_biaya and not st.session_state.jackpot_terjadi:
            hasil = ['🔔', '🔔', '🔔']
            hadiah = prize_table['🔔']
            st.session_state.jackpot_terjadi = True
            jackpot_payout = prize_table['🔔']
            st.session_state.jackpot_min_biaya += int(jackpot_payout / (target_rtp / 100))
        elif hasil[0] == hasil[1] == hasil[2]:
            hadiah = prize_table.get(hasil[0], 0)

        st.session_state.modal += hadiah
        st.session_state.total_kembali += hadiah
        st.session_state.grid_display = hasil

        tampilkan_grid(hasil, "gold" if hadiah > 0 else "white")
        balance_area.markdown(f"**Balance: {st.session_state.modal} credit**")

        if hadiah > 0:
            notif_area.success(f"🎉 Menang {hadiah} credit!")
        else:
            notif_area.empty()

# Auto Spin
total_spin_auto = st.number_input("Jumlah Auto Spin", 1, 500, 50, 1)
if st.button("Start Auto Spin"):
    for _ in range(total_spin_auto):
        if st.session_state.modal < harga_per_spin:
            notif_area.warning("Modal habis, Auto Spin berhenti.")
            break

        st.session_state.modal -= harga_per_spin
        st.session_state.counter_spin += 1
        st.session_state.total_biaya += harga_per_spin

        weights = weights_sulit if st.session_state.jackpot_terjadi else weights_awal
        hasil = random.choices(symbols, weights, k=3)
        hadiah = 0

        if st.session_state.total_biaya >= st.session_state.jackpot_min_biaya and not st.session_state.jackpot_terjadi:
            hasil = ['🔔', '🔔', '🔔']
            hadiah = prize_table['🔔']
            st.session_state.jackpot_terjadi = True
            jackpot_payout = prize_table['🔔']
            st.session_state.jackpot_min_biaya += int(jackpot_payout / (target_rtp / 100))
        elif hasil[0] == hasil[1] == hasil[2]:
            hadiah = prize_table.get(hasil[0], 0)

        st.session_state.modal += hadiah
        st.session_state.total_kembali += hadiah
        st.session_state.grid_display = hasil

        tampilkan_grid(hasil, "gold" if hadiah > 0 else "white")
        balance_area.markdown(f"**Balance: {st.session_state.modal} credit**")

        if hadiah > 0:
            notif_area.success(f"🎉 Menang {hadiah} credit!")
        else:
            notif_area.empty()

        time.sleep(0.1)

# Simulasi Tanpa Animasi
total_simulasi = st.number_input("Jumlah Spin Simulasi", 10, 100_000, 1000, 100)
if st.button("Mulai Simulasi"):

    modal = st.session_state.modal
    total_kembali = 0
    jackpot_terjadi = st.session_state.jackpot_terjadi
    total_menang = 0

    # TOTAL BIAYA harus mengacu ke total biaya AKUMULASI global
    total_biaya = st.session_state.total_biaya
    target_jackpot_min_biaya = st.session_state.jackpot_min_biaya

    for spin in range(1, total_simulasi + 1):
        if modal < harga_per_spin:
            st.warning(f"Modal habis di spin ke-{spin}")
            break

        modal -= harga_per_spin
        total_biaya += harga_per_spin

        weights = weights_sulit if jackpot_terjadi else weights_awal
        hasil = random.choices(symbols, weights, k=3)
        hadiah = 0

        if total_biaya >= target_jackpot_min_biaya and not jackpot_terjadi:
            hasil = ['🔔', '🔔', '🔔']
            hadiah = prize_table['🔔']
            jackpot_terjadi = True

            # Tambahkan ambang batas jackpot selanjutnya
            st.session_state.jackpot_min_biaya += prize_table['🔔']

        elif hasil[0] == hasil[1] == hasil[2]:
            hadiah = prize_table.get(hasil[0], 0)

        modal += hadiah
        total_kembali += hadiah
        total_menang += 1 if hadiah > 0 else 0

    # Update ke session state global
    st.session_state.modal = modal
    st.session_state.total_kembali += total_kembali
    st.session_state.total_biaya = total_biaya
    st.session_state.jackpot_terjadi = jackpot_terjadi

    balance_area.markdown(f"**Balance: {modal} credit**")
    rtp_real = (total_kembali / (spin * harga_per_spin)) * 100 if spin > 0 else 0

    st.info(f"Total Menang: {total_menang} | Total Kembali: {total_kembali} credit | RTP Realisasi: {rtp_real:.2f}%")






