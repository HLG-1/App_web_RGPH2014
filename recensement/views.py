
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q, Avg, Max, Min, F, Case, When, IntegerField
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Individu  
from .serializers import IndividuSerializer, IndividuMinimalSerializer
from rest_framework import serializers
import json
import logging
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Menage
from .serializers import TailleMenageSerializer, TailleCategorieSerializer, EquipementSerializer, EquipementCompletSerializer, DistanceRouteSerializer, ModeCuissonSerializer;



logger = logging.getLogger(__name__)


def get_education_level_label(niveau_code):
    """
    Retourne le libellé correspondant au code du niveau d'éducation
    """
    education_levels = {
        0: "Aucun niveau d'études",
        1: "Préscolaire",
        2: "Primaire",
        3: "Secondaire collégial",
        4: "Secondaire qualifiant",
        5: "Supérieur",
    }
    return education_levels.get(niveau_code, "Non défini")

def get_activity_status_label(code):
    """Convertit le code statut d activité en libellé"""
    labels = {
        1: "Population active",
        2: "Population inactive",
        3: "Chômeur",
        4: "Employé",
        5: "Étudiant",
        6: "Retraité"
    }
    return labels.get(code, f"Statut {code}")

def get_sexe_label(code):
    """Retourne le libellé du sexe"""
    labels = {
        1: "Masculin",
        2: "Féminin"
    }
    return labels.get(code, "Non renseigné")

def get_milieu_label(code):
    """Retourne le libellé du milieu"""
    labels = {
        1: "Urbain",
        2: "Rural"
    }
    return labels.get(code, "Non renseigné")

def get_age_quinquennal_label(code):
    """Retourne le libellé de l'âge quinquennal"""
    labels = {
        0: "0-4 ans",
        5: "5-9 ans",
        10: "10-14 ans",
        15: "15-19 ans",
        20: "20-24 ans",
        25: "25-29 ans",
        30: "30-34 ans",
        35: "35-39 ans",
        40: "40-44 ans",
        45: "45-49 ans",
        50: "50-54 ans",
        55: "55-59 ans",
        60: "60-64 ans",
        65: "65-69 ans",
        70: "70-74 ans",
        75: "75 ans et plus",
        99: "Non déterminé"
    }
    return labels.get(code, f"Âge {code}")

def get_lien_chef_menage_label(code):
    """Retourne le libellé du lien avec le chef de ménage"""
    labels = {
        0: "Chef de ménage",
        1: "Conjoint",
        2: "Fils / Fille",
        3: "Petit-fils / Petite-fille",
        4: "Père / Mère",
        5: "Frère / Sœur",
        6: "Gendre / Bru",
        7: "Autre parent",
        8: "Domestique",
        9: "Personne sans lien de parenté",
        99: "Non déterminé"
    }
    return labels.get(code, f"Lien {code}")


