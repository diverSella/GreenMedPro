"""
GreenMed Pro - Calculadora Avanzada de Dosis de CBD
Versión: 2.0
Desarrollado por: Dr. Diver Sellanes & Qco. Rodrigo Lucero
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import math
import re

from productos import CatalogoProductos
from calculos import CalculadoraCBD, validar_dosis
from patologias import CatalogoPatologias, TipoIndicacion, TipoEvidencia
from referencias import CatalogoReferencias
from comparativa import tabla_equivalencias
from receta import generar_receta_html
from exportar_pdf import generar_pdf_bytes

# ============================================
# CONFIGURACIÓN
# ============================================
st.set_page_config(
    page_title="GreenMed Pro - Calculadora CBD",
    page_icon="🌿",
    layout="wide"
)

# ============================================
# ESTILOS CSS
# ============================================
st.markdown("""
<style>
    .main-header {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 10px 0;
        border-bottom: 2px solid #2E7D32;
        margin-bottom: 20px;
    }
    .main-header img {
        max-height: 60px;
    }
    .main-header h1 {
        color: #2E7D32;
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
        line-height: 60px;
    }
    .main-header .subtitle {
        color: #666;
        font-size: 1rem;
        margin: 0;
    }
    .main-header .version {
        color: #999;
        font-size: 0.8rem;
        margin: 0;
        font-style: italic;
    }
    .highlight-product {
        background-color: #e8f5e9;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4CAF50;
        margin-bottom: 20px;
        text-align: center;
    }
    .highlight-product .producto-nombre {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2E7D32;
        margin: 0;
    }
    .highlight-product .producto-dosis {
        font-size: 1.4rem;
        color: #333;
        margin: 10px 0 0 0;
    }
    .highlight-product .producto-detalle {
        font-size: 1rem;
        color: #666;
        margin: 5px 0 0 0;
    }
    .footer {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        padding-top: 20px;
        border-top: 1px solid #ddd;
        margin-top: 30px;
    }
    .footer .credits {
        font-size: 0.85rem;
        color: #555;
        margin-top: 5px;
    }
    .equivalencia-resaltada {
        background-color: #fff3e0;
        padding: 10px;
        border-radius: 5px;
        border-left: 5px solid #FF9800;
        margin-top: 10px;
    }
    .product-image-container {
        text-align: center;
        padding: 15px 10px 10px 10px;
        background: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 15px;
        max-width: 100%;
        border: 1px solid #e0e0e0;
    }
    .product-image-container img {
        max-width: 180px;
        max-height: 180px;
        object-fit: contain;
        border-radius: 5px;
        margin: 0 auto;
        display: block;
    }
    .product-image-container .product-name {
        font-size: 1.1rem;
        font-weight: bold;
        color: #2E7D32;
        margin: 8px 0 8px 0;
    }
    .product-image-container .product-detail {
        font-size: 0.85rem;
        color: #555;
        margin: 2px 0;
        padding: 4px 0;
        border-top: 1px solid #eee;
    }
    .product-image-container .product-detail strong {
        color: #333;
    }
    .product-image-container .product-detail .value {
        color: #2E7D32;
        font-weight: bold;
    }
    .section-subtitle {
        font-size: 1rem;
        font-weight: 600;
        color: #2E7D32;
        margin: 12px 0 8px 0;
    }
    .badge-prospecto {
        background-color: #2E7D32;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
    }
    .badge-evidencia {
        background-color: #FF9800;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
    }
    .evidencia-alta {
        color: #2E7D32;
        font-weight: bold;
    }
    .evidencia-moderada {
        color: #FF9800;
        font-weight: bold;
    }
    .evidencia-baja {
        color: #f44336;
        font-weight: bold;
    }
    .patologia-info {
        background-color: #f8f9fa;
        padding: 12px 15px;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-top: 8px;
        width: 100%;
    }
    .patologia-info .label {
        font-size: 0.8rem;
        color: #666;
    }
    .patologia-info .value {
        font-size: 1rem;
        font-weight: 500;
        color: #2E7D32;
    }
    .referencia-item {
        font-size: 0.85rem;
        padding: 4px 0;
        border-bottom: 1px solid #f0f0f0;
    }
    .referencia-item:last-child {
        border-bottom: none;
    }
    .recomendacion-box {
        background-color: #e3f2fd;
        padding: 12px 15px;
        border-radius: 8px;
        border-left: 4px solid #1976D2;
        margin: 10px 0;
    }
    .recomendacion-box .producto {
        font-weight: bold;
        color: #0D47A1;
        font-size: 1.1rem;
    }
    .recomendacion-box .tipo-producto {
        font-size: 0.85rem;
        color: #555;
        margin-top: 2px;
    }
    .estrellas {
        color: #FFD700;
        font-size: 1.2rem;
    }
    .info-prospecto {
        font-size: 0.85rem;
        color: #333;
        line-height: 1.6;
        margin: 4px 0;
    }
    .info-prospecto strong {
        color: #0D47A1;
    }
    .input-dosis-container {
        margin-top: 10px;
    }
    .input-dosis-container label {
        font-size: 0.9rem;
        color: #555;
    }
    .badge-recomendado {
        background-color: #1976D2;
        color: white;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: bold;
        display: inline-block;
        margin-top: 8px;
    }
    .dosis-input {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# LOGO Y CABECERA
# ============================================
col_logo, col_title = st.columns([1, 5])
with col_logo:
    logo_paths = [
        "assets/images/Logo empresa.JPG",
        "assets/images/logo-empresa.JPG",
        "assets/images/logo-greenmed.png"
    ]
    logo_cargado = False
    for path in logo_paths:
        if os.path.exists(path):
            st.image(path, width=70)
            logo_cargado = True
            break
    if not logo_cargado:
        st.markdown("🌿")

with col_title:
    st.markdown("""
    <div class="main-header">
        <div>
            <h1>GreenMed Pro</h1>
            <p class="subtitle">Calculadora Avanzada de Dosis de CBD</p>
            <p class="version">Basado en prospecto y evidencia científica</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# INICIALIZACIÓN
# ============================================
catalogo_productos = CatalogoProductos()
catalogo_patologias = CatalogoPatologias()
catalogo_referencias = CatalogoReferencias()

if 'dosis_personalizada' not in st.session_state:
    st.session_state.dosis_personalizada = 5.0
if 'observaciones' not in st.session_state:
    st.session_state.observaciones = ""
if 'receta_generada' not in st.session_state:
    st.session_state.receta_generada = False
if 'receta_html' not in st.session_state:
    st.session_state.receta_html = ""
if 'volumen_envase' not in st.session_state:
    st.session_state.volumen_envase = 30
if 'patologia_seleccionada' not in st.session_state:
    st.session_state.patologia_seleccionada = None
if 'producto_seleccionado' not in st.session_state:
    st.session_state.producto_seleccionado = None
if 'producto_recomendado' not in st.session_state:
    st.session_state.producto_recomendado = None
if 'dosis_recomendada' not in st.session_state:
    st.session_state.dosis_recomendada = None
if 'dosis_aplicada' not in st.session_state:
    st.session_state.dosis_aplicada = False
if 'selector_key' not in st.session_state:
    st.session_state.selector_key = 0

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.header("Datos del Paciente")
    
    paciente_nombre = st.text_input("Nombre del paciente", placeholder="Ej: Juan Pérez", key="nombre_paciente")
    
    col_peso, col_edad = st.columns(2)
    with col_peso:
        peso = st.number_input("Peso (kg)", min_value=0.5, max_value=300.0, value=70.0, step=0.5, key="peso_paciente")
    with col_edad:
        edad = st.number_input("Edad (años)", min_value=0, max_value=120, value=45, step=1, key="edad_paciente")
    
    with st.expander("Datos adicionales (opcional)"):
        diagnostico = st.text_input("Diagnóstico", placeholder="Ej: Epilepsia refractaria", key="diagnostico_input")
        alergias = st.text_input("Alergias", placeholder="Ej: Ninguna conocida", key="alergias_input")
        medicamentos = st.text_area("Medicamentos actuales", placeholder="Ej: Levetiracetam 1000 mg/día", height=68, key="medicamentos_input")
    
    st.divider()
    
    st.subheader("Selección de Patología")
    
    patologias_ordenadas = [
        "Síndrome de Lennox-Gastaut (SLG)",
        "Síndrome de Dravet (SD)",
        "Complejo de Esclerosis Tuberosa (CET)",
        "Dolor neuropático crónico"
    ]
    
    patologia_seleccionada = st.selectbox(
        "Seleccione la patología",
        patologias_ordenadas,
        help="Seleccione la patología para ver la dosis recomendada",
        key="selector_patologia"
    )
    
    if patologia_seleccionada:
        st.session_state.patologia_seleccionada = patologia_seleccionada
        patologia = catalogo_patologias.get_patologia(patologia_seleccionada)
        
        if patologia:
            st.session_state.producto_recomendado = patologia.producto_recomendado
            st.session_state.dosis_recomendada = patologia.dosis_inicial
            
            st.markdown('<div class="patologia-info">', unsafe_allow_html=True)
            
            if patologia.tipo == TipoIndicacion.ON_LABEL:
                st.markdown('<span class="badge-prospecto">Prospecto</span>', unsafe_allow_html=True)
            else:
                st.markdown('<span class="badge-evidencia">Evidencia</span>', unsafe_allow_html=True)
            
            evidencia_color = {
                TipoEvidencia.ALTA: "evidencia-alta",
                TipoEvidencia.MODERADA: "evidencia-moderada",
                TipoEvidencia.BAJA: "evidencia-baja",
                TipoEvidencia.PRELIMINAR: "evidencia-preliminar"
            }
            st.markdown(f"""
            <div style="margin-top: 6px;">
                <span class="label">Nivel de evidencia:</span>
                <span class="{evidencia_color.get(patologia.evidencia, '')}">{patologia.evidencia.value}</span>
                <span class="estrellas">{patologia.nivel_estrellas}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if patologia.referencias:
                st.markdown('<div style="margin-top: 4px;"><span class="label">Referencias:</span></div>', unsafe_allow_html=True)
                for ref_id in patologia.referencias:
                    ref = catalogo_referencias.get_referencia(ref_id)
                    if ref:
                        st.markdown(f"""
                        <div class="referencia-item">
                            <span style="font-size: 0.8rem;">{ref.autores} ({ref.año}). <em>{ref.titulo}</em></span>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Determinar el texto del tipo de producto
            if "Xatiplex" in patologia.producto_recomendado:
                tipo_texto = "en base a CBD purificado"
            else:
                tipo_texto = "en base a Extracto de Espectro Completo"
            
            st.markdown(f"""
            <div class="recomendacion-box">
                <div class="producto">Producto recomendado: {patologia.producto_recomendado}</div>
                <div class="tipo-producto">🔬 {tipo_texto}</div>
            """, unsafe_allow_html=True)
            
            if patologia.info_prospecto:
                for linea in patologia.info_prospecto:
                    st.markdown(f'<div class="info-prospecto">• {linea}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("Aplicar Producto/Dosis Recomendados", use_container_width=True, key="btn_aplicar_dosis"):
                st.session_state.dosis_personalizada = patologia.dosis_inicial
                st.session_state.producto_seleccionado = patologia.producto_recomendado
                st.session_state.dosis_aplicada = True
                st.session_state.selector_key += 1
                st.rerun()
    
    st.divider()
    
    # Selector de producto con título
    st.subheader("Selección del Producto")
    
    producto_lista = catalogo_productos.listar_productos()
    
    # Determinar el índice del producto seleccionado
    if st.session_state.producto_seleccionado and st.session_state.producto_seleccionado in producto_lista:
        default_index = producto_lista.index(st.session_state.producto_seleccionado)
    elif st.session_state.producto_recomendado and st.session_state.producto_recomendado in producto_lista:
        default_index = producto_lista.index(st.session_state.producto_recomendado)
    else:
        default_index = 0
    
    # Usar un key dinámico para forzar la actualización del selectbox
    producto_nombre = st.selectbox(
        "Seleccione el producto",
        producto_lista,
        index=default_index,
        key=f"selector_producto_{st.session_state.selector_key}"
    )
    
    st.session_state.producto_seleccionado = producto_nombre
    
    producto = catalogo_productos.get_producto(producto_nombre)
    
    if producto:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Concentración", f"{producto.concentracion}%")
        with col2:
            st.metric("Presentación", producto.presentacion)
        
        if producto.volumenes_disponibles:
            st.subheader("Volumen del envase")
            volumen_envase = st.radio(
                "Seleccione el volumen",
                producto.volumenes_disponibles,
                index=1 if 30 in producto.volumenes_disponibles else 0,
                horizontal=True,
                key="radio_volumen"
            )
            st.session_state.volumen_envase = volumen_envase
        
        st.info(f"**Descripción:** {producto.descripcion}")
    
    st.divider()
    
    st.subheader("Configuración")
    tomas_por_dia = st.selectbox(
        "Tomas por día",
        [1, 2, 3, 4],
        index=1,
        help="Número de administraciones diarias",
        key="select_tomas"
    )

# ============================================
# FUNCIÓN MOSTRAR IMAGEN
# ============================================
def mostrar_imagen_producto(producto_nombre, mg_por_ml, tiene_gotas, gotas_por_ml=None, mg_por_gota=None, volumen=None):
    imagen_map = {
        "Xpectra 10": "Xpectra_10.webp",
        "Xatiplex 5": "xatiplex_5.webp",
        "Xatiplex 10": "xatiplex_10.webp",
        "Xatiplex 15": "xatiplex_15.webp",
        "Xatiplex 20": "xatiplex_20.webp"
    }
    
    nombre_archivo = imagen_map.get(producto_nombre)
    
    st.markdown('<div class="product-image-container">', unsafe_allow_html=True)
    
    imagen_mostrada = False
    if nombre_archivo:
        ruta_imagen = f"assets/images/{nombre_archivo}"
        if os.path.exists(ruta_imagen):
            try:
                st.image(ruta_imagen, width=180)
                imagen_mostrada = True
            except:
                pass
    
    if not imagen_mostrada:
        emoji = '💊' if 'Xpectra' in producto_nombre else '💉'
        st.markdown(f'<div style="font-size: 2.5rem; padding: 10px 0;">{emoji}</div>', unsafe_allow_html=True)
    
    st.markdown(f'<div class="product-name">{producto_nombre}</div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="product-detail">
            <strong>CBD por ml:</strong> <span class="value">{mg_por_ml:.2f} mg</span>
        </div>
    """, unsafe_allow_html=True)
    
    if tiene_gotas:
        st.markdown(f"""
        <div class="product-detail">
            <strong>CBD por gota:</strong> <span class="value">{mg_por_gota:.3f} mg</span>
        </div>
        <div class="product-detail">
            <strong>Gotas por ml:</strong> <span class="value">{gotas_por_ml} gotas</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="product-detail">
            <span style="color: #666; font-size: 0.85rem;">Administración con jeringa</span>
        </div>
        <div class="product-detail">
            <span style="color: #666; font-size: 0.85rem;">No aplican gotas</span>
        </div>
        """, unsafe_allow_html=True)
    
    if volumen:
        st.markdown(f"""
        <div class="product-detail">
            <strong>Envase:</strong> <span class="value">{volumen} mL</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FUNCIÓN PARA REDONDEAR GOTAS
# ============================================
def redondear_gotas(gotas):
    """Redondea las gotas al número entero más cercano"""
    return round(gotas)

# ============================================
# TABS
# ============================================
tab1, tab2, tab3 = st.tabs(["Calculadora", "Equivalencias", "Receta"])

# ============================================
# TAB 1 - CALCULADORA
# ============================================
with tab1:
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.header("Selección de Dosis")
        
        dosis_recomendada = st.session_state.dosis_recomendada
        dosis_actual = st.session_state.dosis_personalizada
        
        # Badge de dosis recomendada aplicada
        if st.session_state.dosis_aplicada and dosis_recomendada:
            st.markdown(f'<div class="badge-recomendado">⭐ Dosis recomendada aplicada: {dosis_recomendada:.2f} mg/kg/día</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-dosis-container">', unsafe_allow_html=True)
        st.markdown("**Ingrese la dosis (mg/kg/día):**")
        dosis_por_kg = st.number_input(
            "Dosis (mg/kg/día)",
            min_value=0.01,
            max_value=30.0,
            value=st.session_state.dosis_personalizada,
            step=0.01,
            key="input_dosis_personalizada",
            label_visibility="collapsed",
            format="%.2f"
        )
        if dosis_por_kg != st.session_state.dosis_personalizada:
            st.session_state.dosis_personalizada = float(dosis_por_kg)
            st.session_state.dosis_aplicada = False
        st.markdown('</div>', unsafe_allow_html=True)
        
        if patologia_seleccionada:
            pat = catalogo_patologias.get_patologia(patologia_seleccionada)
            if pat:
                st.markdown("---")
                st.markdown(f"""
                <div style="background: #f0f7ff; padding: 12px 15px; border-radius: 8px; border-left: 4px solid #2196F3;">
                    <div style="font-weight: bold; font-size: 0.9rem;">{patologia_seleccionada}</div>
                    <div style="font-size: 0.85rem; color: #555; margin-top: 4px;">
                        {pat.descripcion}
                    </div>
                    <div style="font-size: 0.8rem; color: #666; margin-top: 4px;">
                        <strong>Evidencia:</strong> {pat.evidencia.value} {pat.nivel_estrellas}
                    </div>
                    <div style="font-size: 0.8rem; color: #666; margin-top: 2px;">
                        <strong>Producto recomendado:</strong> {pat.producto_recomendado}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with col2:
        st.header("Producto seleccionado")
        
        if producto:
            calculadora = CalculadoraCBD(producto)
            mg_por_ml = calculadora.mg_por_ml
            tiene_gotas = calculadora.mg_por_gota is not None
            mg_por_gota = calculadora.mg_por_gota if tiene_gotas else None
            gotas_por_ml = producto.gotas_por_ml if tiene_gotas else None
            
            mostrar_imagen_producto(
                producto_nombre, 
                mg_por_ml, 
                tiene_gotas,
                gotas_por_ml,
                mg_por_gota,
                st.session_state.volumen_envase
            )
    
    if peso > 0 and producto:
        st.divider()
        
        # Validar dosis según la patología
        dosis_min = 0.01  # Default
        dosis_max = 30.0
        if patologia_seleccionada:
            pat = catalogo_patologias.get_patologia(patologia_seleccionada)
            if pat:
                dosis_min = pat.dosis_min
                dosis_max = pat.dosis_max
        
        es_valido, mensaje_validacion = validar_dosis(dosis_por_kg, peso, dosis_min, dosis_max)
        
        if not es_valido:
            st.error(f"⚠️ {mensaje_validacion}")
        else:
            st.success(f"✅ {mensaje_validacion}")
        
        calculadora = CalculadoraCBD(producto)
        pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
        
        st.header("Pauta de Administración")
        
        tiene_gotas = "dosis_por_toma_gotas" in pauta
        
        # Redondear gotas al entero más cercano
        if tiene_gotas:
            gotas_redondeadas = redondear_gotas(pauta['dosis_por_toma_gotas'])
            mensaje_dosis = f"{gotas_redondeadas} gotas"
        else:
            mensaje_dosis = f"{pauta['dosis_por_toma_ml']:.1f} ml"
        
        if tomas_por_dia == 1:
            frecuencia = "una vez al día"
        elif tomas_por_dia == 2:
            frecuencia = "dos veces al día (cada 12 horas)"
        elif tomas_por_dia == 3:
            frecuencia = "tres veces al día (cada 8 horas)"
        else:
            frecuencia = f"{tomas_por_dia} veces al día"
        
        badge_html = ""
        if patologia_seleccionada:
            pat = catalogo_patologias.get_patologia(patologia_seleccionada)
            if pat:
                if pat.tipo == TipoIndicacion.ON_LABEL:
                    badge_html = '<span class="badge-prospecto">Prospecto</span>'
                else:
                    badge_html = '<span class="badge-evidencia">Evidencia</span>'
                badge_html += f' <span style="font-size: 0.8rem; color: #666;">{patologia_seleccionada}</span>'
        
        if st.session_state.dosis_aplicada:
            badge_html += ' <span style="background-color: #1976D2; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: bold;">Dosis recomendada aplicada</span>'
        
        st.markdown(f"""
        <div class="highlight-product">
            <p class="producto-nombre">{pauta['producto']} ({pauta['concentracion']}%)</p>
            <p class="producto-dosis">{mensaje_dosis} {frecuencia}</p>
            <p class="producto-detalle">Presentación: {pauta['presentacion']} | Envase: {st.session_state.volumen_envase} mL</p>
            <p class="producto-detalle" style="margin-top: 8px;">{badge_html}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-subtitle">Detalles de la Dosis</p>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Dosis por kg/día</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{pauta['dosis_por_kg']:.2f} mg/kg/día</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Dosis total diaria</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{pauta['dosis_diaria_mg']:.1f} mg/día</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Nro de tomas</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{tomas_por_dia} veces/día</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Dosis por toma</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{pauta['dosis_por_toma_mg']:.2f} mg/toma</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<p class="section-subtitle">Detalles de Administración</p>', unsafe_allow_html=True)
        
        volumen_envase = st.session_state.volumen_envase
        ml_por_toma = pauta['dosis_por_toma_ml']
        dosis_por_envase = math.floor(volumen_envase / ml_por_toma) if ml_por_toma > 0 else 0
        ml_por_toma_str = f"{ml_por_toma:.2f}".replace('.', ',')
        gotas_por_toma = pauta['dosis_por_toma_gotas'] if tiene_gotas else None
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Volumen por toma</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{ml_por_toma_str} mL/toma</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if tiene_gotas:
                gotas_redondeadas = redondear_gotas(gotas_por_toma)
                st.markdown(f"""
                <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                    <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Gotas por toma</div>
                    <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{gotas_redondeadas} gotas/toma</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                    <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Volumen por toma</div>
                    <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{ml_por_toma_str} mL/toma</div>
                </div>
                """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Tomas por día</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{tomas_por_dia} veces/día</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div style="text-align: center; padding: 8px 4px; background: #f8f9fa; border-radius: 6px; border: 1px solid #e9ecef;">
                <div style="font-size: 0.8rem; color: #666; margin-bottom: 2px;">Dosis por envase</div>
                <div style="font-size: 1.1rem; font-weight: 500; color: #2E7D32;">{dosis_por_envase} dosis/envase</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        st.subheader("Equivalencias para esta dosis")
        st.markdown("Si el paciente no puede comprar el producto seleccionado, estas son las dosis equivalentes con otros productos:")
        
        mg_por_toma = pauta['dosis_por_toma_mg']
        productos_equivalencias = {}
        
        for prod_name in catalogo_productos.listar_productos():
            prod = catalogo_productos.get_producto(prod_name)
            calc = CalculadoraCBD(prod)
            if prod_name == "Xpectra 10":
                gotas = calc.convertir_a_gotas(mg_por_toma)
                productos_equivalencias[prod_name] = f"{gotas:.1f} gotas" if gotas else f"{calc.convertir_a_ml(mg_por_toma):.3f} ml"
            else:
                productos_equivalencias[prod_name] = f"{calc.convertir_a_ml(mg_por_toma):.3f} ml"
        
        df_equivalencias = pd.DataFrame({
            "Producto": list(productos_equivalencias.keys()),
            "Cantidad por toma": list(productos_equivalencias.values())
        })
        
        st.dataframe(
            df_equivalencias,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Producto": st.column_config.TextColumn("Producto", width="medium"),
                "Cantidad por toma": st.column_config.TextColumn("Cantidad por toma", width="medium")
            }
        )
        
        producto_seleccionado = pauta['producto']
        cantidad_seleccionada = productos_equivalencias[producto_seleccionado]
        st.markdown(f"""
        <div class="equivalencia-resaltada">
            <strong>Producto seleccionado:</strong> {producto_seleccionado} 
            <span style="color: #FF9800;">→</span> 
            <strong>{cantidad_seleccionada}</strong>
        </div>
        """, unsafe_allow_html=True)

# ============================================
# TAB 2 - EQUIVALENCIAS
# ============================================
with tab2:
    st.header("Tabla de Equivalencias")
    st.markdown("""
    Esta tabla muestra la correspondencia entre **gotas de Xpectra 10** y **ml de Xatiplex**.
    Útil para convertir rápidamente entre productos.
    """)
    
    df_equivalencias_completa, gotas = tabla_equivalencias()
    
    st.dataframe(
        df_equivalencias_completa,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Xpectra 10": st.column_config.TextColumn(
                "Xpectra 10 (10%)",
                help="Gotas de Xpectra 10 (32 gotas/ml)"
            ),
            "Xatiplex 5": st.column_config.TextColumn(
                "Xatiplex 5",
                help="ml de Xatiplex 5%"
            ),
            "Xatiplex 10": st.column_config.TextColumn(
                "Xatiplex 10",
                help="ml de Xatiplex 10%"
            ),
            "Xatiplex 15": st.column_config.TextColumn(
                "Xatiplex 15",
                help="ml de Xatiplex 15%"
            ),
            "Xatiplex 20": st.column_config.TextColumn(
                "Xatiplex 20",
                help="ml de Xatiplex 20%"
            )
        }
    )
    
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Xpectra 10 (Gotero)**
        - 32 gotas = 1 ml
        - Extracto de Espectro Completo
        - Administración con gotero
        """)
    
    with col2:
        st.markdown("""
        **Xatiplex (Jeringa)**
        - Administración con jeringa
        - CBD purificado
        - Mayor precisión en la dosis
        """)

# ============================================
# TAB 3 - RECETA MÉDICA
# ============================================
with tab3:
    st.header("Receta Médica")
    st.markdown("""
    Complete los datos del paciente y la dosis en la pestaña **Calculadora**,
    luego agregue sus observaciones y genere la receta.
    """)
    
    if peso > 0 and producto:
        calculadora = CalculadoraCBD(producto)
        pauta = calculadora.calcular_pauta_completa(peso, dosis_por_kg)
        pauta['paciente_nombre'] = paciente_nombre if paciente_nombre else "No especificado"
        pauta['edad'] = edad
        pauta['volumen_envase'] = st.session_state.volumen_envase
        pauta['patologia'] = patologia_seleccionada if patologia_seleccionada else "No especificada"
        
        st.subheader("Observaciones")
        observaciones = st.text_area(
            "Escriba aquí sus observaciones, indicaciones adicionales o advertencias:",
            value=st.session_state.observaciones,
            height=100,
            placeholder="Ej: Iniciar con dosis baja. Evaluar respuesta en 2 semanas.",
            key="observaciones_input"
        )
        st.session_state.observaciones = observaciones
        
        if st.button("Generar Receta", type="primary", key="btn_generar_receta"):
            with st.spinner("Generando receta..."):
                receta_html = generar_receta_html(pauta, observaciones)
                st.session_state.receta_html = receta_html
                st.session_state.receta_generada = True
        
        if st.session_state.get('receta_generada', False):
            st.divider()
            st.subheader("Receta Generada")
            
            st.components.v1.html(
                st.session_state.receta_html,
                height=600,
                scrolling=True
            )
            
            st.divider()
            st.subheader("Exportar")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nombre_limpio = paciente_nombre.replace(' ', '_') if paciente_nombre else "paciente"
                fecha_actual = datetime.now().strftime('%Y%m%d')
                nombre_archivo_html = f"receta_{nombre_limpio}_{fecha_actual}.html"
                
                st.download_button(
                    label="📄 Descargar HTML",
                    data=st.session_state.receta_html,
                    file_name=nombre_archivo_html,
                    mime="text/html",
                    use_container_width=True,
                    key="btn_descargar_html"
                )
            
            with col2:
                try:
                    pdf_bytes = generar_pdf_bytes(st.session_state.receta_html)
                    nombre_archivo_pdf = f"receta_{nombre_limpio}_{fecha_actual}.pdf"
                    
                    st.download_button(
                        label="📥 Descargar PDF",
                        data=pdf_bytes,
                        file_name=nombre_archivo_pdf,
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary",
                        key="btn_descargar_pdf"
                    )
                except Exception as e:
                    st.error(f"Error al generar PDF: {e}")
                    st.info("💡 Asegúrate de tener instalado weasyprint")
    else:
        st.warning("⚠️ Primero complete los datos del paciente y seleccione un producto.")

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>Esta herramienta es de apoyo para profesionales de la salud.</p>
    <p>La decisión final de prescripción es responsabilidad del médico tratante.</p>
    <p>GreenMed Pro | Basado en prospecto y evidencia científica</p>
    <div class="credits">
        <strong>Desarrollado por:</strong> Dr. Diver Sellanes &amp; Qco. Rodrigo Lucero
    </div>
</div>
""", unsafe_allow_html=True)
