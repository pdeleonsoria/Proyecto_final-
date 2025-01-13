import streamlit as st
import pickle
import pandas as pd

# Cargar los modelos y el escalador
aggressiveness_model_path = "/Users/pauladeleon/Desktop/modelos/rf_model.pkl"
days_left_model_path = "/Users/pauladeleon/Desktop/modelos/best_model2.pkl"
scaler_path = "/Users/pauladeleon/Desktop/modelos/minmax_scaler2.pkl"

with open(aggressiveness_model_path, "rb") as file:
    aggressiveness_model = pickle.load(file)

with open(days_left_model_path, "rb") as file:
    days_left_model = pickle.load(file)

with open(scaler_path, "rb") as file:
    scaler = pickle.load(file)

# Diccionarios para convertir valores categóricos
morphology_map = {
    'ADENOCARCINOMA': 0, 'CARCINOMA': 1, 'CARCINOMA ADENOESCAMOSO': 2,
    'CARCINOMA INDIFERENCIADO': 3, 'CARCINOMA NEUROENDOCRINO': 4,
    'CARCINOMA PSEUDOSARCOMATOSO': 5, 'CARCINOMA VERRUGOSO': 6,
    'CARCINOSARCOMA': 7, 'CARCINOMA DE CÉLULAS EN ANILLO': 8,
    'CÁNCER DE PIEL': 9, 'FIBROSARCOMA': 10, 'LEIOMIOSARCOMA': 11,
    'NEOPLASIA': 12, 'RABDOMIOSARCOMA': 13, 'SARCOMA': 14,
    'SARCOMA SECUNDARIO': 15, 'SEMINOMA': 16, 'TUMOR MALIGNO DE CÉLULAS GIGANTES': 17,
    'TUMOR MALIGNO DE CÉLULAS PEQUEÑAS': 18
}

race_map = {
    'ASIÁTICA': 0, 'CAUCÁSICA': 1, 'INDÍGENA': 2, 'MESTIZA': 3, 'NEGRA': 4
}

nationality_map = {
    'ANGOLA': 0, 'ARGENTINA': 1, 'BOLIVIA': 2, 'BRASIL': 3, 'CHILE': 4,
    'CHINA': 5, 'DINAMARCA': 6, 'ESPAÑA': 7, 'ESTADOS UNIDOS DE AMÉRICA': 8,
    'FRANJA DE GAZA (PALESTINA)': 9, 'FRANCIA': 10, 'GUATEMALA': 11,
    'HOLANDA': 12, 'ITALIA': 13, 'YUGOSLAVIA': 14, 'JAPÓN': 15, 'LÍBANO': 16,
    'PARAGUAY': 17, 'PERÚ': 18, 'POLONIA': 19, 'PORTUGAL': 20, 'REINO UNIDO': 21,
    'REP. FEDERAL DE ALEMANIA': 22, 'REP. ISLÁMICA DE IRÁN': 23,
    'REP. SOC. SOVIÉTICA DE UCRANIA': 24, 'SUIZA': 25, 'TURQUÍA': 26,
    'UNIÓN DE REP. SOC. SOVIÉTICAS': 27, 'URUGUAY': 28, 'VENEZUELA': 29
}

state_civil_map = {
    'CASADO': 0, 'SEPARADO JUDICIALMENTE': 1, 'SOLTERO': 2,
    'UNIÓN CONSENSUAL': 3, 'VIUDO': 4
}

diagnostic_means_map = {
    'CITOLOGÍA': 0, 'CLÍNICO': 1, 'HISTOLOGÍA DE LA METÁSTASIS': 2,
    'HISTOLOGÍA DEL TUMOR PRIMARIO': 3, 'MARCADORES TUMORALES': 4,
    'INVESTIGACIÓN': 5, 'SDO': 6
}

extension_map = {
    'IN SITU': 0, 'LOCALIZADO': 1, 'METÁSTASIS': 2
}

