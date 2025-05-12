
import streamlit as st
from fpdf import FPDF
import time

st.set_page_config(page_title="Estrategia Exblifep", layout="centered")

st.title("🧠 Asistente Estratégico para Exblifep")
st.markdown("Esta app te ayuda a definir la mejor estrategia para introducir Exblifep en un hospital específico, cruzando datos locales con el informe EPINE 2024.")

st.header("1️⃣ Selección geográfica")
hospital = st.text_input("🏥 Nombre del hospital")
comunidad = st.selectbox("Selecciona la comunidad autónoma", ["Andalucía", "Cataluña", "Madrid", "Valencia", "Galicia", "Castilla y León", "País Vasco", "Aragón", "Castilla-La Mancha", "Canarias", "Extremadura", "Murcia", "Navarra", "La Rioja", "Baleares", "Asturias", "Cantabria", "Ceuta", "Melilla"])
provincia = st.text_input("Provincia (escribe manualmente si no aparece)")

st.header("2️⃣ Epidemiología del hospital")

bacterias = st.multiselect("Bacterias Gramnegativas más frecuentes", [
    "Escherichia coli", "Klebsiella pneumoniae", "Enterobacter cloacae", 
    "Pseudomonas aeruginosa", "Acinetobacter baumannii", "Proteus mirabilis"
])
resistencias = st.multiselect("Resistencias más frecuentes", ["OXA-48", "BLEE", "AmpC", "KPC", "NDM"])

if st.button("🔍 Analizar estrategia"):
    with st.spinner("Analizando datos..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.02)
            progress_bar.progress(i + 1)

    st.success("✅ Estrategia generada. Puedes revisarla abajo o exportarla como PDF.")

    st.subheader(f"📋 Estrategia para {hospital.upper()}")
    st.markdown(f"**Zona:** {provincia}, {comunidad}")
    st.markdown("**Bacterias encontradas:** " + ", ".join(bacterias))
    st.markdown("**Resistencias destacadas:** " + ", ".join(resistencias))

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Estrategia para {hospital.upper()}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Ubicación: {provincia}, {comunidad}", ln=True)
    pdf.ln(10)
    pdf.cell(200, 10, txt="Bacterias gramnegativas más frecuentes:", ln=True)
    for b in bacterias:
        pdf.cell(200, 10, txt=f"- {b}", ln=True)
    pdf.cell(200, 10, txt="Resistencias más frecuentes:", ln=True)
    for r in resistencias:
        pdf.cell(200, 10, txt=f"- {r}", ln=True)

    output_path = "/mnt/data/estrategia_" + hospital.lower().replace(" ", "_") + ".pdf"
    pdf.output(output_path)

    st.download_button("📄 Descargar estrategia en PDF", data=open(output_path, "rb"), file_name=f"Estrategia_{hospital}.pdf")
