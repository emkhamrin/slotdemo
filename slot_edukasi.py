# SIMULASI TANPA TULISAN DI ATASNYA
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
        balance_area.markdown(f"**Balance: {modal} credit**")
        rtp_real = (total_kembali / (spin * harga_per_spin)) * 100

        st.success(f"🎯 Jackpot besar muncul di spin ke-{jackpot_ke}")
        st.info(f"Total Menang: {total_menang} | Total Kembali: {total_kembali} credit | RTP Realisasi: {rtp_real:.2f}%")