class DemographicDataViewSet(viewsets.ModelViewSet):
    queryset = Individu.objects.all()
    serializer_class = IndividuSerializer
    
    def get_queryset(self):
        """Filtrage dynamique basé sur les paramètres de requête"""
        try:
            queryset = super().get_queryset()
            
            # Filtres par région, province, milieu
            region = self.request.query_params.get('region', None)
            province = self.request.query_params.get('province', None)
            milieu = self.request.query_params.get('milieu', None)
            
            if region:
                queryset = queryset.filter(region=region)
            if province:
                queryset = queryset.filter(province=province)
            if milieu:
                queryset = queryset.filter(milieu=milieu)
                
            return queryset
        except Exception as e:
            logger.error(f"Erreur dans get_queryset: {e}")
            return Individu.objects.none()
    def get_education_level_label(self,niveau_code):
        """
        Retourne le libellé correspondant au code du niveau d'éducation
        """
        education_levels = {
            0: "Aucun niveau d'études",
            1: "Préscolaire",
            2: "Primaire",
            3: "Secondaire collégial",
            4: "Secondaire qualifiant",
            5: "Supérieur",
        }
        return education_levels.get(niveau_code, "Non défini")

    def get_activity_type_label(self, code):
        """Retourne le libellé pour le type d'activité"""
        labels = {
            0: "Actif occupé",
            1: "Chômeur n'ayant jamais travaillé", 
            2: "Chômeur ayant déjà travaillé",
            3: "Femme au foyer",
            4: "Élève/Étudiant",
            5: "Autre inactif",
            9: "Non déterminé"
        }
        return labels.get(code, f"Code {code}")

    def get_secteur_activite_label(self, code):
        """Retourne le libellé pour le secteur d'activité"""
        labels = {
            1: "Agriculture, sylviculture et pêche",
            2: "Industries extractives et manufacturières",
            3: "Eau, gaz et électricité",
            4: "Construction",
            5: "Commerce et réparation d'automobiles",
            6: "Transports, entreposage et communication",
            7: "Autres services marchands",
            8: "Administration publique, enseignement, santé",
            96: "Non déterminé",
            97: "Type d'activité non déterminé",
            98: "Chômeur n'ayant jamais travaillé",
            99: "Inactif"
        }
        return labels.get(code, f"Secteur {code}")

    def get_section_activite_label(self, code):
        """Retourne le libellé pour la section d'activité"""
        labels = {
            1: "Agriculture, sylviculture et pêche",
            2: "Industries extractives", 
            3: "Industries manufacturières",
            4: "Électricité, gaz, vapeur et air conditionné",
            5: "Eau, assainissement, gestion des déchets",
            6: "Construction",
            7: "Commerce et réparation d'automobiles",
            8: "Transports et entreposage",
            9: "Hébergement et restauration",
            10: "Information et communication",
            11: "Activités financières et d'assurance",
            12: "Activités immobilières",
            13: "Activités spécialisées, scientifiques et techniques",
            14: "Activités de services administratifs",
            15: "Administration publique",
            16: "Enseignement",
            17: "Santé humaine et action sociale",
            18: "Arts, spectacles et activités récréatives",
            19: "Autres activités de services",
            20: "Activités des ménages en tant qu'employeurs",
            21: "Activités extraterritoriales"
        }
        return labels.get(code, f"Section {code}")

    @action(detail=False, methods=['get'], url_path='population-lien-chef')
    def population_lien_chef(self, request):
        """Répartition de la population selon le lien avec le chef de ménage"""
        try:
            queryset = self.get_queryset().filter(lien_chef_menage__isnull=False)
            
            data = queryset.values('lien_chef_menage').annotate(
                effectif=Count('id')
            ).order_by('lien_chef_menage')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
           
            results = []
            for item in data_list:
                lien_code = item['lien_chef_menage']
                pourcentage = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                results.append({
                    'lien_chef_menage': lien_code,
                    'lien_chef_menage_display': get_lien_chef_menage_label(lien_code),
                    'effectif': item['effectif'],
                    'pourcentage': pourcentage
                })
            
            return Response({
                'data': results,
                'total': total,
                'metadata': {
                    'note': 'Répartition de la population selon le lien avec le chef de ménage'
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans population_lien_chef: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la répartition selon le lien avec le chef de ménage',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='chef-menage-sexe')
    def chef_menage_sexe(self, request):
        """Répartition des chefs de ménage par sexe"""
        try:
            queryset = self.get_queryset().filter(
                lien_chef_menage=0,  
                sexe__isnull=False
            )
            
            data = queryset.values('sexe').annotate(
                effectif=Count('id')
            ).order_by('sexe')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            
            results = []
            for item in data_list:
                sexe_code = item['sexe']
                pourcentage = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                results.append({
                    'sexe': sexe_code,
                    'sexe_display': get_sexe_label(sexe_code),
                    'effectif': item['effectif'],
                    'pourcentage': pourcentage
                })
            
            return Response({
                'data': results,
                'total': total,
                'metadata': {
                    'note': 'Répartition des chefs de ménage par sexe'
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans chef_menage_sexe: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la répartition des chefs de ménage par sexe',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='femme-chef-menage-milieu-age')
    def femme_chef_menage_milieu_age(self, request):
        """Répartition des femmes chefs de ménage par milieu et groupes d'âge"""
        try:
            queryset = self.get_queryset().filter(
                lien_chef_menage=0,  # Chefs de ménage uniquement
                sexe=2,  # Femmes
                age_quinquennal__isnull=False,
                milieu__isnull=False
            )
            
            data = queryset.values('age_quinquennal', 'milieu').annotate(
                effectif=Count('id')
            ).order_by('age_quinquennal', 'milieu')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
        
            results = []
            for item in data_list:
                age_code = item['age_quinquennal']
                milieu_code = item['milieu']
                pourcentage = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                results.append({
                    'age_quinquennal': age_code,
                    'age_quinquennal_display': get_age_quinquennal_label(age_code),
                    'milieu': milieu_code,
                    'milieu_display': get_milieu_label(milieu_code),
                    'effectif': item['effectif'],
                    'pourcentage': pourcentage
                })
            
         
         
            stats_par_milieu = queryset.values('milieu').annotate(
                effectif=Count('id')
            ).order_by('milieu')
            
            milieu_stats = []
            for item in stats_par_milieu:
                milieu_code = item['milieu']
                pourcentage = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                milieu_stats.append({
                    'milieu': milieu_code,
                    'milieu_display': get_milieu_label(milieu_code),
                    'effectif': item['effectif'],
                    'pourcentage': pourcentage
                })
            
            return Response({
                'data': results,
                'stats_par_milieu': milieu_stats,
                'total': total,
                'metadata': {
                    'note': 'Répartition des femmes chefs de ménage par milieu et groupes d\'âge'
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans femme_chef_menage_milieu_age: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la répartition des femmes chefs de ménage',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def chefs_menage(self, request):
        """Analyse complète des chefs de ménage"""
        try:
            # Population selon lien avec le chef de ménage
            lien_data = self.get_queryset().values('lien_chef_menage').annotate(
                effectif=Count('id')
            ).order_by('lien_chef_menage')
            
            # Chefs de ménage par sexe
            chefs_sexe = self.get_queryset().filter(
                lien_chef_menage=0
            ).values('sexe').annotate(
                effectif=Count('id')
            ).order_by('sexe')
            
            # Chefs de ménage par âge
            chefs_age = self.get_queryset().filter(
                lien_chef_menage=0
            ).values('age_quinquennal').annotate(
                effectif=Count('id')
            ).order_by('age_quinquennal')
            
            # Ajout des libellés
            lien_data_formatted = []
            for item in lien_data:
                lien_data_formatted.append({
                    'lien_chef_menage': item['lien_chef_menage'],
                    'lien_chef_menage_display': get_lien_chef_menage_label(item['lien_chef_menage']),
                    'effectif': item['effectif']
                })
            
            chefs_sexe_formatted = []
            for item in chefs_sexe:
                chefs_sexe_formatted.append({
                    'sexe': item['sexe'],
                    'sexe_display': get_sexe_label(item['sexe']),
                    'effectif': item['effectif']
                })
            
            chefs_age_formatted = []
            for item in chefs_age:
                chefs_age_formatted.append({
                    'age_quinquennal': item['age_quinquennal'],
                    'age_quinquennal_display': get_age_quinquennal_label(item['age_quinquennal']),
                    'effectif': item['effectif']
                })
            
            return Response({
                'lien_chef_menage': lien_data_formatted,
                'chefs_par_sexe': chefs_sexe_formatted,
                'chefs_par_age': chefs_age_formatted,
                'total_chefs': sum(item['effectif'] for item in chefs_sexe),
                'metadata': {
                    'note': 'Analyse complète des chefs de ménage'
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans chefs_menage: {e}")
            return Response({
                'error': 'Erreur lors du calcul des chefs de ménage',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    @action(detail=False, methods=['get'], url_path='activite-economique')
    def activite_economique(self, request):
        """Analyse de l'activité économique selon la méthodologie standard"""
        try:
            queryset = self.get_queryset()
            
           
            queryset_actif = queryset.filter(age_quinquennal__gte=15)
            
            # 1. Analyse globale population active/inactive
            statut_activite = queryset_actif.extra(
                select={
                    'statut_activite': """
                        CASE 
                            WHEN type_activite IN (0,1,2) THEN 'Population active'
                            WHEN type_activite IN (3,4,5) THEN 'Population inactive'
                            ELSE 'Autre'
                        END
                    """
                }
            ).values('statut_activite').annotate(
                effectif=Count('id')
            ).order_by('statut_activite')
            
            # 2. Analyse détaillée par type d'activité
            data = queryset_actif.values('type_activite').annotate(
                effectif=Count('id')
            ).order_by('type_activite')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
           
            graphique_data = []
            colors = [
                '#000e4b', '#324373', '#ffcc00', '#ffefa3', 
                '#738aba', '#b4ceff', '#2563eb', '#3b82f6',
                '#06b6d4', '#0891b2', '#059669', '#10b981'
            ];

            for i, item in enumerate(data_list):
                if item['type_activite'] is not None:
                    pourcentage = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                    graphique_data.append({
                        'code': item['type_activite'],
                        'label': self.get_activity_type_label(item['type_activite']),
                        'effectif': item['effectif'],
                        'pourcentage': pourcentage,
                        'color': colors[i % len(colors)]
                    })
           
            # Population active = actifs occupés (0) + chômeurs (1,2)
            actifs_occupes = next((item['effectif'] for item in data_list if item['type_activite'] == 0), 0)
            chomeurs_total = sum(item['effectif'] for item in data_list if item['type_activite'] in [1, 2])
            population_active = actifs_occupes + chomeurs_total
            
            # Population inactive = codes 3,4,5
            inactifs_total = sum(item['effectif'] for item in data_list if item['type_activite'] in [3, 4, 5])
            
            # Calcul des taux (méthodologie BIT/OIT)
            taux_activite = round((population_active / total) * 100, 2) if total > 0 else 0
            
            taux_chomage = round((chomeurs_total / population_active) * 100, 2) if population_active > 0 else 0
            taux_emploi = round((actifs_occupes / total) * 100, 2) if total > 0 else 0
            taux_inactivite = round((inactifs_total / total) * 100, 2) if total > 0 else 0
            

            statut_data = []
            for item in statut_activite:
                pourcentage = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                statut_data.append({
                    'statut': item['statut_activite'],
                    'effectif': item['effectif'],
                    'pourcentage': pourcentage
                })
            
            return Response({
                'data': graphique_data,
                'statut_activite': statut_data,
                'total': total,
                'indicateurs': {
                    'taux_activite': taux_activite,
                    'taux_chomage': taux_chomage,
                    'taux_emploi': taux_emploi,
                    'taux_inactivite': taux_inactivite,
                    'population_active': population_active,
                    'actifs_occupes': actifs_occupes,
                    'chomeurs_total': chomeurs_total,
                    'inactifs_total': inactifs_total
                },
                'metadata': {
                    'note': 'Population de 15 ans et plus - Méthodologie BIT/OIT avec noms Django',
                    'classification': {
                        'population_active': 'type_activite codes 0,1,2 (actifs occupés + chômeurs)',
                        'population_inactive': 'type_activite codes 3,4,5 (inactifs)'
                    },
                    'formules': {
                        'taux_activite': '(Population active / Total population 15+) * 100',
                        'taux_chomage': '(Chômeurs / Population active) * 100',
                        'taux_emploi': '(Actifs occupés / Total population 15+) * 100',
                        'taux_inactivite': '(Inactifs / Total population 15+) * 100'
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans activite_economique: {e}")
            return Response({
                'error': 'Erreur lors du calcul de l\'activité économique',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'], url_path='secteurs-economiques')
    def secteurs_economiques(self, request):
        """Répartition par secteurs d'activité économique avec données graphiques"""
        try:
           
            queryset = self.get_queryset().filter(type_activite=0)
            
            secteurs = queryset.values('activite_economique_general').annotate(
                effectif=Count('id')
            ).order_by('-effectif')
            
            sections = queryset.values('activite_economique_superieur').annotate(
                effectif=Count('id')
            ).order_by('-effectif')
            
            total_actifs = queryset.count()
            
          
            secteurs_data = []
            colors_secteurs = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
            
            for i, item in enumerate(secteurs):
                if item['activite_economique_general'] is not None:
                    pourcentage = round((item['effectif'] / total_actifs) * 100, 2) if total_actifs > 0 else 0
                    secteurs_data.append({
                        'code': item['activite_economique_general'],
                        'label': self.get_secteur_activite_label(item['activite_economique_general']),
                        'effectif': item['effectif'],
                        'pourcentage': pourcentage,
                        'color': colors_secteurs[i % len(colors_secteurs)]
                    })
            
            # Préparation des données sections pour graphiques
            sections_data = []
            for i, item in enumerate(sections):
                if item['activite_economique_superieur'] is not None:
                    pourcentage = round((item['effectif'] / total_actifs) * 100, 2) if total_actifs > 0 else 0
                    sections_data.append({
                        'code': item['activite_economique_superieur'],
                        'label': self.get_section_activite_label(item['activite_economique_superieur']),
                        'effectif': item['effectif'],
                        'pourcentage': pourcentage
                    })
            
          
            professions = queryset.values('profession_general').annotate(
                effectif=Count('id')
            ).order_by('-effectif')[:10]  
            
            return Response({
                'secteurs': secteurs_data,
                'sections': sections_data[:15],  
                'professions': list(professions),
                'total_actifs': total_actifs,
                'metadata': {
                    'note': 'Données pour les actifs occupés uniquement',
                    'nombre_secteurs': len(secteurs_data),
                    'nombre_sections': len(sections_data)
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans secteurs_economiques: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse des secteurs économiques',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='emploi-education')
    def emploi_education(self, request):
        """Analyse croisée entre emploi et niveau d'éducation"""
        try:
            queryset = self.get_queryset().filter(
                type_activite=0,  # Actifs occupés
                age_quinquennal__gte=15  # 15 ans et plus
            )
            
            # Croisement niveau d'études et secteur d'activité
            croises = queryset.values('niveau_etudes_agrege', 'activite_economique_general').annotate(
                effectif=Count('id')
            ).order_by('niveau_etudes_agrege', 'activite_economique_general')

            # Préparation des données pour matrice de corrélation
            matrice_data = []
            for item in croises:
                if item['niveau_etudes_agrege'] is not None and item['activite_economique_general'] is not None:
                    matrice_data.append({
                        'niveau_etudes': item['niveau_etudes_agrege'],
                        'niveau_etudes_label': self.get_education_level_label(item['niveau_etudes_agrege']),
                        'secteur_activite': item['activite_economique_general'],
                        'secteur_activite_label': self.get_secteur_activite_label(item['activite_economique_general']),
                        'effectif': item['effectif']
                    })
            
            # Statistiques par niveau d'éducation
            education_stats = queryset.values('niveau_etudes_agrege').annotate(
                effectif=Count('id')
            ).order_by('niveau_etudes_agrege')
            
            education_data = []
            for item in education_stats:
                if item['niveau_etudes_agrege'] is not None:
                    education_data.append({
                        'code': item['niveau_etudes_agrege'],
                        'label': self.get_education_level_label(item['niveau_etudes_agrege']),
                        'effectif': item['effectif']
                    })
            
            return Response({
                'matrice_emploi_education': matrice_data,
                'education_stats': education_data,
                'total_analyses': len(matrice_data),
                'total_actifs': queryset.count()
            })
            
        except Exception as e:
            logger.error(f"Erreur dans emploi_education: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse emploi-éducation',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['get'])
    def population_par_age(self, request):
        """Analyse de la population par âge"""
        try:
            type_age = request.query_params.get('type', 'simple')
            
          
            queryset = self.get_queryset()
            
            if type_age == 'quinquennal':
             
                data = queryset.values('age_quinquennal').annotate(
                    effectif=Count('id')
                ).order_by('age_quinquennal')
                
       
                total = queryset.count()
                
                data = queryset.values('age_quinquennal').annotate(
                    effectif=Count('id'),
                    pourcentage=Count('id') * 100.0 / total if total > 0 else 0
                ).order_by('age_quinquennal')
                
            else:
                total = queryset.count()
                data = queryset.values('age_simple').annotate(
                    effectif=Count('id'),
                    pourcentage=Count('id') * 100.0 / total if total > 0 else 0
                ).order_by('age_simple')
            
            return Response({
                'type': type_age,
                'data': list(data),
                'total': total
            })
            
        except Exception as e:
            logger.error(f"Erreur dans population_par_age: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la population par âge'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def population_par_sexe(self, request):
        """Analyse de la population par sexe"""
        try:
            queryset = self.get_queryset()
            total = queryset.count()
            
            if total == 0:
                return Response({'data': [], 'total': 0})
            
            # Calcul optimisé avec annotation SQL
            data = queryset.values('sexe').annotate(
                effectif=Count('id'),
                pourcentage=Count('id') * 100.0 / total
            ).order_by('sexe')
            
            return Response({
                'data': list(data),
                'total': total
            })
            
        except Exception as e:
            logger.error(f"Erreur dans population_par_sexe: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la population par sexe'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def population_age_sexe(self, request):
        """Tableau croisé âge/sexe"""
        try:
            data = self.get_queryset().values('age_quinquennal', 'sexe').annotate(
                effectif=Count('id')
            ).order_by('age_quinquennal', 'sexe')
            
            return Response({
                'data': list(data)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans population_age_sexe: {e}")
            return Response({
                'error': 'Erreur lors du calcul du tableau croisé âge/sexe',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def population_par_nationalite(self, request):
        """Analyse par nationalité"""
        try:
            data = self.get_queryset().values('nationalite').annotate(
                effectif=Count('id')
            ).order_by('nationalite')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            for item in data_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
            
            return Response({
                'data': data_list,
                'total': total
            })
            
        except Exception as e:
            logger.error(f"Erreur dans population_par_nationalite: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la population par nationalité',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def femmes_selon_nationalite(self, request):
        """Femmes âgées de 15 ans et plus selon la nationalité"""
        try:
            data = self.get_queryset().filter(
                sexe=2, 
                age_simple__gte=15
            ).values('nationalite').annotate(
                effectif=Count('id')
            ).order_by('nationalite')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            for item in data_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
            
            return Response({
                'data': data_list,
                'total': total
            })
            
        except Exception as e:
            logger.error(f"Erreur dans femmes_selon_nationalite: {e}")
            return Response({
                'error': 'Erreur lors du calcul des femmes selon nationalité',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
    @action(detail=False, methods=['get'])
    def etat_matrimonial(self, request):
        """Analyses de l'état matrimonial par âge et sexe"""
        try:
            
            etat_matrimonial_filter = request.GET.get('etat_matrimonial', '1')
            
            etat_matrimonial_mapping = {
                '1': 'Célibataire',
                '2': 'Marié',
                '3': 'Divorcé',
                '4': 'Veuf',
                '9': 'Non déterminé'
            }
            
           
            age_quinquennal_mapping = {
                15: '15-19',
                20: '20-24', 
                25: '25-29',
                30: '30-34',
                35: '35-39',
                40: '40-44',
                45: '45-49',
                50: '50-54',
                55: '55-59',
                60: '60-64',
                65: '65-69',
                70: '70-74',
                75: '75+'
            }
         
            if etat_matrimonial_filter == 'all':
                etat_matrimonial_values = [1, 2, 3, 4, 9]
            else:
                etat_matrimonial_values = [int(x.strip()) for x in etat_matrimonial_filter.split(',')]
            
           
            valid_age_groups = list(age_quinquennal_mapping.keys())
            
          
            donnees_par_age = self.get_queryset().filter(
                etat_matrimonial__in=etat_matrimonial_values,
                sexe__in=[1, 2],  
                age_quinquennal__in=valid_age_groups  
            ).values('age_quinquennal', 'sexe').annotate(
                effectif=Count('id')
            ).order_by('age_quinquennal', 'sexe')
            
            
            logger.info(f"Filtres appliqués - États: {etat_matrimonial_values}")
            logger.info(f"Groupes d'âge: {valid_age_groups}")
            logger.info(f"Nombre d'enregistrements trouvés: {len(donnees_par_age)}")
            
           
            complete_data = []
            
          
            data_dict = {}
            for item in donnees_par_age:
                key = (item['age_quinquennal'], item['sexe'])
                data_dict[key] = item['effectif']
               
                logger.debug(f"Age {item['age_quinquennal']}, Sexe {item['sexe']}: {item['effectif']}")
            
            # Créer la structure complète avec les bons codes d'âge
            for age_group in valid_age_groups:
                for sexe in [1, 2]:
                    effectif = data_dict.get((age_group, sexe), 0)
                    complete_data.append({
                        'age_quinquennal': age_group,
                        'age_libelle': age_quinquennal_mapping[age_group],
                        'sexe': sexe,
                        'effectif': effectif
                    })
            
           
            total_filtered = self.get_queryset().filter(
                age_quinquennal__in=valid_age_groups, 
                etat_matrimonial__in=etat_matrimonial_values,
                sexe__in=[1, 2]
            ).count()
            
            hommes_filtered = self.get_queryset().filter(
                age_quinquennal__in=valid_age_groups,  
                etat_matrimonial__in=etat_matrimonial_values,
                sexe=1
            ).count()
            
            femmes_filtered = self.get_queryset().filter(
                age_quinquennal__in=valid_age_groups, 
                etat_matrimonial__in=etat_matrimonial_values,
                sexe=2
            ).count()
            
           
            logger.info(f"Statistiques - Total: {total_filtered}, H: {hommes_filtered}, F: {femmes_filtered}")
            
            return Response({
                'donnees_par_age': complete_data,
                'statistiques': {
                    'total_filtered': total_filtered,
                    'hommes_filtered': hommes_filtered,
                    'femmes_filtered': femmes_filtered,
                },
                'etat_matrimonial_mapping': etat_matrimonial_mapping,
                'age_quinquennal_mapping': age_quinquennal_mapping,
                'filter_applied': etat_matrimonial_values,
              
                'debug_info': {
                    'raw_data_count': len(donnees_par_age),
                    'age_groups_used': valid_age_groups
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans etat_matrimonial: {e}")
            return Response({
                'error': 'Erreur lors du calcul de l\'état matrimonial',
                'details': str(e)
            }, status=500)
    
    
    @action(detail=False, methods=['get'])
    def handicap_stats(self, request):
        """Analyses du handicap"""
        try:
            # Création de la variable handicap au niveau de la requête
            queryset = self.get_queryset().annotate(
                handicap=Case(
                    When(
                        Q(handicap_vision__gt=1) |
                        Q(handicap_audition__gt=1) |
                        Q(handicap_mobilite__gt=1) |
                        Q(handicap_memoire__gt=1) |
                        Q(handicap_entretien__gt=1) |
                        Q(handicap_communication__gt=1),
                        then=1
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
            
            # Taux de prévalence du handicap selon le sexe et le milieu
            data = queryset.values('milieu', 'sexe', 'handicap').annotate(
                effectif=Count('id')
            ).order_by('milieu', 'sexe', 'handicap')
            
            return Response({
                'data': list(data)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans handicap_stats: {e}")
            return Response({
                'error': 'Erreur lors du calcul des statistiques de handicap',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def statistiques_generales(self, request):
        """Statistiques générales de la population"""
        try:
            queryset = self.get_queryset()
            
            # Une seule requête pour les statistiques de base
            stats = queryset.aggregate(
                total_population=Count('id'),
                hommes=Count('id', filter=Q(sexe=1)),
                femmes=Count('id', filter=Q(sexe=2)),
                urbain=Count('id', filter=Q(milieu=1)),
                rural=Count('id', filter=Q(milieu=2)),
                marocains=Count('id', filter=Q(nationalite=1)),
                etrangers=Count('id', filter=~Q(nationalite=1)),
                age_moyen=Avg('age_simple')
            )
            
            total_population = stats['total_population']
            
            if total_population == 0:
                return Response({
                    'error': 'Aucune donnée disponible pour les filtres sélectionnés'
                }, status=status.HTTP_404_NOT_FOUND)
            
            return Response({
                'total_population': total_population,
                'repartition_sexe': {
                    'hommes': stats['hommes'],
                    'femmes': stats['femmes'],
                    'pourcentage_hommes': round((stats['hommes'] / total_population) * 100, 2),
                    'pourcentage_femmes': round((stats['femmes'] / total_population) * 100, 2)
                },
                'repartition_milieu': {
                    'urbain': stats['urbain'],
                    'rural': stats['rural'],
                    'pourcentage_urbain': round((stats['urbain'] / total_population) * 100, 2),
                    'pourcentage_rural': round((stats['rural'] / total_population) * 100, 2)
                },
                'age_moyen': round(stats['age_moyen'] or 0, 2),
                'nationalite': {
                    'marocains': stats['marocains'],
                    'etrangers': stats['etrangers'],
                    'pourcentage_marocains': round((stats['marocains'] / total_population) * 100, 2),
                    'pourcentage_etrangers': round((stats['etrangers'] / total_population) * 100, 2)
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans statistiques_generales: {e}")
            return Response({
                'error': 'Erreur lors du calcul des statistiques générales'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def niveau_education(self, request):
        """Analyse du niveau d'éducation de la population"""
        try:
            queryset = self.get_queryset()
            
            # Filtre pour les personnes de 10 ans et plus (âge scolaire)
            queryset = queryset.filter(age_simple__gte=10)
            
           
            data = queryset.values('niveau_etudes_agrege').annotate(
                effectif=Count('id')
            ).order_by('niveau_etudes_agrege')

            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            # Mapping des codes NIV.ET.AGR
            niveau_labels = {
                0: "Aucun niveau d'études",
                1: "Préscolaire",
                2: "Primaire", 
                3: "Secondaire collégial",
                4: "Secondaire qualifiant",
                5: "Supérieur"
            }
            
            # Calcul des pourcentages
            for item in data_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                
                item['niveau_label'] = niveau_labels.get(item['niveau_etudes_agrege'], f"Code {item['niveau_etudes_agrege']}")
            
            return Response({
                'data': data_list,
                'total': total,
                'note': 'Population de 10 ans et plus'
            })
            
        except Exception as e:
            logger.error(f"Erreur dans niveau_education: {e}")
            return Response({
                'error': 'Erreur lors du calcul du niveau d\'éducation',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def get_statut_professionnel_label(statut_professionnel):
        """Retourne le libellé du statut professionnel basé sur STAT.PROF"""
        if statut_professionnel is None:
            return "Non renseigné"
        
        labels = {
            1: "Employeur / Membre d'une coopérative",
            2: "Indépendant",
            3: "Aide familial / Apprenti",
            4: "Salarié du secteur public",
            5: "Salarié du secteur privé",
            6: "Autre",
            96: "Non déterminé",
            97: "Type d'activité non déterminé",
            98: "Chômeur n'ayant jamais travaillé",
            99: "Inactif"
        }
        
        return labels.get(statut_professionnel, f"Code {statut_professionnel}")

    
    def get_profession_generale_label(profession_code):
        """Retourne le libellé de la profession générale basé sur PROF.GG"""
        if profession_code is None:
            return "Non renseigné"
        
        labels = {
            0: "Membres des corps législatifs, élus locaux, responsables hiérarchiques de la fonction publique et directeurs et cadres",
            1: "Cadres supérieurs et membres des professions libérales",
            2: "Techniciens et professions intermédiaires",
            3: "Employés",
            4: "Commerçants et intermédiaires commerciaux et financiers",
            5: "Exploitants agricoles, pêcheurs de poissons et d'autres espèces aquatiques, forestiers, chasseurs et travailleurs assimilés",
            6: "Artisans et ouvriers qualifiés des métiers artisanaux (sauf ouvriers de l'agriculture)",
            7: "Ouvriers et manœuvres agricoles et de la pêche (y compris ouvriers qualifiés)",
            8: "Conducteurs d'installations et de machines et ouvriers de l'assemblage",
            9: "Manœuvres non agricoles, manutentionnaires et travailleurs des petits métiers",
            96: "Travailleurs ne pouvant être classés selon la profession",
            97: "Type d'activité non déterminé",
            98: "Chômeur n'ayant jamais travaillé",
            99: "Inactif"
        }
        
        return labels.get(profession_code, f"Code {profession_code}")

    @action(detail=False, methods=['get'])
    def statut_professionnel(self, request):
        """Analyse du statut professionnel"""
        try:
            queryset = self.get_queryset()
            
            # Filtre pour les personnes actives occupées (TY.ACT = 0)
            queryset = queryset.filter(type_activite=0)
            
            # Agrégation par statut professionnel (STAT.PROF)
            data = queryset.values('statut_professionnel').annotate(
                effectif=Count('id')
            ).order_by('statut_professionnel')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            # Calcul des pourcentages et ajout des libellés
            for item in data_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                item['statut_label'] = get_statut_professionnel_label(item['statut_professionnel'])
            
            return Response({
                'data': data_list,
                'total': total,
                'note': 'Population active occupée'
            })
            
        except Exception as e:
            logger.error(f"Erreur dans statut_professionnel: {e}")
            return Response({
                'error': 'Erreur lors du calcul du statut professionnel',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # 5. Ajout d'une API pour les aptitudes de lecture/écriture
    @action(detail=False, methods=['get'])
    def aptitude_lecture_ecriture(self, request):
        """Analyse des aptitudes à lire et écrire"""
        try:
            queryset = self.get_queryset().filter(
                age_simple__gte=10,
                aptitude_lecture_ecriture__isnull=False
            )
            
            data = queryset.values('aptitude_lecture_ecriture').annotate(
                effectif=Count('id')
            ).order_by('aptitude_lecture_ecriture')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            # Mapping des codes d'aptitude lecture/écriture
            aptitude_labels = {
                1: "Alphabète",
                2: "Analphabète",
                7: "Non déterminée",
                8: "Personne de moins de 10 ans",
                9: "Âge non déterminé"
            }
            
            # Calcul des pourcentages et ajout des libellés
            for item in data_list:
                if total > 0:
                    item['pourcentage'] = round((item['effectif'] / total) * 100, 2)
                else:
                    item['pourcentage'] = 0
                    
                aptitude_code = item['aptitude_lecture_ecriture']
                item['aptitude_label'] = aptitude_labels.get(
                    aptitude_code, 
                    f"Code non défini ({aptitude_code})"
                )
            
            return Response({
                'data': data_list,
                'total': total,
                'note': 'Population de 10 ans et plus'
            })
            
        except Exception as e:
            logger.error(f"Erreur dans aptitude_lecture_ecriture: {e}")
            logger.error(f"Type d'erreur: {type(e)}")
            return Response({
                'error': 'Erreur lors du calcul des aptitudes de lecture/écriture',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
  
    @action(detail=False, methods=['get'])
    
    def niveau_education_par_milieu(self, request):
        """Niveau d'éducation par milieu de résidence"""
        try:
            queryset = self.get_queryset().filter(
                age_simple__gte=10,
                niveau_etudes__isnull=False,
                milieu__isnull=False
            )
            
            
            data = queryset.values('niveau_etudes_agrege', 'milieu').annotate(
                effectif=Count('id')
            ).order_by('niveau_etudes_agrege', 'milieu')

            data_list = list(data)
            
            # Mapping des niveaux d'éducation
            niveau_labels = {
                0: "Aucun niveau d'études",
                1: "Préscolaire",
                2: "Primaire",
                3: "Secondaire collégial", 
                4: "Secondaire qualifiant",
                5: "Supérieur"
            }
            
            # Enrichissement avec les libellés
            for item in data_list:
                item['niveau_label'] = niveau_labels.get(
                    item['niveau_etudes_agrege'], 
                    f"Code non défini ({item['niveau_etudes_agrege']})"
                )
                
                # Gestion robuste du milieu
                if item['milieu'] == 1:
                    item['milieu_label'] = 'Urbain'
                elif item['milieu'] == 2:
                    item['milieu_label'] = 'Rural'
                else:
                    item['milieu_label'] = f'Milieu non défini ({item["milieu"]})'
            
            return Response({
                'niveau_par_milieu': data_list,
                'total_enregistrements': len(data_list)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans niveau_education_par_milieu: {e}")
            logger.error(f"Type d'erreur: {type(e)}")
            return Response({
                'error': 'Erreur lors du calcul du niveau d\'éducation par milieu',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   
    @action(detail=False, methods=['get'])
    def population_scolarisee(self, request):
        """Population scolarisée par âge et sexe"""
        try:
            queryset = self.get_queryset().filter(
                age_simple__gte=4,  # Âge préscolaire
                age_simple__lte=24,  # Âge universitaire
                scolarisation__isnull=False,
                sexe__isnull=False
            )
            
            # Utiliser 'scolarisation' qui existe dans le modèle
            data = queryset.values('age_simple', 'sexe', 'scolarisation').annotate(
                effectif=Count('id')
            ).order_by('age_simple', 'sexe')
            
            # Mapping des codes de scolarisation
            scolarisation_labels = {
                1: "Scolarisé dans l'enseignement général (achevé)",
                2: "Scolarisé dans l'enseignement général (non achevé)",
                3: "Scolarisé dans la formation professionnelle (achevé)",
                4: "Scolarisé dans la formation professionnelle (non achevé)",
                5: "Non scolarisé",
                6: "Non déterminée",
                7: "Personne de moins de 3 ans",
                8: "Personne de 49 ans ou plus",
                9: "Âge non déterminé"
            }
            
            data_list = list(data)
            for item in data_list:
                item['scolarisation_label'] = scolarisation_labels.get(
                    item['scolarisation'], 
                    f"Code non défini ({item['scolarisation']})"
                )
                
                # Gestion robuste du sexe
                if item['sexe'] == 1:
                    item['sexe_label'] = 'Masculin'
                elif item['sexe'] == 2:
                    item['sexe_label'] = 'Féminin'
                else:
                    item['sexe_label'] = f'Sexe non défini ({item["sexe"]})'
            
            return Response({
                'data': data_list,
                'total_enregistrements': len(data_list)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans population_scolarisee: {e}")
            logger.error(f"Type d'erreur: {type(e)}")
            return Response({
                'error': 'Erreur lors du calcul de la population scolarisée',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def pyramide_ages(self, request):
        """Pyramide des âges par sexe"""
        try:
            queryset = self.get_queryset()
            
            # Données pour la pyramide des âges
            data = queryset.values('age_quinquennal', 'sexe').annotate(
                effectif=Count('id')
            ).order_by('age_quinquennal', 'sexe')
            
            # Restructurer les données pour faciliter la création de la pyramide
            pyramid_data = {}
            for item in data:
                age_group = item['age_quinquennal']
                sexe = item['sexe']
                effectif = item['effectif']
                
                if age_group not in pyramid_data:
                    pyramid_data[age_group] = {'hommes': 0, 'femmes': 0}
                
                if sexe == 1:  # Hommes
                    pyramid_data[age_group]['hommes'] = effectif
                elif sexe == 2:  # Femmes
                    pyramid_data[age_group]['femmes'] = effectif
            
            # Convertir en liste ordonnée
            pyramid_list = []
            for age_group in sorted(pyramid_data.keys()):
                pyramid_list.append({
                    'age_group': age_group,
                    'hommes': pyramid_data[age_group]['hommes'],
                    'femmes': pyramid_data[age_group]['femmes']
                })
            
            return Response({
                'data': pyramid_list,
                'total': queryset.count()
            })
            
        except Exception as e:
            logger.error(f"Erreur dans pyramide_ages: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la pyramide des âges'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def repartition_geographique(self, request):
        """Répartition géographique par région et province"""
        try:
            queryset = self.get_queryset()
            
            # Données par région
            regions_data = queryset.values('region').annotate(
                effectif=Count('id')
            ).order_by('region')
            
            # Données par région et province
            provinces_data = queryset.values('region', 'province').annotate(
                effectif=Count('id')
            ).order_by('region', 'province')
            
            # Calcul des totaux
            total = queryset.count()
            
            # Ajout des pourcentages
            regions_list = list(regions_data)
            for item in regions_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
            
            provinces_list = list(provinces_data)
            for item in provinces_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
            
            return Response({
                'regions': regions_list,
                'provinces': provinces_list,
                'total': total
            })
            
        except Exception as e:
            logger.error(f"Erreur dans repartition_geographique: {e}")
            return Response({
                'error': 'Erreur lors du calcul de la répartition géographique'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def analyse_croisee_sexe_age(self, request):
        """Analyse croisée sexe-âge avec détails"""
        try:
            queryset = self.get_queryset()
            
            # Données croisées par sexe et âge quinquennal
            data = queryset.values('sexe', 'age_quinquennal').annotate(
                effectif=Count('id')
            ).order_by('sexe', 'age_quinquennal')
            
            # Statistiques par sexe
            stats_sexe = queryset.values('sexe').annotate(
                effectif=Count('id'),
                age_moyen=Avg('age_simple')
            ).order_by('sexe')
            
            return Response({
                'croises': list(data),
                'stats_par_sexe': list(stats_sexe),
                'total': queryset.count()
            })
            
        except Exception as e:
            logger.error(f"Erreur dans analyse_croisee_sexe_age: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse croisée sexe-âge'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def debug_champs_disponibles(self, request):
        """Fonction de débogage pour vérifier les champs disponibles"""
        try:
            queryset = self.get_queryset()
            
            # Vérifier les champs du modèle
            champs_modele = [field.name for field in queryset.model._meta.get_fields()]
            
            # Vérifier quelques valeurs distinctes pour les champs d'éducation
            niveau_etudes_valeurs = list(queryset.values_list('niveau_etudes', flat=True).distinct()[:10])
            aptitude_valeurs = list(queryset.values_list('aptitude_lecture_ecriture', flat=True).distinct()[:10])
            scolarisation_valeurs = list(queryset.values_list('scolarisation', flat=True).distinct()[:10])
            
            return Response({
                'champs_modele': champs_modele,
                'echantillon_niveau_etudes': niveau_etudes_valeurs,
                'echantillon_aptitude_lecture_ecriture': aptitude_valeurs,
                'echantillon_scolarisation': scolarisation_valeurs,
                'total_enregistrements': queryset.count()
            })
            
        except Exception as e:
            logger.error(f"Erreur dans debug_champs_disponibles: {e}")
            return Response({
                'error': 'Erreur lors du débogage',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['get'])
    def taux_scolarisation(self, request):
        """Taux de scolarisation par âge, sexe et milieu"""
        try:
            queryset = self.get_queryset().filter(
                age_simple__gte=4,
                age_simple__lte=24,
                scolarisation__isnull=False
            )
            
        
            scolarises_filter = Q(scolarisation__in=[1, 2, 3, 4])
            
            # Taux par âge
            taux_age = queryset.values('age_simple').annotate(
                total=Count('id'),
                scolarises=Count('id', filter=scolarises_filter)
            ).order_by('age_simple')
            
            # Taux par sexe (filtrer les valeurs NULL)
            taux_sexe = queryset.filter(sexe__isnull=False).values('sexe').annotate(
                total=Count('id'),
                scolarises=Count('id', filter=scolarises_filter)
            ).order_by('sexe')
            
            # Taux par milieu (filtrer les valeurs NULL)
            taux_milieu = queryset.filter(milieu__isnull=False).values('milieu').annotate(
                total=Count('id'),
                scolarises=Count('id', filter=scolarises_filter)
            ).order_by('milieu')
            
            # Calcul des pourcentages avec protection contre division par zéro
            for dataset in [taux_age, taux_sexe, taux_milieu]:
                for item in dataset:
                    if item['total'] > 0:
                        item['taux_scolarisation'] = round(
                            (item['scolarises'] / item['total']) * 100, 2
                        )
                    else:
                        item['taux_scolarisation'] = 0
            
            # Ajout des libellés avec gestion d'erreur
            for item in taux_sexe:
                if item['sexe'] == 1:
                    item['sexe_label'] = 'Masculin'
                elif item['sexe'] == 2:
                    item['sexe_label'] = 'Féminin'
                else:
                    item['sexe_label'] = f'Sexe non défini ({item["sexe"]})'
                
            for item in taux_milieu:
                if item['milieu'] == 1:
                    item['milieu_label'] = 'Urbain'
                elif item['milieu'] == 2:
                    item['milieu_label'] = 'Rural'
                else:
                    item['milieu_label'] = f'Milieu non défini ({item["milieu"]})'
            
            return Response({
                'par_age': list(taux_age),
                'par_sexe': list(taux_sexe),
                'par_milieu': list(taux_milieu),
                'note': 'Population de 4-24 ans'
            })
            
        except Exception as e:
            logger.error(f"Erreur dans taux_scolarisation: {e}")
            logger.error(f"Type d'erreur: {type(e)}")
            return Response({
                'error': 'Erreur lors du calcul des taux de scolarisation',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def secteur_enseignement(self, request):
        """Répartition par secteur d'enseignement (public vs privé)"""
        try:
            queryset = self.get_queryset().filter(scolarisation=1)
            
            data = queryset.values('secteur_enseignement').annotate(
                effectif=Count('id')
            ).order_by('secteur_enseignement')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            # Libellés pour les secteurs
            secteur_labels = {
                1: "Public",
                2: "Privé",
                3: "Autre",
                None: "Non renseigné"
            }
            
            for item in data_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                secteur = item['secteur_enseignement']
                item['secteur_label'] = secteur_labels.get(secteur, f"Code {secteur}")
            
            return Response({
                'data': data_list,
                'total': total
            })
            
        except Exception as e:
            logger.error(f"Erreur dans secteur_enseignement: {e}")
            return Response({
                'error': 'Erreur lors du calcul du secteur d\'enseignement'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def langues_analysis(self, request):
        """Analyse des langues parlées"""
        try:
            queryset = self.get_queryset()
            
            # Première langue
            langue1 = queryset.values('langue_1').annotate(
                effectif=Count('id')
            ).order_by('langue_1')
            
            # Deuxième langue
            langue2 = queryset.values('langue_2').annotate(
                effectif=Count('id')
            ).order_by('langue_2')
            
            # Troisième langue
            langue3 = queryset.values('langue_3').annotate(
                effectif=Count('id')
            ).order_by('langue_3')
            
            # Langues locales
            langue_locale1 = queryset.values('langue_locale_1').annotate(
                effectif=Count('id')
            ).order_by('langue_locale_1')
            
            langue_locale2 = queryset.values('langue_locale_2').annotate(
                effectif=Count('id')
            ).order_by('langue_locale_2')
            
            return Response({
                'premiere_langue': list(langue1),
                'deuxieme_langue': list(langue2),
                'troisieme_langue': list(langue3),
                'premiere_langue_locale': list(langue_locale1),
                'deuxieme_langue_locale': list(langue_locale2)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans langues_analysis: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse des langues'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def multilinguisme(self, request):
        """Analyse du multilinguisme"""
        try:
            queryset = self.get_queryset()
            
            # Compter le nombre de langues par individu
            data = queryset.annotate(
                nb_langues=Case(
                    When(langue_1__isnull=False, langue_2__isnull=False, langue_3__isnull=False, then=3),
                    When(langue_1__isnull=False, langue_2__isnull=False, then=2),
                    When(langue_1__isnull=False, then=1),
                    default=0,
                    output_field=IntegerField()
                )
            ).values('nb_langues').annotate(
                effectif=Count('id')
            ).order_by('nb_langues')
            
            data_list = list(data)
            total = sum(item['effectif'] for item in data_list)
            
            # Ajout des pourcentages et libellés
            for item in data_list:
                item['pourcentage'] = round((item['effectif'] / total) * 100, 2) if total > 0 else 0
                nb = item['nb_langues']
                if nb == 0:
                    item['label'] = "Aucune langue"
                elif nb == 1:
                    item['label'] = "1 langue"
                else:
                    item['label'] = f"{nb} langues"
            
            return Response({
                'data': data_list,
                'total': total
            })
            
        except Exception as e:
            logger.error(f"Erreur dans multilinguisme: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse du multilinguisme'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def diplomes_analysis(self, request):
        """Analyse des diplômes"""
        try:
            queryset = self.get_queryset()
            
            # Diplômes supérieurs généraux
            diplome_sup_gen = queryset.values('diplome_superieur_general').annotate(
                effectif=Count('id')
            ).order_by('diplome_superieur_general')
            
            # Diplômes généraux
            diplome_gen = queryset.values('diplome_general').annotate(
                effectif=Count('id')
            ).order_by('diplome_general')
            
            # Diplômes de formation professionnelle
            diplome_fp_sup = queryset.values('diplome_formation_professionnelle_superieur').annotate(
                effectif=Count('id')
            ).order_by('diplome_formation_professionnelle_superieur')
            
            diplome_fp_gen = queryset.values('diplome_formation_professionnelle_general').annotate(
                effectif=Count('id')
            ).order_by('diplome_formation_professionnelle_general')
            
            diplome_fp_base = queryset.values('diplome_formation_professionnelle_base').annotate(
                effectif=Count('id')
            ).order_by('diplome_formation_professionnelle_base')
            
            return Response({
                'diplome_superieur_general': list(diplome_sup_gen),
                'diplome_general': list(diplome_gen),
                'diplome_fp_superieur': list(diplome_fp_sup),
                'diplome_fp_general': list(diplome_fp_gen),
                'diplome_fp_base': list(diplome_fp_base)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans diplomes_analysis: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse des diplômes'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def taux_diplomation(self, request):
        """Taux de diplomation par sexe et milieu"""
        try:
            queryset = self.get_queryset().filter(age_simple__gte=25)  # Adultes
            
            # Taux par sexe
            taux_sexe = queryset.values('sexe').annotate(
                total=Count('id'),
                diplomes=Count('id', filter=Q(
                    Q(diplome_superieur_general__isnull=False) |
                    Q(diplome_general__isnull=False) |
                    Q(diplome_formation_professionnelle_superieur__isnull=False)
                ))
            ).order_by('sexe')
            
            # Taux par milieu
            taux_milieu = queryset.values('milieu').annotate(
                total=Count('id'),
                diplomes=Count('id', filter=Q(
                    Q(diplome_superieur_general__isnull=False) |
                    Q(diplome_general__isnull=False) |
                    Q(diplome_formation_professionnelle_superieur__isnull=False)
                ))
            ).order_by('milieu')
            
            # Calcul des pourcentages
            for dataset in [taux_sexe, taux_milieu]:
                for item in dataset:
                    item['taux_diplomation'] = round(
                        (item['diplomes'] / item['total']) * 100, 2
                    ) if item['total'] > 0 else 0
            
            return Response({
                'par_sexe': list(taux_sexe),
                'par_milieu': list(taux_milieu)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans taux_diplomation: {e}")
            return Response({
                'error': 'Erreur lors du calcul des taux de diplomation'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def professions_analysis(self, request):
        """Analyse des professions"""
        try:
            queryset = self.get_queryset().filter(type_activite=0)  # Actifs occupés (TY.ACT = 0)
            
            # Professions détaillées (PROF.SGG)
            prof_detaille = queryset.values('profession_sgg').annotate(
                effectif=Count('id')
            ).order_by('profession_sgg')
            
            # Professions générales (PROF.GG)
            prof_generale = queryset.values('profession_gg').annotate(
                effectif=Count('id')
            ).order_by('profession_gg')
            
            # Ajout des libellés pour les professions générales
            prof_generale_list = list(prof_generale)
            for item in prof_generale_list:
                item['profession_label'] = get_profession_generale_label(item['profession_gg'])
            
            return Response({
                'professions_detaillees': list(prof_detaille),
                'professions_generales': prof_generale_list,
                'total_actifs': queryset.count()
            })
            
        except Exception as e:
            logger.error(f"Erreur dans professions_analysis: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse des professions'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    


    @action(detail=False, methods=['get'])
    def taux_activite(self, request):
        """Taux d'activité par âge, sexe et éducation"""
        try:
            queryset = self.get_queryset().filter(age_simple__gte=15)
            
            # Taux par âge
            taux_age = queryset.values('age_quinquennal').annotate(
                total=Count('id'),
                actifs=Count('id', filter=Q(type_activite=0))  # TY.ACT = 0 pour actifs occupés
            ).order_by('age_quinquennal')
            
            # Taux par sexe
            taux_sexe = queryset.values('sexe').annotate(
                total=Count('id'),
                actifs=Count('id', filter=Q(type_activite=0))  # TY.ACT = 0 pour actifs occupés
            ).order_by('sexe')
            
            # Taux par niveau d'éducation
            taux_education = queryset.values('niveau_etudes').annotate(
                total=Count('id'),
                actifs=Count('id', filter=Q(type_activite=0))  # TY.ACT = 0 pour actifs occupés
            ).order_by('niveau_etudes_agrege')
            
            # Calcul des pourcentages
            for dataset in [taux_age, taux_sexe, taux_education]:
                for item in dataset:
                    item['taux_activite'] = round(
                        (item['actifs'] / item['total']) * 100, 2
                    ) if item['total'] > 0 else 0
            
            return Response({
                'par_age': list(taux_age),
                'par_sexe': list(taux_sexe),
                'par_education': list(taux_education)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans taux_activite: {e}")
            return Response({
                'error': 'Erreur lors du calcul des taux d\'activité'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def taux_chomage(self, request):
        """Calcul du taux de chômage"""
        try:
            queryset = self.get_queryset().filter(age_quinquennal__gte=15)

            # Population active = actifs occupés + chômeurs
            population_active = queryset.filter(
                type_activite__in=[0, 1, 2]  # Actifs occupés + chômeurs
            )
            
            # Chômeurs uniquement
            chomeurs = queryset.filter(
                type_activite__in=[1, 2]  # Chômeurs n'ayant jamais travaillé + ayant déjà travaillé
            )
            
            # Calcul global
            total_actifs = population_active.count()
            total_chomeurs = chomeurs.count()
            
            taux_chomage_global = round(
                (total_chomeurs / total_actifs) * 100, 2
            ) if total_actifs > 0 else 0
            
            # Taux par sexe
            taux_par_sexe = population_active.values('sexe').annotate(
                actifs=Count('id'),
                chomeurs=Count('id', filter=Q(type_activite__in=[1, 2]))
            ).order_by('sexe')
            
            for item in taux_par_sexe:
                item['taux_chomage'] = round(
                    (item['chomeurs'] / item['actifs']) * 100, 2
                ) if item['actifs'] > 0 else 0
            
            return Response({
                'taux_chomage_global': taux_chomage_global,
                'total_actifs': total_actifs,
                'total_chomeurs': total_chomeurs,
                'par_sexe': list(taux_par_sexe)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans taux_chomage: {e}")
            return Response({
                'error': 'Erreur lors du calcul du taux de chômage'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def lieu_travail_transport(self, request):
        """Analyse du lieu de travail et transport"""
        try:
            queryset = self.get_queryset().filter(type_activite=1)  # Actifs occupés
            
            # Lieu de travail
            lieu_travail = queryset.values('lieu_travail').annotate(
                effectif=Count('id')
            ).order_by('lieu_travail')
            
            # Mode de transport
            transport = queryset.values('mode_transport_travail').annotate(
                effectif=Count('id')
            ).order_by('mode_transport_travail')
            
            return Response({
                'lieu_travail': list(lieu_travail),
                'transport_travail': list(transport)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans lieu_travail_transport: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse du lieu de travail et transport'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @action(detail=False, methods=['get'])
    def types_handicap(self, request):
        """Analyse détaillée des types de handicap"""
        try:
            queryset = self.get_queryset()
            
            # Handicap par type
            handicap_vision = queryset.values('handicap_vision').annotate(
                effectif=Count('id')
            ).order_by('handicap_vision')
            
            handicap_audition = queryset.values('handicap_audition').annotate(
                effectif=Count('id')
            ).order_by('handicap_audition')
            
            handicap_mobilite = queryset.values('handicap_mobilite').annotate(
                effectif=Count('id')
            ).order_by('handicap_mobilite')
            
            handicap_memoire = queryset.values('handicap_memoire').annotate(
                effectif=Count('id')
            ).order_by('handicap_memoire')
            
            handicap_entretien = queryset.values('handicap_entretien').annotate(
                effectif=Count('id')
            ).order_by('handicap_entretien')
            
            handicap_communication = queryset.values('handicap_communication').annotate(
                effectif=Count('id')
            ).order_by('handicap_communication')
            
            return Response({
                'handicap_vision': list(handicap_vision),
                'handicap_audition': list(handicap_audition),
                'handicap_mobilite': list(handicap_mobilite),
                'handicap_memoire': list(handicap_memoire),
                'handicap_entretien': list(handicap_entretien),
                'handicap_communication': list(handicap_communication)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans types_handicap: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse des types de handicap'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def handicap_par_age_sexe(self, request):
        """Handicap par âge et sexe"""
        try:
            queryset = self.get_queryset().annotate(
                handicap=Case(
                    When(
                        Q(handicap_vision__gt=1) |
                        Q(handicap_audition__gt=1) |
                        Q(handicap_mobilite__gt=1) |
                        Q(handicap_memoire__gt=1) |
                        Q(handicap_entretien__gt=1) |
                        Q(handicap_communication__gt=1),
                        then=1
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
            
            # Par âge
            par_age = queryset.values('age_quinquennal', 'handicap').annotate(
                effectif=Count('id')
            ).order_by('age_quinquennal', 'handicap')
            
            # Par sexe
            par_sexe = queryset.values('sexe', 'handicap').annotate(
                effectif=Count('id')
            ).order_by('sexe', 'handicap')
            
            return Response({
                'par_age': list(par_age),
                'par_sexe': list(par_sexe)
            })
            
        except Exception as e:
            logger.error(f"Erreur dans handicap_par_age_sexe: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse du handicap par âge et sexe'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def fecondite_analysis(self, request):
       
        try:
            # Filtrer les femmes en âge de procréer (15-49 ans)
            # Utiliser age_quinquennal pour cohérence avec le groupement
            queryset = self.get_queryset().filter(
                sexe=2,  # Femmes
                age_quinquennal__gte=15,  # 15-19 ans
                age_quinquennal__lte=45   # 45-49 ans (dernière tranche fertile)
            ).exclude(
                # Exclure les codes spéciaux pour les variables de fécondité
                Q(enfants_vivants__in=[96, 97, 98, 99]) |
                Q(enfants_decedes__in=[96, 97, 98, 99]) |
                Q(age_quinquennal=99)  # Exclure âge non déterminé
            )
            
            # Enfants vivants (ENF.VIV)
            enfants_vivants = queryset.values('enfants_vivants').annotate(
                effectif=Count('id')
            ).order_by('enfants_vivants')
            
            # Enfants décédés (ENF.DEC)
            enfants_decedes = queryset.values('enfants_decedes').annotate(
                effectif=Count('id')
            ).order_by('enfants_decedes')
            
            # Naissances récentes (ENF.VIV.12M)
            # Attention: cette variable a des codes différents (95-99)
            naissances_12m = queryset.exclude(
                naissances_vivantes_12m__in=[95, 96, 97, 98, 99]
            ).values('naissances_vivantes_12m').annotate(
                effectif=Count('id')
            ).order_by('naissances_vivantes_12m')
            
            # Décès récents (ENF.DEC.12M)
            deces_12m = queryset.exclude(
                deces_12m__in=[95, 96, 97, 98, 99]
            ).values('deces_12m').annotate(
                effectif=Count('id')
            ).order_by('deces_12m')
            
            # Moyennes par âge quinquennal (filtrer seulement les tranches d'âge de procréation)
            moyennes_age = queryset.exclude(
                Q(enfants_vivants__in=[96, 97, 98, 99]) |
                Q(enfants_decedes__in=[96, 97, 98, 99]) |
                Q(age_quinquennal=99)
            ).filter(
                age_quinquennal__in=[15, 20, 25, 30, 35, 40, 45]  # Tranches d'âge de procréation
            ).values('age_quinquennal').annotate(
                moyenne_enfants_vivants=Avg('enfants_vivants'),
                moyenne_enfants_decedes=Avg('enfants_decedes'),
                effectif=Count('id')
            ).order_by('age_quinquennal')
            
            # Indicateurs de fécondité - Statistiques générales
            stats_generales = queryset.exclude(
                Q(enfants_vivants__in=[96, 97, 98, 99]) |
                Q(enfants_decedes__in=[96, 97, 98, 99])
            ).aggregate(
                nombre_moyen_enfants_vivants=Avg('enfants_vivants'),
                nombre_moyen_enfants_decedes=Avg('enfants_decedes'),
                total_femmes=Count('id')
            )
            
            # Fonction pour générer les labels des enfants
            def get_label_enfants(code):
                labels = {
                    0: "Aucun enfant",
                    1: "1 enfant", 
                    2: "2 enfants", 
                    3: "3 enfants", 
                    4: "4 enfants",
                    5: "5 enfants", 
                    6: "6 enfants", 
                    7: "7 enfants", 
                    8: "8 enfants",
                    9: "9 enfants", 
                    10: "10 enfants et plus",
                    96: "Non déterminé",
                    97: "Femme dont l'état matrimonial est non déterminé",
                    98: "Femme célibataire",
                    99: "Homme"
                }
                return labels.get(code, f"Code {code}")
            
            # Ajouter les labels aux résultats - Enfants vivants
            enfants_vivants_avec_labels = []
            for item in enfants_vivants:
                enfants_vivants_avec_labels.append({
                    'code': item['enfants_vivants'],
                    'label': get_label_enfants(item['enfants_vivants']),
                    'effectif': item['effectif']
                })
            
            # Ajouter les labels aux résultats - Enfants décédés
            enfants_decedes_avec_labels = []
            for item in enfants_decedes:
                enfants_decedes_avec_labels.append({
                    'code': item['enfants_decedes'],
                    'label': get_label_enfants(item['enfants_decedes']),
                    'effectif': item['effectif']
                })
            
            # Calcul du taux de fécondité par groupe d'âge quinquennal
            fecondite_par_age = []
            for age_group in moyennes_age:
                if age_group['effectif'] > 0:
                    fecondite_par_age.append({
                        'age_quinquennal': age_group['age_quinquennal'],
                        'moyenne_enfants_vivants': round(age_group['moyenne_enfants_vivants'], 2),
                        'moyenne_enfants_decedes': round(age_group['moyenne_enfants_decedes'], 2),
                        'effectif': age_group['effectif']
                    })
            
            # Calcul d'indicateurs démographiques additionnels
            taux_fecondite_total = 0
            if fecondite_par_age:
                # Approximation du TFT (Taux de Fécondité Total)
                # Somme des taux de fécondité par âge × 5 (largeur de l'intervalle)
                taux_fecondite_total = sum([group['moyenne_enfants_vivants'] for group in fecondite_par_age])
            
            # Calcul du taux de mortalité infantile global
            taux_mortalite_global = 0
            total_enfants_vivants = stats_generales['nombre_moyen_enfants_vivants'] or 0
            total_enfants_decedes = stats_generales['nombre_moyen_enfants_decedes'] or 0
            
            if total_enfants_vivants > 0:
                taux_mortalite_global = round((total_enfants_decedes / total_enfants_vivants) * 100, 2)
            
            return Response({
                'enfants_vivants': enfants_vivants_avec_labels,
                'enfants_decedes': enfants_decedes_avec_labels,
                'naissances_12m': list(naissances_12m),
                'deces_12m': list(deces_12m),
                'fecondite_par_age': fecondite_par_age,
                'statistiques_generales': {
                    'nombre_moyen_enfants_vivants': round(stats_generales['nombre_moyen_enfants_vivants'], 2) if stats_generales['nombre_moyen_enfants_vivants'] else 0,
                    'nombre_moyen_enfants_decedes': round(stats_generales['nombre_moyen_enfants_decedes'], 2) if stats_generales['nombre_moyen_enfants_decedes'] else 0,
                    'total_femmes_analysees': stats_generales['total_femmes'],
                    'taux_fecondite_total_approx': round(taux_fecondite_total, 2),
                    'taux_mortalite_infantile_global': taux_mortalite_global
                },
                'metadata': {
                    'population_analysee': 'Femmes en âge de procréer (15-49 ans)',
                    'tranches_age_incluses': [15, 20, 25, 30, 35, 40, 45],
                    'codes_exclus': {
                        'enfants_vivants_decedes': [96, 97, 98, 99],
                        'naissances_deces_12m': [95, 96, 97, 98, 99],
                        'age_quinquennal': [99]
                    }
                }
            })
            
        except Exception as e:
            logger.error(f"Erreur dans fecondite_analysis: {e}")
            return Response({
                'error': 'Erreur lors de l\'analyse de la fécondité',
                'details': str(e) if settings.DEBUG else None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class MetadataViewSet(viewsets.ViewSet):
    """API pour les métadonnées et filtres"""
    
    @action(detail=False, methods=['get'])
    def regions(self, request):
        """Liste des régions disponibles"""
        try:
            regions = Individu.objects.values_list('region', flat=True).distinct().order_by('region')
            return Response({'regions': list(regions)})
        except Exception as e:
            logger.error(f"Erreur dans regions: {e}")
            return Response({
                'error': 'Erreur lors de la récupération des régions',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def provinces(self, request):
        """Liste des provinces disponibles"""
        try:
            region = request.query_params.get('region', None)
            queryset = Individu.objects.all()

            if region:
                queryset = queryset.filter(region=region)
                
            provinces = queryset.values_list('province', flat=True).distinct().order_by('province')
            return Response({'provinces': list(provinces)})
        except Exception as e:
            logger.error(f"Erreur dans provinces: {e}")
            return Response({
                'error': 'Erreur lors de la récupération des provinces',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def milieux(self, request):
        """Liste des milieux disponibles"""
        try:
            milieux = Individu.objects.values_list('milieu', flat=True).distinct().order_by('milieu')
            return Response({'milieux': list(milieux)})
        except Exception as e:
            logger.error(f"Erreur dans milieux: {e}")
            return Response({
                'error': 'Erreur lors de la récupération des milieux',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def filtres_complets(self, request):
        """Tous les filtres disponibles"""
        try:
            return Response({
                'regions': list(Individu.objects.values_list('region', flat=True).distinct().order_by('region')),
                'provinces': list(Individu.objects.values_list('province', flat=True).distinct().order_by('province')),
                'milieux': list(Individu.objects.values_list('milieu', flat=True).distinct().order_by('milieu')),
                'sexes': [
                    {'value': 1, 'label': 'Masculin'},
                    {'value': 2, 'label': 'Féminin'}
                ],
                'etats_matrimoniaux': [
                    {'value': 1, 'label': 'Célibataire'},
                    {'value': 2, 'label': 'Marié(e)'},
                    {'value': 3, 'label': 'Divorcé(e)'},
                    {'value': 4, 'label': 'Veuf/Veuve'}
                ]
            })
        except Exception as e:
            logger.error(f"Erreur dans filtres_complets: {e}")
            return Response({
                'error': 'Erreur lors de la récupération des filtres',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#############################################################################

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg, Sum, Case, When, IntegerField, FloatField, Q
from django.db.models.functions import Cast
from .models import Menage
from .serializers import (
    TailleMenageSerializer, TailleCategorieSerializer, EquipementSerializer,
    EquipementCompletSerializer, DistanceRouteSerializer, ModeCuissonSerializer
)

@api_view(['GET'])
def taille_moyenne_menages(request):
    """
    Analyse de la taille moyenne des ménages par région et milieu
    """
    # Calcul de la taille moyenne par région et milieu
    resultats = (
        Menage.objects
        .values('region', 'milieu')
        .annotate(taille_moyenne=Avg('taille_menage'))
        .order_by('region', 'milieu')
    )
    
    # Enrichissement avec les labels
    data = []
    for resultat in resultats:
        region_label = dict(Menage.REGION_CHOICES).get(resultat['region'], 'Inconnu')
        milieu_label = dict(Menage.MILIEU_CHOICES).get(resultat['milieu'], 'Inconnu')
        
        data.append({
            'region': region_label,
            'milieu': milieu_label,
            'taille_moyenne': round(resultat['taille_moyenne'], 2)
        })
    
    serializer = TailleMenageSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def distribution_taille_categorisee(request):
    """
    Distribution des ménages par taille catégorisée et milieu
    """
    # Catégorisation de la taille des ménages
    resultats = (
        Menage.objects
        .annotate(
            taille_categorie=Case(
                When(taille_menage__range=(1, 3), then=1),
                When(taille_menage__range=(4, 6), then=2),
                When(taille_menage__range=(7, 9), then=3),
                default=4,
                output_field=IntegerField()
            )
        )
        .values('taille_categorie', 'milieu')
        .annotate(effectif=Count('id'))
        .order_by('taille_categorie', 'milieu')
    )
    
    # Enrichissement avec les labels
    data = []
    taille_labels = {
        1: '1-3 personnes',
        2: '4-6 personnes',
        3: '7-9 personnes',
        4: '10+ personnes'
    }
    
    for resultat in resultats:
        milieu_label = dict(Menage.MILIEU_CHOICES).get(resultat['milieu'], 'Inconnu')
        
        data.append({
            'taille_categorie': taille_labels.get(resultat['taille_categorie'], 'Inconnu'),
            'milieu': milieu_label,
            'effectif': resultat['effectif']
        })
    
    serializer = TailleCategorieSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def analyse_equipements_base(request):
    """
    Analyse des équipements de base des ménages
    """
    total_menages = Menage.objects.count()
    
    # Analyse de la cuisine
    cuisine_stats = (
        Menage.objects
        .aggregate(
            disponible=Count('id', filter=Q(cuisine__lte=2)),
            non_disponible=Count('id', filter=Q(cuisine=3))
        )
    )
    
    # Analyse des WC
    wc_stats = (
        Menage.objects
        .aggregate(
            disponible=Count('id', filter=Q(wc__lte=2)),
            non_disponible=Count('id', filter=Q(wc=3))
        )
    )
    
    # Analyse de l'électricité
    electricite_stats = (
        Menage.objects
        .aggregate(
            disponible=Count('id', filter=Q(mode_eclairage__lte=2)),
            non_disponible=Count('id', filter=Q(mode_eclairage__gt=2))
        )
    )
    
    # Formatage des résultats
    data = []
    
    # Cuisine
    data.extend([
        {
            'equipement': 'Cuisine',
            'statut': 'Disponible',
            'effectif': cuisine_stats['disponible'],
            'pourcentage': round((cuisine_stats['disponible'] * 100.0) / total_menages, 2)
        },
        {
            'equipement': 'Cuisine',
            'statut': 'Non disponible',
            'effectif': cuisine_stats['non_disponible'],
            'pourcentage': round((cuisine_stats['non_disponible'] * 100.0) / total_menages, 2)
        }
    ])
    
    # WC
    data.extend([
        {
            'equipement': 'WC',
            'statut': 'Disponible',
            'effectif': wc_stats['disponible'],
            'pourcentage': round((wc_stats['disponible'] * 100.0) / total_menages, 2)
        },
        {
            'equipement': 'WC',
            'statut': 'Non disponible',
            'effectif': wc_stats['non_disponible'],
            'pourcentage': round((wc_stats['non_disponible'] * 100.0) / total_menages, 2)
        }
    ])
    
    # Électricité
    data.extend([
        {
            'equipement': 'Électricité',
            'statut': 'Disponible',
            'effectif': electricite_stats['disponible'],
            'pourcentage': round((electricite_stats['disponible'] * 100.0) / total_menages, 2)
        },
        {
            'equipement': 'Électricité',
            'statut': 'Non disponible',
            'effectif': electricite_stats['non_disponible'],
            'pourcentage': round((electricite_stats['non_disponible'] * 100.0) / total_menages, 2)
        }
    ])
    
    serializer = EquipementSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def menages_equipements_complets(request):
    """
    Ménages disposant de tous les équipements de base par milieu et région
    """
    # Filtre pour les ménages avec tous les équipements
    menages_complets = Menage.objects.filter(
        Q(baignoire_douche__lte=2) | Q(bain_local__lte=2),  # Q object first
        cuisine__lte=2,  # keyword arguments after
        wc__lte=2,       
        mode_eclairage__lte=2,  
        mode_eau__lte=2         
    )
    
    # Groupement par région et milieu
    resultats = (
        menages_complets
        .values('region', 'milieu')
        .annotate(effectif=Count('id'))
        .order_by('region', 'milieu')
    )
    
    # Calcul des pourcentages par milieu
    total_par_milieu = (
        Menage.objects
        .values('milieu')
        .annotate(total=Count('id'))
    )
    
    # Création d'un dictionnaire pour les totaux
    totaux = {item['milieu']: item['total'] for item in total_par_milieu}
    
    # Enrichissement avec les labels et pourcentages
    data = []
    for resultat in resultats:
        region_label = dict(Menage.REGION_CHOICES).get(resultat['region'], 'Inconnu')
        milieu_label = dict(Menage.MILIEU_CHOICES).get(resultat['milieu'], 'Inconnu')
        
        total_milieu = totaux.get(resultat['milieu'], 1)
        pourcentage = round((resultat['effectif'] * 100.0) / total_milieu, 2)
        
        data.append({
            'region': region_label,
            'milieu': milieu_label,
            'effectif': resultat['effectif'],
            'pourcentage': pourcentage
        })
    
    serializer = EquipementCompletSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def distance_moyenne_route(request):
    """
    Distance moyenne à la route goudronnée par région
    """
    resultats = (
        Menage.objects
        .filter(distance_route__isnull=False)
        .values('region')
        .annotate(distance_moyenne=Avg('distance_route'))
        .order_by('region')
    )
    
    # Enrichissement avec les labels
    data = []
    for resultat in resultats:
        region_label = dict(Menage.REGION_CHOICES).get(resultat['region'], 'Inconnu')
        
        data.append({
            'region': region_label,
            'distance_moyenne': round(resultat['distance_moyenne'], 2)
        })
    
    serializer = DistanceRouteSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def repartition_modes_cuisson(request):
    """
    Répartition des ménages selon le mode de cuisson par milieu
    """
    resultats = (
        Menage.objects
        .values('milieu')
        .annotate(
            gaz=Count('id', filter=Q(utilisation_gaz=1)),
            electricite=Count('id', filter=Q(utilisation_electricite=1)),
            charbon=Count('id', filter=Q(utilisation_charbon=1)),
            bois=Count('id', filter=Q(utilisation_bois=1)),
            total=Count('id')
        )
        .order_by('milieu')
    )
    
    # Enrichissement avec les labels
    data = []
    for resultat in resultats:
        milieu_label = dict(Menage.MILIEU_CHOICES).get(resultat['milieu'], 'Inconnu')
        
        data.append({
            'milieu': milieu_label,
            'gaz': resultat['gaz'],
            'electricite': resultat['electricite'],
            'charbon': resultat['charbon'],
            'bois': resultat['bois'],
            'total': resultat['total']
        })
    
    serializer = ModeCuissonSerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def statistiques_globales(request):
    """
    Statistiques globales sur les ménages
    """
    stats = Menage.objects.aggregate(
        total_menages=Count('id'),
        taille_moyenne_globale=Avg('taille_menage'),
        menages_urbains=Count('id', filter=Q(milieu=1)),
        menages_ruraux=Count('id', filter=Q(milieu=2)),
        menages_proprietaires=Count('id', filter=Q(statut_occupation=1)),
        menages_avec_electricite=Count('id', filter=Q(mode_eclairage__lte=2)),
        menages_avec_eau_courante=Count('id', filter=Q(mode_eau__lte=2))
    )
    
    # Calcul du score d'équipement moyen (ne peut pas être fait avec aggregate car c'est une property)
    menages = Menage.objects.all()
    total_score = sum(menage.niveau_equipement_score for menage in menages)
    score_equipement_moyen = total_score / len(menages) if menages else 0
    stats['score_equipement_moyen'] = round(score_equipement_moyen, 2)
    
    # Calcul des pourcentages
    total = stats['total_menages']
    if total > 0:
        stats['pourcentage_urbains'] = round((stats['menages_urbains'] * 100.0) / total, 2)
        stats['pourcentage_ruraux'] = round((stats['menages_ruraux'] * 100.0) / total, 2)
        stats['pourcentage_proprietaires'] = round((stats['menages_proprietaires'] * 100.0) / total, 2)
        stats['pourcentage_avec_electricite'] = round((stats['menages_avec_electricite'] * 100.0) / total, 2)
        stats['pourcentage_avec_eau_courante'] = round((stats['menages_avec_eau_courante'] * 100.0) / total, 2)
    
    # Arrondir les moyennes
    if stats['taille_moyenne_globale']:
        stats['taille_moyenne_globale'] = round(stats['taille_moyenne_globale'], 2)
    
    return Response(stats)

@api_view(['GET'])
def analyse_par_region(request, region_id):
    """
    Analyse détaillée pour une région spécifique
    """
    try:
        region_label = dict(Menage.REGION_CHOICES).get(region_id, 'Inconnu')
        
        # Statistiques de base pour la région
        stats_region = Menage.objects.filter(region=region_id).aggregate(
            total_menages=Count('id'),
            taille_moyenne=Avg('taille_menage'),
            menages_urbains=Count('id', filter=Q(milieu=1)),
            menages_ruraux=Count('id', filter=Q(milieu=2)),
            menages_proprietaires=Count('id', filter=Q(statut_occupation=1)),
            # Calcul du score d'équipement moyen
            score_equipement_moyen=Avg(
                Case(When(possede_television=1, then=1), default=0) +
                Case(When(possede_radio=1, then=1), default=0) +
                Case(When(possede_telephone_portable=1, then=1), default=0) +
                Case(When(possede_telephone_fixe=1, then=1), default=0) +
                Case(When(possede_internet=1, then=1), default=0) +
                Case(When(possede_ordinateur=1, then=1), default=0) +
                Case(When(possede_parabole=1, then=1), default=0) +
                Case(When(possede_refrigerateur=1, then=1), default=0)
            )
        )
        
        # Distribution par type de ménage
        types_menages = (
            Menage.objects
            .filter(region=region_id)
            .values('type_menage')
            .annotate(effectif=Count('id'))
            .order_by('type_menage')
        )
        
        # Enrichissement des types de ménages
        types_data = []
        for item in types_menages:
            type_label = dict(Menage.TYPE_MENAGE_CHOICES).get(item['type_menage'], 'Inconnu')
            types_data.append({
                'type': type_label,
                'effectif': item['effectif']
            })
        
        # Distribution par type de logement
        types_logements = (
            Menage.objects
            .filter(region=region_id)
            .values('type_logement')
            .annotate(effectif=Count('id'))
            .order_by('type_logement')
        )
        
        # Enrichissement des types de logements
        logements_data = []
        for item in types_logements:
            type_label = dict(Menage.TYPE_LOGEMENT_CHOICES).get(item['type_logement'], 'Inconnu')
            logements_data.append({
                'type': type_label,
                'effectif': item['effectif']
            })
        
        # Calcul des pourcentages
        total = stats_region['total_menages']
        if total > 0:
            stats_region['pourcentage_urbains'] = round((stats_region['menages_urbains'] * 100.0) / total, 2)
            stats_region['pourcentage_ruraux'] = round((stats_region['menages_ruraux'] * 100.0) / total, 2)
            stats_region['pourcentage_proprietaires'] = round((stats_region['menages_proprietaires'] * 100.0) / total, 2)
        
        # Arrondir les moyennes
        stats_region['taille_moyenne'] = round(stats_region['taille_moyenne'], 2)
        if stats_region['score_equipement_moyen'] is not None:
            stats_region['score_equipement_moyen'] = round(stats_region['score_equipement_moyen'], 2)
        
        response_data = {
            'region': region_label,
            'statistiques_globales': stats_region,
            'types_menages': types_data,
            'types_logements': logements_data
        }
        
        return Response(response_data)
        
    except Exception as e:
        return Response(
            {'error': f'Erreur lors de l analyse de la région: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Exemple d'utilisation avec des filtres avancés
@api_view(['GET'])

def analyse_avancee(request):
    """
    Analyse avancée avec filtres multiples
    """
    # Récupération des paramètres de requête
    region_id = request.GET.get('region')
    milieu = request.GET.get('milieu')
    taille_min = request.GET.get('taille_min')
    taille_max = request.GET.get('taille_max')
    
    # Construction de la requête de base
    queryset = Menage.objects.all()
    
    # Application des filtres
    if region_id:
        queryset = queryset.filter(region=region_id)
    if milieu:
        queryset = queryset.filter(milieu=milieu)
    if taille_min:
        queryset = queryset.filter(taille_menage__gte=taille_min)
    if taille_max:
        queryset = queryset.filter(taille_menage__lte=taille_max)
    
    # Annotation pour calculer le score d'équipement directement dans la requête
    queryset = queryset.annotate(
        score_equipement=Sum(
            Case(When(possede_television=1, then=1), default=0, output_field=IntegerField()) +
            Case(When(possede_radio=1, then=1), default=0, output_field=IntegerField()) +
            Case(When(possede_telephone_portable=1, then=1), default=0, output_field=IntegerField()) +
            Case(When(possede_telephone_fixe=1, then=1), default=0, output_field=IntegerField()) +
            Case(When(possede_internet=1, then=1), default=0, output_field=IntegerField()) +
            Case(When(possede_ordinateur=1, then=1), default=0, output_field=IntegerField()) +
            Case(When(possede_parabole=1, then=1), default=0, output_field=IntegerField()) +
            Case(When(possede_refrigerateur=1, then=1), default=0, output_field=IntegerField())
        )
    )
    
    # Calcul des statistiques
    stats = queryset.aggregate(
        total_menages=Count('id'),
        taille_moyenne=Avg('taille_menage'),
        score_equipement_moyen=Avg('score_equipement'),
        menages_proprietaires=Count('id', filter=Q(statut_occupation=1)),
        menages_avec_electricite=Count('id', filter=Q(mode_eclairage__lte=2)),
        menages_avec_eau_courante=Count('id', filter=Q(mode_eau__lte=2))
    )
    
    # Calcul des pourcentages
    total = stats['total_menages']
    if total > 0:
        stats['pourcentage_proprietaires'] = round((stats['menages_proprietaires'] * 100.0) / total, 2)
        stats['pourcentage_avec_electricite'] = round((stats['menages_avec_electricite'] * 100.0) / total, 2)
        stats['pourcentage_avec_eau_courante'] = round((stats['menages_avec_eau_courante'] * 100.0) / total, 2)
    
    # Arrondir les moyennes
    if stats['taille_moyenne']:
        stats['taille_moyenne'] = round(stats['taille_moyenne'], 2)
    if stats['score_equipement_moyen']:
        stats['score_equipement_moyen'] = round(stats['score_equipement_moyen'], 2)
    
    return Response({
        'filtres_appliques': {
            'region': region_id,
            'milieu': milieu,
            'taille_min': taille_min,
            'taille_max': taille_max
        },
        'statistiques': stats
    })