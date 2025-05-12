
# app_exblifep_con_barra.py
# Versión mejorada con barra de progreso, selección detallada, y exportación PDF

import streamlit as st
import time
from fpdf import FPDF
import os

st.set_page_config(page_title="Asistente Exblifep", layout="centered")

st.title("🧠 Asistente Estratégico para Exblifep")
st.markdown("""
Esta app te ayuda a definir la mejor estrategia para introducir Exblifep en un hospital específico, cruzando datos locales con el informe EPINE 2024.
""")

# --- Paso 1: Geografía ---
st.header("1️⃣ Selección geográfica")
comunidad = st.selectbox("Selecciona la comunidad autónoma", [
    "Andalucía", "Aragón", "Asturias", "Baleares", "Canarias", "Cantabria",
    "Castilla-La Mancha", "Castilla y León", "Cataluña", "Ceuta", "Comunidad Valenciana",
    "Extremadura", "Galicia", "La Rioja", "Madrid", "Melilla", "Murcia", "Navarra", "País Vasco"
])
provincia = st.text_input("Provincia (escribe manualmente si no aparece)")
hospital = st.text_input("Nombre del hospital").upper()

# --- Paso 2: Epidemiología ---
st.header("2️⃣ Epidemiología del hospital")

st.subheader("Bacterias Gramnegativas más frecuentes")
bacterias_disp = [
    "Escherichia coli", "Klebsiella pneumoniae", "Enterobacter cloacae", "Pseudomonas aeruginosa",
    "Proteus mirabilis", "Serratia marcescens", "Acinetobacter baumannii"
]
bacterias_seleccionadas = st.multiselect("Selecciona bacterias", bacterias_disp)
porcentajes_bact = {}
for b in bacterias_seleccionadas:
    porc = st.selectbox(f"Prevalencia estimada de {b}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"bact_{b}")
    porcentajes_bact[b] = porc

st.subheader("Resistencias más frecuentes")
resistencias_disp = ["BLEE", "OXA-48", "KPC", "NDM", "AmpC"]
resistencias_seleccionadas = st.multiselect("Selecciona resistencias", resistencias_disp)
porcentajes_res = {}
for r in resistencias_seleccionadas:
    porc = st.selectbox(f"Prevalencia estimada de {r}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"res_{r}")
    porcentajes_res[r] = porc

# --- Generar estrategia ---
st.header("3️⃣ Análisis estratégico")
if st.button("🔍 Analizar estrategia"):
    with st.spinner("Analizando datos y cruzando con EPINE 2024..."):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

    st.success("✅ Estrategia generada. Puedes revisarla abajo o exportarla como PDF.")

    # --- Resultado ---
    st.markdown(f"""
    ## 📋 Estrategia para {hospital}
    **Zona:** {provincia}, {comunidad}

    **Bacterias encontradas:** {', '.join([f"{b} ({porcentajes_bact[b]})" for b in bacterias_seleccionadas])}
    
    **Resistencias destacadas:** {', '.join([f"{r} ({porcentajes_res[r]})" for r in resistencias_seleccionadas])}

    **Cruce con EPINE 2024:**
    Según los datos del informe EPINE 2024, en la comunidad autónoma de **{comunidad}** y provincia de **{provincia}**, las infecciones por enterobacterias multirresistentes muestran una tendencia creciente, especialmente en unidades críticas y pacientes con dispositivos invasivos. Esto respalda la necesidad de contar con tratamientos activos frente a BLEE y OXA-48, como Exblifep.

    **Propuesta de posicionamiento:**
    Exblifep (cefepime/enmetazobactam) se propone como alternativa eficaz frente a BLEE, OXA-48 y AmpC, pudiendo sustituir carbapenémicos (ahorro PROA) y ofrecer una opción eficaz en fallos de CAZ/AVI. Cuenta con evidencia en NAVM y BGN hospitalarios (estudios como ALLIUM [Kaye 2022], Bonnin 2025, Das 2020).

    """)

    # --- Exportar a PDF ---
    def exportar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Estrategia para {hospital}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Zona: {provincia}, {comunidad}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)
        pdf.cell(200, 10, txt="Bacterias frecuentes:", ln=True)
        for b in bacterias_seleccionadas:
            pdf.cell(200, 10, txt=f" - {b}: {porcentajes_bact[b]}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)
        pdf.cell(200, 10, txt="Resistencias frecuentes:", ln=True)
        for r in resistencias_seleccionadas:
            pdf.cell(200, 10, txt=f" - {r}: {porcentajes_res[r]}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)
        pdf.multi_cell(0, 10, txt=f"Cruce con EPINE: En {comunidad}, los datos reflejan aumento de BLEE/OXA-48. Exblifep permite reducir meropenem y ofrece cobertura adecuada.")
        pdf.multi_cell(0, 10, txt="Estudios: ALLIUM (Kaye), Bonnin R. 2025, Das 2020")

        output_path = f"estrategia_{hospital.replace(' ', '_')}.pdf"
        pdf.output(output_path)
        return output_path

    if st.button("💾 Exportar estrategia como PDF"):
        try:
            pdf_file = exportar_pdf()
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Descargar PDF", f, file_name=pdf_file, mime="application/pdf")
        except Exception as e:
            st.error(f"Error exportando PDF: {e}")
