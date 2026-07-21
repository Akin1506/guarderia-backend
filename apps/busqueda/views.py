from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.ninos.models import Nino
from apps.tutores.models import Tutor
from apps.salas.models import Sala


class BusquedaGlobalView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        termino = request.GET.get("q", "").strip()

        if termino == "":
            return Response([])

        termino_lower = termino.lower()

        resultados = []

        # ==================================================
        # MÓDULOS DEL SISTEMA
        # ==================================================

        modulos = [
            {"nombre": "Dashboard", "ruta": "/dashboard", "icono": "🏠"},
            {"nombre": "Niños", "ruta": "/ninos", "icono": "👶"},
            {"nombre": "Favoritos", "ruta": "/favoritos", "icono": "❤️"},
            {"nombre": "Tutores", "ruta": "/tutores", "icono": "👨‍👩‍👧"},
            {"nombre": "Salas", "ruta": "/salas", "icono": "🏫"},
            {"nombre": "Servicios", "ruta": "/servicios", "icono": "🛎️"},
            {"nombre": "Actividades", "ruta": "/actividades", "icono": "📅"},
            {"nombre": "Asistencia", "ruta": "/asistencia", "icono": "📝"},
            {"nombre": "Salud", "ruta": "/salud", "icono": "❤️"},
        ]

        coincidencias_inicio = []
        coincidencias_contiene = []

        for modulo in modulos:

            nombre = modulo["nombre"].lower()

            if nombre.startswith(termino_lower):
                coincidencias_inicio.append(modulo)

            elif termino_lower in nombre:
                coincidencias_contiene.append(modulo)

        for modulo in coincidencias_inicio + coincidencias_contiene:

            resultados.append({
                "tipo": "Módulo",
                "nombre": modulo["nombre"],
                "ruta": modulo["ruta"],
                "icono": modulo["icono"],
            })

        # ==================================================
        # NIÑOS
        # ==================================================

        for nino in Nino.objects.filter(
            nombre__icontains=termino,
            activo=True
        )[:5]:

            resultados.append({
                "tipo": "Niño",
                "id": nino.id_nino,
                "nombre": nino.nombre,
                "icono": "👶",
            })

        # ==================================================
        # TUTORES
        # ==================================================

        for tutor in Tutor.objects.filter(
            nombre__icontains=termino,
            activo=True
        )[:5]:

            resultados.append({
                "tipo": "Tutor",
                "id": tutor.id_tutor,
                "nombre": tutor.nombre,
                "icono": "👨‍👩‍👧",
            })

        # ==================================================
        # SALAS
        # ==================================================

        for sala in Sala.objects.filter(
            nombre__icontains=termino,
            activo=True
        )[:5]:

            resultados.append({
                "tipo": "Sala",
                "id": sala.id_sala,
                "nombre": sala.nombre,
                "icono": "🏫",
            })

        return Response(resultados)