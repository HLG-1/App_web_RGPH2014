# urls.py (dans votre app)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DemographicDataViewSet, MetadataViewSet
from . import views

# Configuration du router DRF
router = DefaultRouter()
router.register(r'demographic', DemographicDataViewSet, basename='demographic')
router.register(r'metadata', MetadataViewSet, basename='metadata')

# Patterns d'URL
urlpatterns = [
    # URLs du router DRF
    path('api/', include(router.urls)),
    path('api/menages/taille-moyenne/', views.taille_moyenne_menages, name='taille_moyenne_menages'),
    path('api/menages/distribution-taille/', views.distribution_taille_categorisee, name='distribution_taille_categorisee'),
    
    # Analyses des équipements
    path('api/menages/equipements-base/', views.analyse_equipements_base, name='analyse_equipements_base'),
    path('api/menages/equipements-complets/', views.menages_equipements_complets, name='menages_equipements_complets'),
    
    # Analyses spécialisées
    path('api/menages/distance-route/', views.distance_moyenne_route, name='distance_moyenne_route'),
    path('api/menages/modes-cuisson/', views.repartition_modes_cuisson, name='repartition_modes_cuisson'),
    
    # Statistiques globales
    path('api/menages/statistiques-globales/', views.statistiques_globales, name='statistiques_globales'),
    
    # Analyse par région
    path('api/menages/region/<int:region_id>/', views.analyse_par_region, name='analyse_par_region'),
     path('api/menages/analyse-avancee/', views.analyse_avancee, name='analyse_avancee'),

]

