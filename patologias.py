"""
Base de datos de patologías para GreenMed Pro
On-Label: según prospecto de Xpectra/Xatiplex
Off-Label: según evidencia científica
Todas las dosis expresadas en mg/kg/día
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class TipoEvidencia(Enum):
    ALTA = "Alta"
    MODERADA = "Moderada"
    BAJA = "Baja"
    PRELIMINAR = "Preliminar"

class TipoIndicacion(Enum):
    ON_LABEL = "On-Label (prospecto)"
    OFF_LABEL = "Off-Label (evidencia científica)"

@dataclass
class Patologia:
    nombre: str
    tipo: TipoIndicacion
    dosis_min: float
    dosis_max: float
    dosis_inicial: float
    dosis_mantenimiento: float
    evidencia: TipoEvidencia
    descripcion: str
    referencias: List[str]
    resumen: str = ""
    producto_recomendado: str = ""
    tipo_producto: str = ""
    dosis_inicial_texto: str = ""
    dosis_max_texto: str = ""
    comentarios: str = ""
    bibliografia: str = ""
    nivel_estrellas: str = ""
    info_prospecto: List[str] = None
    dosis_opciones: List[float] = None
    peso_referencia: float = 70.0
    prospectos: List[Dict] = None  # Lista de prospectos descargables

class CatalogoPatologias:
    
    def __init__(self):
        self.patologias: Dict[str, Patologia] = {
            # ============================================
            # ON-LABEL - Epilepsia (según prospecto)
            # ============================================
            "Síndrome de Lennox-Gastaut (SLG)": Patologia(
                nombre="Síndrome de Lennox-Gastaut (SLG)",
                tipo=TipoIndicacion.ON_LABEL,
                dosis_min=5.0,
                dosis_max=20.0,
                dosis_inicial=5.0,
                dosis_mantenimiento=10.0,
                evidencia=TipoEvidencia.ALTA,
                descripcion="Síndrome de Lennox-Gastaut. Epilepsia refractaria con múltiples tipos de crisis.",
                referencias=["GW2018", "GW2020"],
                resumen="El CBD ha demostrado reducir significativamente la frecuencia de crisis en pacientes con SLG.",
                producto_recomendado="Xatiplex 10",
                tipo_producto="CBD purificado",
                dosis_inicial_texto="5.0 mg/kg/día",
                dosis_max_texto="20.0 mg/kg/día",
                comentarios="Titulación semanal: incrementos de 2.5 mg/kg dos veces al día.",
                bibliografia="Devinsky O, et al. NEJM 2018; Devinsky O, et al. Epilepsia 2020.",
                nivel_estrellas="⭐⭐⭐",
                dosis_opciones=[2.5, 5.0, 10.0, 15.0, 20.0],
                info_prospecto=[
                    "Dosis inicial: 5.0 mg/kg/día",
                    "Titulación: Incrementos semanales de 2.5 mg/kg/día",
                    "Dosis máxima: 20.0 mg/kg/día",
                    "Evidencia: Alta - Múltiples ensayos clínicos"
                ],
                prospectos=[
                    {"nombre": "Xpectra 10 - Prospecto", "archivo": "Xpectra-10_Prospecto_V.02.pdf", "descripcion": "Extracto de Cannabis Sativa L - Solución oral gotas (10%)"},
                    {"nombre": "Xatiplex - Prospecto", "archivo": "Xatiplex_Prospecto.pdf", "descripcion": "CBD purificado - Solución oral jeringa"}
                ]
            ),
            "Síndrome de Dravet (SD)": Patologia(
                nombre="Síndrome de Dravet (SD)",
                tipo=TipoIndicacion.ON_LABEL,
                dosis_min=5.0,
                dosis_max=20.0,
                dosis_inicial=5.0,
                dosis_mantenimiento=10.0,
                evidencia=TipoEvidencia.ALTA,
                descripcion="Síndrome de Dravet. Epilepsia refractaria con crisis febriles prolongadas.",
                referencias=["GW2018", "GW2020"],
                resumen="El CBD ha demostrado reducir significativamente la frecuencia de crisis en pacientes con SD.",
                producto_recomendado="Xatiplex 10",
                tipo_producto="CBD purificado",
                dosis_inicial_texto="5.0 mg/kg/día",
                dosis_max_texto="20.0 mg/kg/día",
                comentarios="Titulación semanal: incrementos de 2.5 mg/kg dos veces al día.",
                bibliografia="Devinsky O, et al. NEJM 2018.",
                nivel_estrellas="⭐⭐⭐",
                dosis_opciones=[2.5, 5.0, 10.0, 15.0, 20.0],
                info_prospecto=[
                    "Dosis inicial: 5.0 mg/kg/día",
                    "Titulación: Incrementos semanales de 2.5 mg/kg/día",
                    "Dosis máxima: 20.0 mg/kg/día",
                    "Evidencia: Alta - Múltiples ensayos clínicos"
                ],
                prospectos=[
                    {"nombre": "Xpectra 10 - Prospecto", "archivo": "Xpectra-10_Prospecto_V.02.pdf", "descripcion": "Extracto de Cannabis Sativa L - Solución oral gotas (10%)"},
                    {"nombre": "Xatiplex - Prospecto", "archivo": "Xatiplex_Prospecto.pdf", "descripcion": "CBD purificado - Solución oral jeringa"}
                ]
            ),
            "Complejo de Esclerosis Tuberosa (CET)": Patologia(
                nombre="Complejo de Esclerosis Tuberosa (CET)",
                tipo=TipoIndicacion.ON_LABEL,
                dosis_min=5.0,
                dosis_max=25.0,
                dosis_inicial=5.0,
                dosis_mantenimiento=10.0,
                evidencia=TipoEvidencia.ALTA,
                descripcion="Complejo de Esclerosis Tuberosa. Epilepsia refractaria asociada a esclerosis tuberosa.",
                referencias=["GW2020"],
                resumen="El CBD ha demostrado reducir significativamente la frecuencia de crisis en pacientes con CET.",
                producto_recomendado="Xatiplex 10",
                tipo_producto="CBD purificado",
                dosis_inicial_texto="5.0 mg/kg/día",
                dosis_max_texto="25.0 mg/kg/día",
                comentarios="Dosis de mantenimiento: 5 mg/kg dos veces al día (10 mg/kg/día).",
                bibliografia="Devinsky O, et al. Epilepsia 2020.",
                nivel_estrellas="⭐⭐⭐",
                dosis_opciones=[2.5, 5.0, 10.0, 15.0, 20.0, 25.0],
                info_prospecto=[
                    "Dosis inicial: 5.0 mg/kg/día",
                    "Titulación: Incrementos semanales según tolerancia",
                    "Dosis máxima: 25.0 mg/kg/día",
                    "Evidencia: Alta - Ensayos clínicos"
                ],
                prospectos=[
                    {"nombre": "Xpectra 10 - Prospecto", "archivo": "Xpectra-10_Prospecto_V.02.pdf", "descripcion": "Extracto de Cannabis Sativa L - Solución oral gotas (10%)"},
                    {"nombre": "Xatiplex - Prospecto", "archivo": "Xatiplex_Prospecto.pdf", "descripcion": "CBD purificado - Solución oral jeringa"}
                ]
            ),
            
            # ============================================
            # OFF-LABEL - Dolor neuropático
            # ============================================
            "Dolor neuropático crónico": Patologia(
                nombre="Dolor neuropático crónico",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=0.10,
                dosis_max=2.8,
                dosis_inicial=0.14,
                dosis_mantenimiento=0.57,
                evidencia=TipoEvidencia.MODERADA,
                descripcion="Dolor de origen neuropático.",
                referencias=["TGA2022", "Hauser2024", "Busse2021", "Serpell2021"],
                resumen="La evidencia clínica favorece formulaciones con THC + CBD como tratamiento adyuvante del dolor neuropático. El CBD aislado no ha demostrado una eficacia consistente frente a placebo.",
                producto_recomendado="Xpectra 10",
                tipo_producto="Extracto de Espectro Completo",
                dosis_inicial_texto="0.14 mg/kg/día",
                dosis_max_texto="2.8 mg/kg/día",
                comentarios="El CBD aislado no ha demostrado eficacia consistente para dolor neuropático. Se recomienda espectro completo con THC. La TGA recomienda iniciar con dosis bajas y titular según respuesta.",
                bibliografia="TGA Australia (2024); Häuser W. Eur J Pain (2024); Busse JW et al. BMJ (2021); Serpell M, et al. Pain (2021).",
                nivel_estrellas="⭐⭐⭐",
                dosis_opciones=[0.10, 0.14, 0.20, 0.50, 1.0, 1.5, 2.0, 2.5],
                info_prospecto=[
                    "Dosis inicial: 0.14 mg/kg/día (≈10 mg/día en 70 kg)",
                    "Titulación: Aumentar gradualmente según tolerancia y respuesta",
                    "Dosis máxima: 2.8 mg/kg/día (≈200 mg/día en 70 kg)",
                    "Evidencia: Moderada - Guía TGA Australia (2024) y estudios controlados muestran beneficio modesto"
                ],
                prospectos=[
                    {"nombre": "Xpectra 10 - Prospecto", "archivo": "Xpectra-10_Prospecto_V.02.pdf", "descripcion": "Extracto de Cannabis Sativa L - Solución oral gotas (10%)"},
                    {"nombre": "Xatiplex - Prospecto", "archivo": "Xatiplex_Prospecto.pdf", "descripcion": "CBD purificado - Solución oral jeringa"}
                ]
            ),
        }
    
    def get_patologia(self, nombre: str) -> Optional[Patologia]:
        return self.patologias.get(nombre)
    
    def listar_patologias(self) -> List[str]:
        return list(self.patologias.keys())
    
    def listar_on_label(self) -> List[str]:
        return [
            nombre for nombre, p in self.patologias.items()
            if p.tipo == TipoIndicacion.ON_LABEL
        ]
    
    def listar_off_label(self) -> List[str]:
        return [
            nombre for nombre, p in self.patologias.items()
            if p.tipo == TipoIndicacion.OFF_LABEL
        ]

if __name__ == "__main__":
    catalogo = CatalogoPatologias()
    print("=" * 70)
    print("CATÁLOGO DE PATOLOGÍAS - GreenMed Pro")
    print("=" * 70)
    
    for nombre in catalogo.listar_patologias():
        p = catalogo.get_patologia(nombre)
        print(f"\n📌 {nombre}")
        print(f"   Producto recomendado: {p.producto_recomendado}")
        print(f"   Tipo: {p.tipo_producto}")
        print(f"   Dosis inicial: {p.dosis_inicial} mg/kg/día")
        print(f"   Dosis máxima: {p.dosis_max} mg/kg/día")
        print(f"   Opciones: {p.dosis_opciones}")
        print(f"   Prospectos: {len(p.prospectos) if p.prospectos else 0}")
        for linea in p.info_prospecto:
            print(f"   • {linea}")
    
    print("\n" + "=" * 70)
