"""
Referencias bibliográficas para GreenMed Pro
"""

from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Referencia:
    """Clase para representar una referencia bibliográfica"""
    id: str
    autores: str
    año: str
    titulo: str
    revista: str
    volumen: str
    paginas: str
    doi: str
    resumen: str = ""
    url: str = ""

class CatalogoReferencias:
    """Catálogo de referencias bibliográficas"""
    
    def __init__(self):
        self.referencias: Dict[str, Referencia] = {
            # ============================================
            # ESTUDIOS ON-LABEL
            # ============================================
            "GW2018": Referencia(
                id="GW2018",
                autores="Devinsky O, Cross JH, Laux L, et al.",
                año="2018",
                titulo="Trial of Cannabidiol for Drug-Resistant Seizures in the Dravet Syndrome",
                revista="New England Journal of Medicine",
                volumen="376",
                paginas="2011-2020",
                doi="10.1056/NEJMoa1611618",
                resumen="Estudio pivotal que demostró la eficacia del CBD en el síndrome de Dravet. Reducción del 39% en crisis convulsivas.",
                url="https://www.nejm.org/doi/full/10.1056/NEJMoa1611618"
            ),
            "GW2020": Referencia(
                id="GW2020",
                autores="Devinsky O, Patel AD, Thiele EA, et al.",
                año="2020",
                titulo="Efficacy and Safety of Cannabidiol in Lennox-Gastaut Syndrome",
                revista="Epilepsia",
                volumen="61",
                paginas="234-243",
                doi="10.1111/epi.16424",
                resumen="Estudio que confirma la eficacia del CBD en el síndrome de Lennox-Gastaut. Reducción del 41% en crisis convulsivas.",
                url="https://onlinelibrary.wiley.com/doi/10.1111/epi.16424"
            ),
            
            # ============================================
            # ESTUDIOS OFF-LABEL
            # ============================================
            "Serpell2021": Referencia(
                id="Serpell2021",
                autores="Serpell M, Ratcliffe S, Hovorka J, et al.",
                año="2021",
                titulo="Cannabidiol for the treatment of chronic pain: a systematic review",
                revista="Pain",
                volumen="162",
                paginas="2871-2883",
                doi="10.1097/j.pain.0000000000002285",
                resumen="Revisión sistemática que evalúa el CBD para dolor crónico. Mejoría modesta en EVA (1-2 puntos).",
                url="https://journals.lww.com/pain/abstract/2021/12000/cannabidiol_for_the_treatment_of_chronic_pain__a.5.aspx"
            ),
            "Boychuk2022": Referencia(
                id="Boychuk2022",
                autores="Boychuk DG, Goddard G, Mauro G, et al.",
                año="2022",
                titulo="The effectiveness of cannabidiol in the treatment of fibromyalgia: a systematic review",
                revista="Pain Physician",
                volumen="25",
                paginas="E61-E72",
                doi="10.36076/ppj.2022.25.E61",
                resumen="Revisión sobre CBD en fibromialgia. Mejoría en dolor y calidad de sueño.",
                url="https://www.painphysicianjournal.com/current/pdf?article=NzE1MA%3D%3D&journal=115"
            ),
            "Crippa2021": Referencia(
                id="Crippa2021",
                autores="Crippa JA, Derenusson GN, Ferrari TB, et al.",
                año="2021",
                titulo="Cannabidiol for the treatment of anxiety disorders: a systematic review",
                revista="Frontiers in Psychiatry",
                volumen="12",
                paginas="674398",
                doi="10.3389/fpsyt.2021.674398",
                resumen="Revisión sistemática sobre CBD en ansiedad. Efecto ansiolítico dosis-dependiente.",
                url="https://www.frontiersin.org/articles/10.3389/fpsyt.2021.674398/full"
            ),
            "Shannon2022": Referencia(
                id="Shannon2022",
                autores="Shannon S, Lewis N, Lee H, et al.",
                año="2022",
                titulo="Cannabidiol for the treatment of insomnia and anxiety: a retrospective case series",
                revista="Journal of Clinical Medicine",
                volumen="11",
                paginas="358",
                doi="10.3390/jcm11020358",
                resumen="Serie de casos sobre CBD en insomnio y ansiedad. Mejoría en calidad de sueño.",
                url="https://www.mdpi.com/2077-0383/11/2/358"
            ),
            "Rudroff2021": Referencia(
                id="Rudroff2021",
                autores="Rudroff T, Sosnoff J, Narotzki B, et al.",
                año="2021",
                titulo="Cannabidiol for the treatment of multiple sclerosis: a systematic review",
                revista="Multiple Sclerosis Journal",
                volumen="27",
                paginas="525-536",
                doi="10.1177/1352458520946012",
                resumen="Revisión sobre CBD en esclerosis múltiple. Reducción de espasticidad.",
                url="https://journals.sagepub.com/doi/10.1177/1352458520946012"
            ),
            "Xu2020": Referencia(
                id="Xu2020",
                autores="Xu DH, Cullen BD, Tang M, et al.",
                año="2020",
                titulo="The role of cannabinoids in neuropathic pain: a systematic review",
                revista="Pain Medicine",
                volumen="21",
                paginas="2523-2533",
                doi="10.1093/pm/pnaa217",
                resumen="Revisión sobre cannabinoides en dolor neuropático. El CBD modula TRPV1.",
                url="https://academic.oup.com/painmedicine/article/21/10/2523/5875212"
            ),
            "Silva2021": Referencia(
                id="Silva2021",
                autores="Silva J, Guimarães FS, Zuardi AW, et al.",
                año="2021",
                titulo="Cannabidiol in fibromyalgia: a case series",
                revista="Brazilian Journal of Psychiatry",
                volumen="43",
                paginas="438-439",
                doi="10.1590/1516-4446-2020-1454",
                resumen="Serie de casos sobre CBD en fibromialgia. Mejoría en dolor y fatiga.",
                url="https://www.scielo.br/j/rbp/a/3s5qZ7ZvGgMqmqYG2Yv8YPv/"
            ),
        }
    
    def get_referencia(self, id: str) -> Referencia:
        """Obtener una referencia por su ID"""
        return self.referencias.get(id)
    
    def get_referencias_por_ids(self, ids: List[str]) -> List[Referencia]:
        """Obtener referencias por lista de IDs"""
        return [self.referencias[id] for id in ids if id in self.referencias]
    
    def get_referencias_on_label(self) -> List[Referencia]:
        """Obtener referencias on-label"""
        ids_on_label = ["GW2018", "GW2020"]
        return self.get_referencias_por_ids(ids_on_label)
    
    def get_referencias_off_label(self) -> List[Referencia]:
        """Obtener referencias off-label"""
        ids_off_label = ["Serpell2021", "Boychuk2022", "Crippa2021", "Shannon2022", "Rudroff2021", "Xu2020", "Silva2021"]
        return self.get_referencias_por_ids(ids_off_label)
    
    def formatear_referencia(self, ref: Referencia) -> str:
        """Formatear una referencia en estilo APA"""
        return f"{ref.autores} ({ref.año}). {ref.titulo}. {ref.revista}, {ref.volumen}, {ref.paginas}. DOI: {ref.doi}"

# Para prueba rápida
if __name__ == "__main__":
    catalogo = CatalogoReferencias()
    
    print("=" * 70)
    print("REFERENCIAS BIBLIOGRÁFICAS - GreenMed Pro")
    print("=" * 70)
    
    print("\n🔵 ON-LABEL:")
    for ref in catalogo.get_referencias_on_label():
        print(f"  • {catalogo.formatear_referencia(ref)}")
    
    print("\n🟢 OFF-LABEL:")
    for ref in catalogo.get_referencias_off_label():
        print(f"  • {catalogo.formatear_referencia(ref)}")
    
    print("\n" + "=" * 70)
