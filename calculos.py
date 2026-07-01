"""
Módulo de cálculos para dosificación de CBD
"""

from typing import Dict, Tuple, Optional
from productos import Producto

class CalculadoraCBD:
    """Calculadora de dosis de CBD"""
    
    DOSIS_MINIMA = 0.01  # Valor mínimo genérico
    DOSIS_MAXIMA = 30.0  # Valor máximo genérico
    DOSIS_INICIAL = 2.5
    DOSIS_MANTENIMIENTO = 5.0
    
    def __init__(self, producto: Producto):
        self.producto = producto
        self.mg_por_ml = self._calcular_mg_por_ml()
        self.mg_por_gota = self._calcular_mg_por_gota() if producto.gotas_por_ml else None
    
    def _calcular_mg_por_ml(self) -> float:
        return (self.producto.concentracion / 100) * 1000
    
    def _calcular_mg_por_gota(self) -> Optional[float]:
        if self.producto.gotas_por_ml:
            return self.mg_por_ml / self.producto.gotas_por_ml
        return None
    
    def calcular_dosis_diaria(self, peso_kg: float, dosis_por_kg: float) -> Dict:
        dosis_mg = peso_kg * dosis_por_kg
        return {
            "dosis_mg": round(dosis_mg, 2),
            "dosis_por_kg": dosis_por_kg
        }
    
    def convertir_a_ml(self, mg: float) -> float:
        return mg / self.mg_por_ml
    
    def convertir_a_gotas(self, mg: float) -> Optional[float]:
        if self.mg_por_gota:
            return mg / self.mg_por_gota
        return None
    
    def calcular_dosis_por_toma(self, mg_diarios: float, tomas_por_dia: int = 2) -> Dict:
        mg_por_toma = mg_diarios / tomas_por_dia
        ml_por_toma = self.convertir_a_ml(mg_por_toma)
        gotas_por_toma = self.convertir_a_gotas(mg_por_toma) if self.mg_por_gota else None
        
        resultado = {
            "mg_por_toma": round(mg_por_toma, 2),
            "ml_por_toma": round(ml_por_toma, 3),
        }
        
        if gotas_por_toma is not None:
            resultado["gotas_por_toma"] = gotas_por_toma  # Mantener valor exacto para redondear después
        
        return resultado
    
    def calcular_pauta_completa(self, peso_kg: float, dosis_por_kg: float) -> Dict:
        dosis_diaria = self.calcular_dosis_diaria(peso_kg, dosis_por_kg)
        mg_diarios = dosis_diaria["dosis_mg"]
        dosis_toma = self.calcular_dosis_por_toma(mg_diarios, 2)
        
        resultado = {
            "peso": peso_kg,
            "dosis_por_kg": dosis_por_kg,
            "dosis_diaria_mg": mg_diarios,
            "dosis_por_toma_mg": dosis_toma["mg_por_toma"],
            "dosis_por_toma_ml": dosis_toma["ml_por_toma"],
            "tomas_por_dia": 2,
            "ml_por_dia": self.convertir_a_ml(mg_diarios),
            "ml_mensual": round(self.convertir_a_ml(mg_diarios * 30), 2),
            "mg_por_ml": round(self.mg_por_ml, 2),
            "producto": self.producto.nombre,
            "concentracion": self.producto.concentracion,
            "tipo": self.producto.tipo,
            "presentacion": self.producto.presentacion
        }
        
        if "gotas_por_toma" in dosis_toma:
            resultado["dosis_por_toma_gotas"] = dosis_toma["gotas_por_toma"]
            resultado["mg_por_gota"] = round(self.mg_por_gota, 3)
        
        return resultado
    
    def obtener_rangos_recomendados(self) -> Dict:
        return {
            "inicial": self.DOSIS_INICIAL,
            "mantenimiento": self.DOSIS_MANTENIMIENTO,
            "minimo": self.DOSIS_MINIMA,
            "maximo": self.DOSIS_MAXIMA
        }

def validar_dosis(dosis_por_kg: float, peso_kg: float, dosis_min: float = 0.01, dosis_max: float = 30.0) -> Tuple[bool, str]:
    """
    Validar que la dosis esté dentro del rango terapéutico
    
    Args:
        dosis_por_kg: Dosis en mg/kg/día
        peso_kg: Peso del paciente
        dosis_min: Dosis mínima para la patología específica
        dosis_max: Dosis máxima para la patología específica
    """
    if peso_kg <= 0:
        return False, "El peso debe ser mayor a 0 kg"
    
    if dosis_por_kg < dosis_min:
        return False, f"La dosis es menor al mínimo recomendado ({dosis_min:.2f} mg/kg/día)"
    
    if dosis_por_kg > dosis_max:
        return False, f"La dosis excede el máximo recomendado ({dosis_max:.2f} mg/kg/día)"
    
    if dosis_por_kg < CalculadoraCBD.DOSIS_INICIAL:
        return True, "Dosis inicial baja. Considere titulación gradual."
    
    if dosis_por_kg <= CalculadoraCBD.DOSIS_MANTENIMIENTO:
        return True, "Dosis dentro del rango de mantenimiento estándar."
    
    return True, "Dosis alta. Requiere monitoreo estrecho."
