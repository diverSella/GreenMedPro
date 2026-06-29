"""
Base de datos de patologías para GreenMed Pro
On-Label: según prospecto de Xpectra/Xatiplex
Off-Label: según evidencia científica
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

class TipoEvidencia(Enum):
    """Nivel de evidencia científica"""
    ALTA = "Alta"          # Múltiples ensayos clínicos robustos
    MODERADA = "Moderada"   # Algunos ensayos clínicos
    BAJA = "Baja"          # Estudios observacionales o casos
    PRELIMINAR = "Preliminar"  # Estudios iniciales

class TipoIndicacion(Enum):
    """Tipo de indicación"""
    ON_LABEL = "On-Label (prospecto)"
    OFF_LABEL = "Off-Label (evidencia científica)"

@dataclass
class Patologia:
    """Clase para representar una patología"""
    nombre: str
    tipo: TipoIndicacion
    dosis_min: float  # mg/kg/día
    dosis_max: float  # mg/kg/día
    dosis_inicial: float  # mg/kg/día
    dosis_mantenimiento: float  # mg/kg/día
    evidencia: TipoEvidencia
    descripcion: str
    referencias: List[str]  # IDs de referencias
    resumen: str = ""

class CatalogoPatologias:
    """Catálogo de patologías con indicaciones on y off-label"""
    
    def __init__(self):
        self.patologias: Dict[str, Patologia] = {
            # ============================================
            # ON-LABEL (según prospecto Xpectra/Xatiplex)
            # ============================================
            "Epilepsia refractaria": Patologia(
                nombre="Epilepsia refractaria",
                tipo=TipoIndicacion.ON_LABEL,
                dosis_min=2.5,
                dosis_max=20.0,
                dosis_inicial=2.5,
                dosis_mantenimiento=5.0,
                evidencia=TipoEvidencia.ALTA,
                descripcion="Epilepsia refractaria en niños y adultos. Basado en estudios con CBD.",
                referencias=["GW2018", "GW2020"],
                resumen="El CBD ha demostrado reducir significativamente la frecuencia de crisis en pacientes con epilepsia refractaria (síndrome de Lennox-Gastaut, Dravet)."
            ),
            
            # ============================================
            # OFF-LABEL (evidencia científica)
            # ============================================
            "Dolor crónico": Patologia(
                nombre="Dolor crónico",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=2.5,
                dosis_max=20.0,
                dosis_inicial=2.5,
                dosis_mantenimiento=10.0,
                evidencia=TipoEvidencia.MODERADA,
                descripcion="Manejo del dolor crónico no oncológico.",
                referencias=["Serpell2021", "Boychuk2022"],
                resumen="El CBD modula el sistema endocannabinoide y puede reducir la percepción del dolor. Estudios muestran mejoría en escala visual análoga (EVA) de 1-2 puntos."
            ),
            "Dolor neuropático": Patologia(
                nombre="Dolor neuropático",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=5.0,
                dosis_max=30.0,
                dosis_inicial=5.0,
                dosis_mantenimiento=15.0,
                evidencia=TipoEvidencia.MODERADA,
                descripcion="Dolor de origen neuropático.",
                referencias=["Serpell2021", "Xu2020"],
                resumen="El CBD actúa sobre receptores TRPV1 y canales de sodio, modulando la señalización del dolor neuropático. Estudios muestran reducción en escala DN4."
            ),
            "Fibromialgia": Patologia(
                nombre="Fibromialgia",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=5.0,
                dosis_max=20.0,
                dosis_inicial=5.0,
                dosis_mantenimiento=15.0,
                evidencia=TipoEvidencia.BAJA,
                descripcion="Síndrome de fibromialgia.",
                referencias=["Boychuk2022", "Silva2021"],
                resumen="Pacientes con fibromialgia reportan mejoría en puntuación de dolor y calidad de sueño con CBD. Evidencia aún limitada pero prometedora."
            ),
            "Ansiedad": Patologia(
                nombre="Ansiedad",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=10.0,
                dosis_max=30.0,
                dosis_inicial=10.0,
                dosis_mantenimiento=20.0,
                evidencia=TipoEvidencia.MODERADA,
                descripcion="Trastornos de ansiedad generalizada y social.",
                referencias=["Crippa2021", "Shannon2022"],
                resumen="El CBD modula la respuesta al estrés y reduce la ansiedad en modelos preclínicos y estudios en humanos. Efecto ansiolítico dosis-dependiente."
            ),
            "Insomnio": Patologia(
                nombre="Insomnio",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=10.0,
                dosis_max=25.0,
                dosis_inicial=10.0,
                dosis_mantenimiento=20.0,
                evidencia=TipoEvidencia.MODERADA,
                descripcion="Trastorno del sueño con dificultad para iniciar o mantener el sueño.",
                referencias=["Shannon2022", "Rudroff2021"],
                resumen="El CBD mejora la calidad del sueño y reduce el tiempo de latencia. Efecto probablemente mediado por modulación de la ansiedad y ritmos circadianos."
            ),
            "Esclerosis múltiple": Patologia(
                nombre="Esclerosis múltiple",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=5.0,
                dosis_max=20.0,
                dosis_inicial=5.0,
                dosis_mantenimiento=15.0,
                evidencia=TipoEvidencia.BAJA,
                descripcion="Espasticidad y dolor asociados a esclerosis múltiple.",
                referencias=["Rudroff2021", "Serpell2021"],
                resumen="El CBD reduce la espasticidad y mejora la calidad de vida en pacientes con EM. Estudios con Sativex muestran eficacia, CBD solo tiene evidencia preliminar."
            ),
            "Cuidados paliativos": Patologia(
                nombre="Cuidados paliativos",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=5.0,
                dosis_max=30.0,
                dosis_inicial=5.0,
                dosis_mantenimiento=15.0,
                evidencia=TipoEvidencia.MODERADA,
                descripcion="Síntomas en pacientes paliativos: dolor, náuseas, anorexia, ansiedad.",
                referencias=["Boychuk2022", "Crippa2021"],
                resumen="El CBD mejora múltiples síntomas en cuidados paliativos: dolor, náuseas, apetito y bienestar general. Buena tolerancia en pacientes frágiles."
            ),
            "TEPT (Estrés postraumático)": Patologia(
                nombre="TEPT (Estrés postraumático)",
                tipo=TipoIndicacion.OFF_LABEL,
                dosis_min=10.0,
                dosis_max=30.0,
                dosis_inicial=10.0,
                dosis_mantenimiento=20.0,
                evidencia=TipoEvidencia.BAJA,
                descripcion="Trastorno de estrés postraumático.",
                referencias=["Shannon2022", "Crippa2021"],
                resumen="El CBD reduce los síntomas de hipervigilancia y pesadillas en TEPT. Evidencia preliminar, se necesitan más ensayos clínicos."
            ),
        }
    
    def get_patologia(self, nombre: str) -> Optional[Patologia]:
        """Obtener una patología por su nombre"""
        return self.patologias.get(nombre)
    
    def listar_patologias(self) -> List[str]:
        """Listar todas las patologías"""
        return list(self.patologias.keys())
    
    def listar_on_label(self) -> List[str]:
        """Listar patologías on-label"""
        return [
            nombre for nombre, p in self.patologias.items()
            if p.tipo == TipoIndicacion.ON_LABEL
        ]
    
    def listar_off_label(self) -> List[str]:
        """Listar patologías off-label"""
        return [
            nombre for nombre, p in self.patologias.items()
            if p.tipo == TipoIndicacion.OFF_LABEL
        ]
    
    def get_por_tipo(self, tipo: TipoIndicacion) -> List[Dict]:
        """Obtener patologías por tipo con formato de diccionario"""
        return [
            {
                "nombre": p.nombre,
                "tipo": p.tipo.value,
                "dosis_min": p.dosis_min,
                "dosis_max": p.dosis_max,
                "dosis_inicial": p.dosis_inicial,
                "dosis_mantenimiento": p.dosis_mantenimiento,
                "evidencia": p.evidencia.value,
                "descripcion": p.descripcion,
                "resumen": p.resumen,
                "referencias": p.referencias
            }
            for p in self.patologias.values()
            if p.tipo == tipo
        ]

# Para prueba rápida
if __name__ == "__main__":
    catalogo = CatalogoPatologias()
    print("=" * 60)
    print("CATÁLOGO DE PATOLOGÍAS - GreenMed Pro")
    print("=" * 60)
    
    print("\n🔵 ON-LABEL (prospecto):")
    for nombre in catalogo.listar_on_label():
        p = catalogo.get_patologia(nombre)
        print(f"  • {nombre}: {p.dosis_min}-{p.dosis_max} mg/kg/día")
    
    print("\n🟢 OFF-LABEL (evidencia):")
    for nombre in catalogo.listar_off_label():
        p = catalogo.get_patologia(nombre)
        print(f"  • {nombre}: {p.dosis_min}-{p.dosis_max} mg/kg/día (Evidencia: {p.evidencia.value})")
    
    print("\n" + "=" * 60)
