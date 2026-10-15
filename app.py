import datetime
import streamlit as st

st.set_page_config(
    page_title="Nukleáris Medicina - Effektív Dózis", page_icon="☢️"
)

st.title("Nukleáris Medicina - Effektív Dózis Teljes Testre")
st.markdown(
    "Beteg-specifikus dózisbecslés ICRP szabványok (Publ. 80, 106, 128) alapján."
)

# Adatbázisok szervspecifikus együtthatókkal (mSv/MBq)
pet_dict = {
    "C-11 metionin": {
        "c": 0.0055,
        "s": "ICRP Publ. 128 (Amino acid)",
        "org": {
            "Agy": 0.0080,
            "Máj": 0.0065,
            "Hasnyálmirigy": 0.0070,
            "Húgyhólyag fal": 0.0040,
        },
    },
    "F-18 FDG": {
        "c": 0.0190,
        "s": "ICRP Publ. 106 / 128 (Glucose)",
        "org": {
            "Agy": 0.0250,
            "Szívfal": 0.0450,
            "Húgyhólyag fal": 0.1100,
            "Vesék": 0.0150,
        },
    },
    "Ga-68 DOTATATE / PSMA": {
        "c": 0.0230,
        "s": "ICRP Publ. 128 (Gallium peptide)",
        "org": {
            "Vesék": 0.0850,
            "Lép": 0.0900,
            "Máj": 0.0350,
            "Húgyhólyag fal": 0.1200,
        },
    },
}

spect_dict = {
    "BrainSPECT (HMPAO/ECD)": {
        "c": 0.0075,
        "s": "ICRP Publ. 80 / 128 (Brain)",
        "org": {"Agy": 0.0220, "Vesék": 0.0080, "Húgyhólyag fal": 0.0500},
    },
    "Bromida": {
        "c": 0.0060,
        "s": "ICRP Publ. 128 (Generic)",
        "org": {"Gyomor": 0.0070, "Húgyhólyag fal": 0.0400},
    },
    "DMSA": {
        "c": 0.0053,
        "s": "ICRP Publ. 80 / 128 (Renal)",
        "org": {"Vesék": 0.1500, "Húgyhólyag fal": 0.0350},
    },
    "DTPA": {
        "c": 0.0060,
        "s": "ICRP Publ. 80 / 106 / 128",
        "org": {"Vesék": 0.0250, "Húgyhólyag fal": 0.0900},
    },
    "EC": {
        "c": 0.0065,
        "s": "ICRP Publ. 128 (Renal function)",
        "org": {"Vesék": 0.0300, "Húgyhólyag fal": 0.0850},
    },
    "Fyton": {
        "c": 0.0035,
        "s": "ICRP Publ. 80 / 128 (Reticuloend.)",
        "org": {"Máj": 0.0150, "Lép": 0.0200},
    },
    "HIDA": {
        "c": 0.0030,
        "s": "ICRP Publ. 80 / 128 (Hepatobiliary)",
        "org": {"Epehólyag fal": 0.0450, "Máj": 0.0080},
    },
    "I-123 DaTscan": {
        "c": 0.0220,
        "s": "ICRP Publ. 128 (Dopamine)",
        "org": {"Pajzsmirigy": 0.0150, "Húgyhólyag fal": 0.1800},
    },
    "I-123 MIBG": {
        "c": 0.0130,
        "s": "ICRP Publ. 128 (Adrenergic)",
        "org": {"Mellékvese": 0.0400, "Húgyhólyag fal": 0.0950},
    },
    "I-131 diagnosztikus": {
        "c": 0.2200,
        "s": "ICRP Publ. 80 / 128 (Thyroid)",
        "org": {
            "Pajzsmirigy": 3.5000,
            "Gyomor fal": 0.0500,
            "Húgyhólyag fal": 0.2500,
        },
    },
    "I-131 MIBG": {
        "c": 0.0350,
        "s": "ICRP Publ. 128 (Theranostic)",
        "org": {"Mellékvese": 0.1200, "Húgyhólyag fal": 0.3000},
    },
    "Lu-177 Dotatate": {
        "c": 0.0550,
        "s": "ICRP Publ. 128 (PRRT)",
        "org": {"Vesék": 0.2500, "Lép": 0.3000, "Máj": 0.0800},
    },
    "Lu-177 Pluvicto": {
        "c": 0.0480,
        "s": "ICRP / Literature (PSMA)",
        "org": {"Nyálmirigyek": 0.1500, "Vesék": 0.2000, "Lép": 0.1200},
    },
    "MAG3": {
        "c": 0.0070,
        "s": "ICRP Publ. 80 / 128 (Clearance)",
        "org": {"Vesék": 0.0400, "Húgyhólyag fal": 0.0950},
    },
    "Makroalbumon (MAA)": {
        "c": 0.0110,
        "s": "ICRP Publ. 80 / 128 (Lung)",
        "org": {"Tüdő": 0.3500, "Máj": 0.0050},
    },
    "MDP (Skeleton)": {
        "c": 0.0057,
        "s": "ICRP Publ. 80 / 128 (Bone)",
        "org": {
            "Csontfelszínek": 0.5300,
            "Húgyhólyag fal": 0.1300,
            "Vörös csontvelő": 0.0550,
            "Vesék": 0.0160,
        },
    },
    "MIBI (Sestamibi)": {
        "c": 0.0090,
        "s": "ICRP Publ. 80 / 128 (Myocardial)",
        "org": {"Szívfal": 0.0350, "Epehólyag fal": 0.0400, "Vesék": 0.0200},
    },
    "NanoScan": {
        "c": 0.0052,
        "s": "ICRP Publ. 128 (Lymph)",
        "org": {"Nyirokcsomók": 0.0500, "Máj": 0.0100},
    },
    "Pyron": {
        "c": 0.0050,
        "s": "ICRP Publ. 80 / 128 (Cardiac)",
        "org": {"Szívfal": 0.0300, "Máj": 0.0080},
    },
    "Senti scint": {
        "c": 0.0052,
        "s": "ICRP Publ. 80 / 128 (Sentinel)",
        "org": {"Nyirokcsomók": 0.0450},
    },
    "Tco4 (Pertechnetát)": {
        "c": 0.0130,
        "s": "ICRP Publ. 80 / 106 / 128",
        "org": {
            "Pajzsmirigy": 0.1000,
            "Gyomor fal": 0.0450,
            "Húgyhólyag fal": 0.0800,
        },
    },
    "Tektrotyd": {
        "c": 0.0160,
        "s": "ICRP Publ. 80 / 128 (Somatostatin)",
        "org": {"Vesék": 0.0600, "Lép": 0.0800, "Máj": 0.0250},
    },
}

