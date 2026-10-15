import datetime
import os
import streamlit as st

st.set_page_config(
    page_title="Nukleáris Medicina - Effektív Dózis", page_icon="☢️"
)

st.title("Nukleáris Medicina - Effektív Dózis Teljes Testre")
st.markdown(
    "Beteg-specifikus dózisbecslés ICRP szabványok (Publ. 80, 106, 128) alapján."
)

# Adatbázisok
pet_dict = {
    "C-11 metionin": {"c": 0.0055, "s": "ICRP Publ. 128 (Amino acid)"},
    "F-18 FDG": {"c": 0.0190, "s": "ICRP Publ. 106 / 128 (Glucose)"},
    "Ga-68 DOTATATE / PSMA": {
        "c": 0.0230,
        "s": "ICRP Publ. 128 (Gallium peptide)",
    },
}

spect_dict = {
    "BrainSPECT (HMPAO/ECD)": {"c": 0.0075, "s": "ICRP Publ. 80 / 128 (Brain)"},
    "Bromida": {"c": 0.0060, "s": "ICRP Publ. 128 (Generic)"},
    "DMSA": {"c": 0.0053, "s": "ICRP Publ. 80 / 128 (Renal)"},
    "DTPA": {"c": 0.0060, "s": "ICRP Publ. 80 / 106 / 128"},
    "EC": {"c": 0.0065, "s": "ICRP Publ. 128 (Renal function)"},
    "Fyton": {"c": 0.0035, "s": "ICRP Publ. 80 / 128 (Reticuloend.)"},
    "HIDA": {"c": 0.0030, "s": "ICRP Publ. 80 / 128 (Hepatobiliary)"},
    "I-123 DaTscan": {"c": 0.0220, "s": "ICRP Publ. 128 (Dopamine)"},
    "I-123 MIBG": {"c": 0.0130, "s": "ICRP Publ. 128 (Adrenergic)"},
    "I-131 diagnosztikus": {"c": 0.2200, "s": "ICRP Publ. 80 / 128 (Thyroid)"},
    "I-131 MIBG": {"c": 0.0350, "s": "ICRP Publ. 128 (Theranostic)"},
    "Lu-177 Dotatate": {"c": 0.0550, "s": "ICRP Publ. 128 (PRRT)"},
    "Lu-177 Pluvicto": {"c": 0.0480, "s": "ICRP / Literature (PSMA)"},
    "MAG3": {"c": 0.0070, "s": "ICRP Publ. 80 / 128 (Clearance)"},
    "Makroalbumon (MAA)": {"c": 0.0110, "s": "ICRP Publ. 80 / 128 (Lung)"},
    "MDP (Skeleton)": {"c": 0.0057, "s": "ICRP Publ. 80 / 128 (Bone)"},
    "MIBI (Sestamibi)": {"c": 0.0090, "s": "ICRP Publ. 80 / 128 (Myocardial)"},
    "NanoScan": {"c": 0.0052, "s": "ICRP Publ. 128 (Lymph)"},
    "Pyron": {"c": 0.0050, "s": "ICRP Publ. 80 / 128 (Cardiac)"},
    "Senti scint": {"c": 0.0052, "s": "ICRP Publ. 80 / 128 (Sentinel)"},
    "Tco4 (Pertechnetát)": {"c": 0.0130, "s": "ICRP Publ. 80 / 106 / 128"},
    "Tektrotyd": {"c": 0.0160, "s": "ICRP Publ. 80 / 128 (Somatostatin)"},
}

st.subheader("Vizsgálati mód kiválasztása")
modality = st.radio("Modalitás:", ["SPECT / Theranostic", "PET"], horizontal=True)

current_dict = pet_dict if modality == "PET" else spect_dict

with st.form("dose_form"):
    st.subheader("Vizsgálati adatok megadása")
    taj = st.text_input("Beteg TAJ száma:")

    pharmaceutical = st.selectbox(
        "Radiofarmakon:", sorted(current_dict.keys())
    )

    activity = st.number_input(
        "Beadott aktivitás (MBq):", min_value=0.1, value=740.0, step=10.0
    )

    submitted = st.form_submit_button("Effektív Dózis Számítása és Mentése")

if submitted:
    if activity <= 0:
        st.error("Kérjük, adj meg érvényes, pozitív aktivitást!")
    else:
        item = current_dict[pharmaceutical]
        dose = activity * item["c"]

        st.success(f"### Effektív dózis teljes testre: {dose:.2f} mSv")

        st.info(
            f"**Számítás részletei:**\n\n"
            f"- **TAJ:** {taj if taj else 'Nincs megadva'}\n"
            f"- **Modalitás:** {modality}\n"
            f"- **Farmakon:** {pharmaceutical}\n"
            f"- **Beadott aktivitás:** {activity:.1f} MBq\n"
            f"- **Szabvány / Forrás:** {item['s']}\n"
            f"- **Alkalmazott együttható:** {item['c']} mSv/MBq"
        )

        taj_clean = (
            "".join(c for c in taj if c.isalnum() or c in ("-", "_"))
            if taj
            else "Ismeretlen"
        )
        if not taj_clean:
            taj_clean = "Ismeretlen"

        # Letöltések mappa útvonalának automatikus meghatározása Windows / Linux / macOS rendszereken
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(downloads_path):
            downloads_path = os.path.expanduser(
                "~"
            )  # Biztonsági fallback a home mappára

        filename = os.path.join(downloads_path, f"taj_{taj_clean}_dozis_naplo.csv")
        file_exists = os.path.exists(filename)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            with open(filename, mode="a", encoding="utf-8", newline="") as f:
                if not file_exists:
                    f.write(
                        "Datum;TAJ;Modalitas;Farmakon;Beadott_Aktivitas_MBq;Effektiv_Dozis_mSv;ICRP_Egyutthato;Szabvany_Forras\n"
                    )
                f.write(
                    f"{timestamp};{taj if taj else 'Ismeretlen'};{modality};{pharmaceutical};"
                    f"{str(activity).replace('.', ',')};{str(round(dose, 2)).replace('.', ',')};"
                    f"{str(item['c']).replace('.', ',')};{item['s']}\n"
                )
            st.success(
                f"Sikeresen rögzítve a Letöltések mappába:\n`{filename}`"
            )
        except Exception as e:
            st.error(f"Nem sikerült menteni a fájlt: {e}")