tnm_map = {
    '000': 0, '001': 1, '010': 2, '100': 3, '101': 4, '110': 5, '111': 6,
    '191': 7, '200': 8, '201': 9, '210': 10, '211': 11, '221': 12, '231': 13,
    '300': 14, '301': 15, '310': 16, '311': 17, '320': 18, '321': 19,
    '400': 20, '401': 21, '410': 22, '411': 23, '421': 24, '881': 25,
    '888': 26, '990': 27, '991': 28, '999': 29
}
# Título
st.title("🔬 Calculadora Cáncer de Próstata🔬")
st.markdown("""
Este formulario te permitirá predecir si el cáncer de próstata es agresivo basándose en datos recogidos en Brasil entre los años 2000 y 2019.
""")
# Primer formulario: Predicción de agresividad
st.header("¿Es tu cáncer agresivo?")
st.markdown("""
La agresividad de un cáncer esta estipulada según media de años de vida postdiagnóstico, siendo el cáncer de próstata uno de las neoplasias con mejor pronóstico, una media de vida postdiagnóstico menor de 5 años se supone agresivo
""")
with st.form(key='aggressiveness_form'):
    age = st.slider("Edad:", min_value=3, max_value=103, step=1)
    morphology = st.selectbox("Morfología:", list(morphology_map.keys()))
    race = st.selectbox("Raza:", list(race_map.keys()))
    nationality = st.selectbox("País de residencia:", list(nationality_map.keys()))
    state_civil = st.selectbox("Estado Civil:", list(state_civil_map.keys()))
    diagnostic_means = st.selectbox("Medio de Diagnóstico:", list(diagnostic_means_map.keys()))
    extension = st.selectbox("Extensión:", list(extension_map.keys()))
    tnm = st.selectbox("TNM:", list(tnm_map.keys()))

    submit_button_1 = st.form_submit_button("Predecir Agresividad")

if submit_button_1:
    # Escalar la edad
    age_scaled = scaler.transform([[age]])[0][0]

    # Convertir entradas categóricas a valores numéricos
    morphology_n = morphology_map[morphology]
    race_n = race_map[race]
    nationality_n = nationality_map[nationality]
    state_civil_n = state_civil_map[state_civil]
    diagnostic_means_n = diagnostic_means_map[diagnostic_means]
    extension_n = extension_map[extension]
    tnm_n = tnm_map[tnm]

    # Crear el DataFrame de entrada
    input_data = pd.DataFrame({
        'Age': [age_scaled],
        'Morphology_Description': [morphology_n],
        'Raca_Color': [race_n],
        'Nationality': [nationality_n],
        'State_Civil': [state_civil_n],
        'Diagnostic_means': [diagnostic_means_n],
        'Extension': [extension_n],
        'TNM': [tnm_n]
    })

    # Predecir
    prediction = aggressiveness_model.predict(input_data)

    # Mostrar el resultado
    if prediction[0] == 1:
        st.success("🔴 El cáncer es agresivo.")
    else:
        st.success("🟢 El cáncer NO es agresivo.")

# Segundo formulario: Predicción de días post diagnóstico
st.header("Entonces... ¿Cuántos días me quedan?")
with st.form(key='days_left_form'):
    age = st.number_input("Edad:", min_value=3, max_value=103, step=1, key='age_days')
    morphology = st.selectbox("Morfología:", list(morphology_map.keys()), key='morphology_days')
    race = st.selectbox("Raza:", list(race_map.keys()), key='race_days')
    nationality = st.selectbox("País de residencia:", list(nationality_map.keys()), key='nationality_days')
    state_civil = st.selectbox("Estado Civil:", list(state_civil_map.keys()), key='state_civil_days')
    diagnostic_means = st.selectbox("Medio de Diagnóstico:", list(diagnostic_means_map.keys()), key='diagnostic_means_days')
    extension = st.selectbox("Extensión:", list(extension_map.keys()), key='extension_days')
    tnm = st.selectbox("TNM:", list(tnm_map.keys()), key='tnm_days')
    # Pregunta simplificada: ¿Es agresivo?
    agresivo = st.radio("¿El cáncer es agresivo?", ["Sí", "No"], key='agresivo_days')

    # Mapear la respuesta a valores numéricos
    agresivo_n = 1 if agresivo == "Sí" else 0
    no_agresivo_n = 1 - agresivo_n  # Valor opuesto


    submit_button_2 = st.form_submit_button("Predecir días post diagnóstico")

if submit_button_2:
    
    # Escalar la edad
    age_scaled = scaler.transform([[age]])[0][0]

    # Convertir entradas categóricas a valores numéricos
    morphology_n = morphology_map[morphology]
    race_n = race_map[race]
    nationality_n = nationality_map[nationality]
    state_civil_n = state_civil_map[state_civil]
    diagnostic_means_n = diagnostic_means_map[diagnostic_means]
    extension_n = extension_map[extension]
    tnm_n = tnm_map[tnm]

    # Crear el DataFrame de entrada
    input_data = pd.DataFrame({
        'Age': [age_scaled],
        'Morphology_Description': [morphology_n],
        'Raca_Color': [race_n],
        'Nationality': [nationality_n],
        'State_Civil': [state_civil_n],
        'Diagnostic_means': [diagnostic_means_n],
        'Extension': [extension_n],
        'TNM': [tnm_n],
        'Agresivo': [agresivo_n],
        'No_Agresivo': [no_agresivo_n]
    })

    # Predecir los días post diagnóstico
    days_prediction = days_left_model.predict(input_data)
    st.success(f"Te quedan aproximadamente {int(days_prediction[0])} días post diagnóstico.")