st.subheader("Vizsgálati mód kiválasztása")
modality = st.radio("Modalitás:", ["SPECT / Theranostic", "PET"], horizontal=True)

current_dict = pet_dict if modality == "PET" else spect_dict

with st.form("dose_form"):
    st.subheader("Vizsgálati adatok megadása")
    taj = st.text_input("Beteg TAJ száma (opcionális a mentéshez):")

    pharmaceutical = st.selectbox(
        "Radiofarmakon:", sorted(current_dict.keys())
    )

    activity = st.number_input(
        "Beadott aktivitás (MBq):", min_value=0.1, value=740.0, step=10.0
    )

    submitted = st.form_submit_button("Effektív Dózis Számítása")

if submitted:
    if activity <= 0:
        st.error("Kérjük, adj meg érvényes, pozitív aktivitást!")
    else:
        item = current_dict[pharmaceutical]
        dose = activity * item["c"]

        taj_trimmed = taj.strip()
        taj_display = taj_trimmed if taj_trimmed else "Nincs megadva"

        # Szervdózisok számítása mSv-ben
        org_text = ""
        org_csv_str = ""
        if "org" in item:
            org_lines = []
            org_csv_parts = []
            for organ, coeff in item["org"].items():
                org_dose = activity * coeff
                org_lines.append(f"- **{organ}**: {org_dose:.2f} mSv")
                org_csv_parts.append(f"{organ}:{org_dose:.2f}mSv")
            org_text = "\n".join(org_lines)
            org_csv_str = " | ".join(org_csv_parts)

        st.success(f"### Effektív dózis teljes testre: {dose:.2f} mSv")

        org_display_block = (
            f"\n\n**Főbb szervdózisok:**\n{org_text}" if org_text else ""
        )

        st.info(
            f"**Számítás részletei:**\n\n"
            f"- **TAJ:** {taj_display}\n"
            f"- **Modalitás:** {modality}\n"
            f"- **Farmakon:** {pharmaceutical}\n"
            f"- **Beadott aktivitás:** {activity:.1f} MBq\n"
            f"- **Szabvány / Forrás:** {item['s']}\n"
            f"- **Alkalmazott együttható:** {item['c']} mSv/MBq"
            f"{org_display_block}"
        )

        # Mentési opció csak akkor jelenik meg, ha van megadott TAJ szám
        if taj_trimmed:
            taj_clean = "".join(
                c for c in taj_trimmed if c.isalnum() or c in ("-", "_")
            )
            if not taj_clean:
                taj_clean = "Ismeretlen"

            filename = f"taj_{taj_clean}_dozis_naplo.csv"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            csv_header = "Datum;TAJ;Modalitas;Farmakon;Beadott_Aktivitas_MBq;Effektiv_Dozis_mSv;ICRP_Egyutthato;Szabvany_Forras;Szervdozisok_mSv\n"
            csv_row = f"{timestamp};{taj_trimmed};{modality};{pharmaceutical};{str(activity).replace('.', ',')};{str(round(dose, 2)).replace('.', ',')};{str(item['c']).replace('.', ',')};{item['s']};{org_csv_str}\n"
            csv_data = csv_header + csv_row

            st.markdown("---")
            st.subheader("Fájl mentése")
            st.download_button(
                label="📥 CSV Fájl Letöltése / Mentése másként",
                data=csv_data.encode("utf-8-sig"),
                file_name=filename,
                mime="text/csv",
            )
        else:
            st.warning(
                "💡 *Megjegyzés: Mivel nem adtál meg TAJ számot, a mentési opció nem jelenik meg, de a számítást sikeresen elvégeztük.*"
            )
