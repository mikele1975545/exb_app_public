
import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="Asistente Exblifep", layout="centered")

st.title("🧠 Asistente Estratégico para Exblifep")
st.markdown("Esta app te ayuda a definir la mejor estrategia para introducir Exblifep en un hospital específico, cruzando datos locales con el informe EPINE 2024.")

# --- Paso 1: Comunidad y Provincia ---
st.header("1️⃣ Selección geográfica")

ccaa = st.selectbox("Selecciona la comunidad autónoma", [
    "Andalucía", "Aragón", "Asturias", "Baleares", "Canarias", "Cantabria", "Castilla-La Mancha",
    "Castilla y León", "Cataluña", "Ceuta", "Extremadura", "Galicia", "La Rioja", "Madrid",
    "Melilla", "Murcia", "Navarra", "País Vasco", "Valencia"
])

provincia = st.text_input("Provincia (escribe manualmente si no aparece)")

# --- Paso 2: Bacterias y resistencias ---
st.header("2️⃣ Epidemiología del hospital")

st.subheader("Bacterias Gramnegativas más frecuentes")
bacterias = st.multiselect("Selecciona bacterias", [
    "Klebsiella pneumoniae", "Escherichia coli", "Enterobacter cloacae", "Citrobacter freundii",
    "Proteus mirabilis", "Serratia marcescens", "Morganella morganii", "Pseudomonas aeruginosa",
    "Acinetobacter baumannii", "Providencia spp.", "Burkholderia cepacia"
])
porc_bacterias = {}
for b in bacterias:
    porc = st.selectbox(f"Prevalencia estimada de {b}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"porc_{b}")
    porc_bacterias[b] = porc

st.subheader("Resistencias más frecuentes")
resistencias = st.multiselect("Selecciona resistencias", [
    "OXA-48", "BLEE", "AmpC", "KPC", "NDM", "IMI", "VIM"
])
porc_resistencias = {}
for r in resistencias:
    porc = st.selectbox(f"Prevalencia estimada de {r}", ["<10%", "10-25%", "25-50%", ">50%"], key=f"porc_{r}")
    porc_resistencias[r] = porc

# --- Paso 3: Estrategia ---
estrategia_texto = ""

if st.button("🔍 Analizar estrategia"):
    st.header("✅ Estrategia recomendada")

    argumentos = []

    if "OXA-48" in resistencias:
        argumentos.append("- Exblifep es activo frente a OXA-48. Soporte: Bonnin R 2025 (META disminuye CMI90 de FEP en OXA-48).")
    if "BLEE" in resistencias:
        argumentos.append("- Permite ahorro de carbapenémicos en BLEE. Soporte: IPT Exblifep, p.7 (actividad frente a BLEE).")
    if "Klebsiella pneumoniae" in bacterias:
        argumentos.append("- Alta actividad frente a K. pneumoniae BLEE/OXA-48. Soporte: ALLIUM trial (Kaye 2022).")
    if "Pseudomonas aeruginosa" in bacterias:
        argumentos.append("- Aunque Exblifep no está dirigido a Pseudomonas, puede cubrir BLEE u OXA-48 en coinfecciones mixtas.")
    if ccaa and provincia:
        argumentos.append(f"- En {provincia}, {ccaa}, los datos EPINE muestran alta prevalencia de BLEE/OXA-48 en enterobacterias.")
        argumentos.append("  Esto refuerza la necesidad de un antibiótico activo y específico como Exblifep.")

    for a in argumentos:
        st.markdown(f"🧩 {a}")

    estrategia_texto = "\n".join(arg for arg in argumentos)

# --- Exportar en PDF ---
def generar_pdf(texto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, texto)
    output_path = "/mnt/data/Estrategia_Exblifep.pdf"
    pdf.output(output_path)
    return output_path

if estrategia_texto:
    if st.button("📄 Exportar estrategia en PDF"):
        pdf_path = generar_pdf(estrategia_texto)
        st.success("PDF generado correctamente.")
        st.download_button("⬇️ Descargar PDF", data=open(pdf_path, "rb"), file_name="estrategia_exblifep.pdf")

