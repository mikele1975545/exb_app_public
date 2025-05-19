
import streamlit as st

st.set_page_config(page_title="Estrategia Exblifep Pro", layout="wide")

# Tabs para navegación
tab1, tab2 = st.tabs(["🧠 Estrategia hospital", "⚖️ Comparativa entre antibióticos"])

# ---------- TAB 1: Estrategia hospital ----------
with tab1:
    st.title("🧠 Estrategia para introducir Exblifep")
    st.markdown("Define la mejor estrategia cruzando datos locales con epidemiología regional.")

    ccaa_provincias = {
        "Andalucía": ["Almería", "Cádiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla"],
        "Aragón": ["Huesca", "Teruel", "Zaragoza"],
        "Asturias": ["Asturias"],
        "Baleares": ["Baleares"],
        "Canarias": ["Las Palmas", "Santa Cruz de Tenerife"],
        "Cantabria": ["Cantabria"],
        "Castilla-La Mancha": ["Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo"],
        "Castilla y León": ["Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora"],
        "Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"],
        "Ceuta": ["Ceuta"],
        "Extremadura": ["Badajoz", "Cáceres"],
        "Galicia": ["A Coruña", "Lugo", "Ourense", "Pontevedra"],
        "La Rioja": ["La Rioja"],
        "Madrid": ["Madrid"],
        "Melilla": ["Melilla"],
        "Murcia": ["Murcia"],
        "Navarra": ["Navarra"],
        "País Vasco": ["Álava", "Bizkaia", "Gipuzkoa"],
        "Valencia": ["Alicante", "Castellón", "Valencia"]
    }

    bacterias = [
        "Escherichia coli", "Klebsiella pneumoniae", "Pseudomonas aeruginosa",
        "Enterobacter cloacae", "Proteus mirabilis", "Acinetobacter baumannii"
    ]

    resistencias = [
        "BLEE", "AmpC", "OXA-48", "KPC", "NDM", "VIM", "IMP"
    ]

    porcentajes = ["<10%", "10-25%", "25-50%", "50-75%", ">75%"]

    hospital = st.text_input("Nombre del hospital")
    zona = st.selectbox("Comunidad Autónoma", list(ccaa_provincias.keys()))
    provincia = st.selectbox("Provincia", ccaa_provincias[zona])

    st.subheader("Bacterias más frecuentes")
    bacterias_selec = st.multiselect("Selecciona bacterias", bacterias)
    bacteria_porcs = {bac: st.selectbox(f"Prevalencia de {bac}", porcentajes, key="bacteria_" + bac) for bac in bacterias_selec}

    st.subheader("Resistencias más frecuentes")
    resistencias_selec = st.multiselect("Selecciona resistencias", resistencias)
    resistencia_porcs = {res: st.selectbox(f"Prevalencia de {res}", porcentajes, key="resistencia_" + res) for res in resistencias_selec}

    if st.button("Analizar estrategia"):
        st.markdown("### 📊 Análisis estratégico personalizado")
        st.write(f"**Hospital:** {hospital}")
        st.write(f"**Zona:** {zona} ({provincia})")
        st.markdown("**Bacterias seleccionadas:**")
        for b, p in bacteria_porcs.items():
            st.write(f"- {b}: {p}")
        st.markdown("**Resistencias seleccionadas:**")
        for r, p in resistencia_porcs.items():
            st.write(f"- {r}: {p}")

        st.markdown("---")
        st.markdown("### ✅ Estrategia recomendada")
        if "OXA-48" in resistencia_porcs:
            st.success("Exblifep es activo frente a OXA-48, incluso en BLEE+OXA-48.")
        if "BLEE" in resistencia_porcs:
            st.success("Exblifep permite ahorrar carbapenémicos frente a BLEE.")
        if "KPC" in resistencia_porcs or "NDM" in resistencia_porcs:
            st.warning("Exblifep no cubre bien KPC/NDM. Considerar otros si predominan.")
        if not resistencia_porcs:
            st.info("Considerar Exblifep como alternativa a CAZ/AVI o en fallos clínicos.")

        st.markdown("---")
        st.markdown("### 🔍 Análisis con EPINE (simulado)")
        st.markdown(f"En {provincia}, las tasas de resistencia a BLEE y OXA-48 son relevantes. Exblifep es adecuado en este contexto.")

        st.markdown("### 🧠 Argumentos para infecciosas")
        st.markdown("""
        - Alternativa eficaz a CAZ/AVI en OXA-48.
        - Permite reducir uso de meropenem (estrategia PROA).
        - Estudio ALLIUM respalda su eficacia clínica.
        - Alta penetración pulmonar.
        - Buena tolerabilidad.
        """)

# ---------- TAB 2: Comparativa entre antibióticos ----------
with tab2:
    st.title("⚖️ Comparativa entre antibióticos")

    abx_list = [
        "Cefepime/enmetazobactam", "Ceftazidima/avibactam", "Ceftolozano/tazobactam",
        "Meropenem/vaborbactam", "Imipenem/relebactam", "Aztreonam/avibactam",
        "Piperacilina/tazobactam", "Cefiderocol"
    ]

    col1, col2 = st.columns(2)
    with col1:
        abx1 = st.selectbox("Antibiótico 1", abx_list, index=0)
    with col2:
        abx2 = st.selectbox("Antibiótico 2", abx_list, index=1)

    if st.button("Comparar"):
        comparativas = {
            "BLEE": {
                "Cefepime/enmetazobactam": "✅",
                "Ceftazidima/avibactam": "✅",
                "Ceftolozano/tazobactam": "✅",
                "Meropenem/vaborbactam": "✅",
                "Imipenem/relebactam": "✅",
                "Aztreonam/avibactam": "✅",
                "Piperacilina/tazobactam": "⚠️ Limitado",
                "Cefiderocol": "✅"
            },
            "OXA-48": {
                "Cefepime/enmetazobactam": "✅",
                "Ceftazidima/avibactam": "⚠️ Parcial",
                "Ceftolozano/tazobactam": "❌",
                "Meropenem/vaborbactam": "❌",
                "Imipenem/relebactam": "❌",
                "Aztreonam/avibactam": "✅",
                "Piperacilina/tazobactam": "❌",
                "Cefiderocol": "✅"
            },
            "MBL": {
                "Cefepime/enmetazobactam": "❌",
                "Ceftazidima/avibactam": "❌",
                "Ceftolozano/tazobactam": "❌",
                "Meropenem/vaborbactam": "❌",
                "Imipenem/relebactam": "❌",
                "Aztreonam/avibactam": "✅",
                "Piperacilina/tazobactam": "❌",
                "Cefiderocol": "✅"
            }
        }

        st.markdown("### 🧪 Comparativa en tabla")
        st.table({
            "Característica": ["BLEE", "OXA-48", "MBL"],
            abx1: [comparativas["BLEE"][abx1], comparativas["OXA-48"][abx1], comparativas["MBL"][abx1]],
            abx2: [comparativas["BLEE"][abx2], comparativas["OXA-48"][abx2], comparativas["MBL"][abx2]]
        })

        st.markdown("### 📋 Análisis resumen")
        st.info(f"{abx1} y {abx2} ofrecen distintos perfiles. {abx1} destaca frente a {abx2} en ciertas enzimas dependiendo del espectro de betalactamasas.")

