# serializers.py
from rest_framework import serializers
from .models import Individu  

class IndividuSerializer(serializers.ModelSerializer):
    """Serializer principal pour les données démographiques"""
    
    class Meta:
        model = Individu
        fields = '__all__'
        
    def to_representation(self, instance):
        """Personnalisation de la représentation des données"""
        data = super().to_representation(instance)
        
        # Conversion des codes en libellés lisibles
        data['sexe_label'] = self.get_sexe_label(instance.sexe)
        data['milieu_label'] = self.get_milieu_label(instance.milieu)
        data['etat_matrimonial_label'] = self.get_etat_matrimonial_label(instance.etat_matrimonial)
        data['nationalite_label'] = self.get_nationalite_label(instance.nationalite)
        data['niveau_etudes_label'] = self.get_niveau_etudes_label(instance.niveau_etudes)
        data['type_activite_label'] = self.get_type_activite_label(instance.type_activite)
        data['lien_chef_menage_label'] = self.get_lien_chef_menage_label(instance.lien_chef_menage)
        
        return data
    
    def get_sexe_label(self, sexe):
        """Conversion du code sexe en libellé"""
        if sexe == 1:
            return 'Masculin'
        elif sexe == 2:
            return 'Féminin'
        return 'Non spécifié'
    
    def get_milieu_label(self, milieu):
        """Conversion du code milieu en libellé"""
        if milieu == 1:
            return 'Urbain'
        elif milieu == 2:
            return 'Rural'
        return 'Non spécifié'
    
    def get_etat_matrimonial_label(self, etat):
        """Conversion du code état matrimonial en libellé"""
        etats = {
            1: 'Célibataire',
            2: 'Marié(e)',
            3: 'Divorcé(e)',
            4: 'Veuf/Veuve'
        }
        return etats.get(etat, 'Non spécifié')
    
    def get_nationalite_label(self, nationalite):
        """Conversion du code nationalité en libellé"""
        if nationalite == 1:
            return 'Marocaine'
        else:
            return 'Étrangère'
    
    def get_niveau_etudes_label(self, niveau):
        """Conversion du code niveau d'études en libellé"""
        niveaux = {
            0: 'Aucun',
            1: 'Préscolaire',
            2: 'Primaire incomplet',
            3: 'Primaire complet',
            11: 'Secondaire collégial 1ère année',
            12: 'Secondaire collégial 2ème année',
            13: 'Secondaire collégial 3ème année',
            21: 'Secondaire qualifiant 1ère année',
            22: 'Secondaire qualifiant 2ème année',
            23: 'Secondaire qualifiant 3ème année',
            31: 'Supérieur 1ère année',
            32: 'Supérieur 2ème année',
            33: 'Supérieur 3ème année',
            34: 'Supérieur 4ème année',
            35: 'Supérieur 5ème année et plus'
        }
        return niveaux.get(niveau, 'Non spécifié')
    
    def get_type_activite_label(self, type_activite):
        """Conversion du code type d'activité en libellé"""
        types = {
            0: 'Actif occupé',
            1: 'Chômeur ayant déjà travaillé',
            2: 'Chômeur n\'ayant jamais travaillé',
            3: 'Femme au foyer',
            4: 'Étudiant/Élève',
            5: 'Retraité/Rentier',
            6: 'Invalide/Handicapé',
            7: 'Autre inactif'
        }
        return types.get(type_activite, 'Non spécifié')
    
    def get_lien_chef_menage_label(self, lien):
        """Conversion du code lien avec le chef de ménage en libellé"""
        liens = {
            0: 'Chef de ménage',
            1: 'Conjoint(e)',
            2: 'Enfant',
            3: 'Père/Mère',
            4: 'Frère/Sœur',
            5: 'Autre parent',
            6: 'Domestique',
            7: 'Autre'
        }
        return liens.get(lien, 'Non spécifié')

class IndividuMinimalSerializer(serializers.ModelSerializer):
    """Serializer minimal pour les listes et les performances"""
    
    class Meta:
        model = Individu
        fields = [
            'id', 'region', 'province', 'milieu', 'sexe', 'age_simple', 
            'age_quinquennal', 'nationalite', 'etat_matrimonial'
        ]

class DemographicDataCreateSerializer(serializers.ModelSerializer):
    """Serializer pour la création/mise à jour des données"""
    
    class Meta:
        model = Individu
        fields = '__all__'
        
    def validate_age_simple(self, value):
        """Validation de l'âge simple"""
        if value is not None and (value < 0 or value > 120):
            raise serializers.ValidationError("L'âge doit être compris entre 0 et 120 ans")
        return value
    
    def validate_sexe(self, value):
        """Validation du sexe"""
        if value is not None and value not in [1, 2]:
            raise serializers.ValidationError("Le sexe doit être 1 (Masculin) ou 2 (Féminin)")
        return value
    
    def validate_milieu(self, value):
        """Validation du milieu"""
        if value is not None and value not in [1, 2]:
            raise serializers.ValidationError("Le milieu doit être 1 (Urbain) ou 2 (Rural)")
        return value
    
    def validate_etat_matrimonial(self, value):
        """Validation de l'état matrimonial"""
        if value is not None and value not in [1, 2, 3, 4]:
            raise serializers.ValidationError("L'état matrimonial doit être entre 1 et 4")
        return value

class StatistiquesSerializer(serializers.Serializer):
    """Serializer pour les statistiques agrégées"""
    
    effectif = serializers.IntegerField()
    pourcentage = serializers.FloatField()
    
class PopulationAgeSerializer(serializers.Serializer):
    """Serializer pour les analyses par âge"""
    
    age_simple = serializers.IntegerField(required=False)
    age_quinquennal = serializers.IntegerField(required=False)
    effectif = serializers.IntegerField()
    pourcentage = serializers.FloatField()

class PopulationSexeSerializer(serializers.Serializer):
    """Serializer pour les analyses par sexe"""
    
    sexe = serializers.IntegerField()
    effectif = serializers.IntegerField()
    pourcentage = serializers.FloatField()

class PopulationAgeSexeSerializer(serializers.Serializer):
    """Serializer pour le tableau croisé âge/sexe"""
    
    age_quinquennal = serializers.IntegerField()
    sexe = serializers.IntegerField()
    effectif = serializers.IntegerField()

class NationaliteSerializer(serializers.Serializer):
    """Serializer pour les analyses par nationalité"""
    
    nationalite = serializers.IntegerField()
    effectif = serializers.IntegerField()
    pourcentage = serializers.FloatField()

class ChefsMenageSerializer(serializers.Serializer):
    """Serializer pour les analyses des chefs de ménage"""
    
    lien_chef_menage = serializers.IntegerField()
    effectif = serializers.IntegerField()

class FemmesChefsMenageSerializer(serializers.Serializer):
    """Serializer pour les femmes chefs de ménage"""
    
    age_quinquennal = serializers.IntegerField()
    milieu = serializers.IntegerField()
    effectif = serializers.IntegerField()

class EtatMatrimonialSerializer(serializers.Serializer):
    """Serializer pour les analyses de l'état matrimonial"""
    
    age_quinquennal = serializers.IntegerField()
    effectif = serializers.IntegerField()

class CelibatairesMilieuSerializer(serializers.Serializer):
    """Serializer pour les célibataires par milieu et région"""
    
    region = serializers.IntegerField()
    milieu = serializers.IntegerField()
    effectif = serializers.IntegerField()

class HandicapSerializer(serializers.Serializer):
    """Serializer pour les analyses du handicap"""
    
    milieu = serializers.IntegerField()
    sexe = serializers.IntegerField()
    handicap = serializers.IntegerField()
    effectif = serializers.IntegerField()

class HandicapDetailSerializer(serializers.Serializer):
    """Serializer détaillé pour les types de handicap"""
    
    type_handicap = serializers.CharField()
    milieu = serializers.IntegerField()
    sexe = serializers.IntegerField()
    effectif = serializers.IntegerField()
    pourcentage = serializers.FloatField()

class NiveauEducationSerializer(serializers.Serializer):
    """Serializer pour les analyses du niveau d'éducation"""
    
    niveau_agrege = serializers.IntegerField()
    milieu = serializers.IntegerField()
    effectif = serializers.IntegerField()

class NiveauSuperieurSerializer(serializers.Serializer):
    """Serializer pour le niveau supérieur"""
    
    milieu = serializers.IntegerField()
    effectif = serializers.IntegerField()

class ScolarisationSerializer(serializers.Serializer):
    """Serializer pour les analyses de scolarisation"""
    
    statut_scolarisation = serializers.CharField()
    milieu = serializers.IntegerField()
    effectif = serializers.IntegerField()

class ScolarisationDetailSerializer(serializers.Serializer):
    """Serializer détaillé pour la scolarisation"""
    
    age_simple = serializers.IntegerField()
    sexe = serializers.IntegerField()
    milieu = serializers.IntegerField()
    statut_scolarisation = serializers.CharField()
    effectif = serializers.IntegerField()
    taux = serializers.FloatField()

class AlphabetisationSerializer(serializers.Serializer):
    """Serializer pour les analyses d'alphabétisation"""
    
    aptitude_lecture_ecriture = serializers.IntegerField()
    milieu = serializers.IntegerField(required=False)
    sexe = serializers.IntegerField(required=False)
    effectif = serializers.IntegerField()

class AlphabetisationTauxSerializer(serializers.Serializer):
    """Serializer pour les taux d'alphabétisation"""
    
    milieu = serializers.IntegerField()
    sexe = serializers.IntegerField()
    taux_alphabetisation = serializers.FloatField()
    taux_analphabetisme = serializers.FloatField()

class ActiviteEconomiqueSerializer(serializers.Serializer):
    """Serializer pour les analyses d'activité économique"""
    
    statut_activite = serializers.CharField()
    effectif = serializers.IntegerField()

class ActiviteDetailSerializer(serializers.Serializer):
    """Serializer détaillé pour l'activité économique"""
    
    milieu = serializers.IntegerField()
    sexe = serializers.IntegerField()
    type_activite = serializers.IntegerField()
    effectif = serializers.IntegerField()
    taux = serializers.FloatField()

class ChomageSerializer(serializers.Serializer):
    """Serializer pour les analyses du chômage"""
    
    statut_emploi = serializers.CharField()
    effectif = serializers.IntegerField()

class ChomageDetailSerializer(serializers.Serializer):
    """Serializer détaillé pour le chômage"""
    
    milieu = serializers.IntegerField()
    sexe = serializers.IntegerField()
    age_quinquennal = serializers.IntegerField()
    taux_chomage = serializers.FloatField()
    effectif_chomeurs = serializers.IntegerField()
    effectif_actifs = serializers.IntegerField()

class StatistiquesGeneralesSerializer(serializers.Serializer):
    """Serializer pour les statistiques générales"""
    
    total_population = serializers.IntegerField()
    repartition_sexe = serializers.DictField()
    repartition_milieu = serializers.DictField()
    age_moyen = serializers.FloatField()
    nationalite = serializers.DictField()

class IndicateursDemographiquesSerializer(serializers.Serializer):
    """Serializer pour les indicateurs démographiques avancés"""
    
    rapport_masculinite = serializers.FloatField()
    age_median = serializers.FloatField()
    indice_vieillissement = serializers.FloatField()
    taux_dependance = serializers.FloatField()
    taux_activite_global = serializers.FloatField()

class FiltresSerializer(serializers.Serializer):
    """Serializer pour les filtres"""
    
    region = serializers.IntegerField(required=False)
    province = serializers.IntegerField(required=False)
    milieu = serializers.IntegerField(required=False)
    sexe = serializers.IntegerField(required=False)
    age_min = serializers.IntegerField(required=False)
    age_max = serializers.IntegerField(required=False)
    nationalite = serializers.IntegerField(required=False)
    etat_matrimonial = serializers.IntegerField(required=False)
    niveau_etudes = serializers.IntegerField(required=False)
    type_activite = serializers.IntegerField(required=False)
    
    def validate_age_min(self, value):
        if value is not None and (value < 0 or value > 120):
            raise serializers.ValidationError("L'âge minimum doit être entre 0 et 120")
        return value
    
    def validate_age_max(self, value):
        if value is not None and (value < 0 or value > 120):
            raise serializers.ValidationError("L'âge maximum doit être entre 0 et 120")
        return value

class MetadataSerializer(serializers.Serializer):
    """Serializer pour les métadonnées"""
    
    regions = serializers.ListField(child=serializers.IntegerField())
    provinces = serializers.ListField(child=serializers.IntegerField())
    milieux = serializers.ListField(child=serializers.IntegerField())
    sexes = serializers.ListField(child=serializers.DictField())
    etats_matrimoniaux = serializers.ListField(child=serializers.DictField())
    niveaux_etudes = serializers.ListField(child=serializers.DictField())
    types_activite = serializers.ListField(child=serializers.DictField())

class ExportDataSerializer(serializers.Serializer):
    """Serializer pour l'export des données"""
    
    format = serializers.ChoiceField(choices=['json', 'csv', 'excel'], default='json')
    fields = serializers.ListField(child=serializers.CharField(), required=False)
    filters = FiltresSerializer(required=False)
    include_labels = serializers.BooleanField(default=True)

# Serializers pour les réponses d'API spécifiques
class PopulationAgeResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API population par âge"""
    
    type = serializers.CharField()
    data = serializers.ListField(child=PopulationAgeSerializer())

class PopulationSexeResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API population par sexe"""
    
    data = serializers.ListField(child=PopulationSexeSerializer())
    total = serializers.IntegerField()

class PopulationAgeSexeResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse du tableau croisé âge/sexe"""
    
    data = serializers.ListField(child=PopulationAgeSexeSerializer())

class NationaliteResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API nationalité"""
    
    data = serializers.ListField(child=NationaliteSerializer())
    total = serializers.IntegerField()

class FemmesSelonNationaliteResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse des femmes selon nationalité"""
    
    data = serializers.ListField(child=NationaliteSerializer())
    total = serializers.IntegerField()

class ChefsMenageResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API chefs de ménage"""
    
    lien_chef_menage = serializers.ListField(child=ChefsMenageSerializer())
    chefs_par_sexe = serializers.ListField(child=PopulationSexeSerializer())

class FemmesChefsMenageResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse des femmes chefs de ménage"""
    
    data = serializers.ListField(child=FemmesChefsMenageSerializer())

class EtatMatrimonialResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API état matrimonial"""
    
    femmes_celibataires = serializers.ListField(child=EtatMatrimonialSerializer())
    celibataires_par_milieu = serializers.ListField(child=CelibatairesMilieuSerializer())

class HandicapResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API handicap"""
    
    data = serializers.ListField(child=HandicapSerializer())

class NiveauEducationResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API niveau d'éducation"""
    
    niveau_par_milieu = serializers.ListField(child=NiveauEducationSerializer())
    niveau_superieur = serializers.ListField(child=NiveauSuperieurSerializer())

class ScolarisationResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API scolarisation"""
    
    data = serializers.ListField(child=ScolarisationSerializer())

class AlphabetisationResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API alphabétisation"""
    
    global_data = serializers.ListField(child=AlphabetisationSerializer(), source='global')
    detailed = serializers.ListField(child=AlphabetisationSerializer())

class ActiviteEconomiqueResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'API activité économique"""
    
    activite = serializers.ListField(child=ActiviteEconomiqueSerializer())
    chomage = serializers.ListField(child=ChomageSerializer())

class ExportDataResponseSerializer(serializers.Serializer):
    """Serializer pour la réponse de l'export des données"""
    
    count = serializers.IntegerField()
    data = serializers.ListField(child=serializers.DictField())
    format = serializers.CharField()
    exported_at = serializers.DateTimeField()

class ValidationErrorSerializer(serializers.Serializer):
    """Serializer pour les erreurs de validation"""
    
    field = serializers.CharField()
    message = serializers.CharField()
    code = serializers.CharField()

class ErrorResponseSerializer(serializers.Serializer):
    """Serializer pour les réponses d'erreur"""
    
    error = serializers.CharField()
    message = serializers.CharField()
    details = serializers.ListField(child=ValidationErrorSerializer(), required=False)
    status_code = serializers.IntegerField()

# Serializers pour la pagination
class PaginationSerializer(serializers.Serializer):
    """Serializer pour la pagination"""
    
    count = serializers.IntegerField()
    next = serializers.URLField(allow_null=True)
    previous = serializers.URLField(allow_null=True)
    results = serializers.ListField()

# Serializers pour les comparaisons
class ComparaisonRegionSerializer(serializers.Serializer):
    """Serializer pour les comparaisons entre régions"""
    
    region = serializers.IntegerField()
    indicateur = serializers.CharField()
    valeur = serializers.FloatField()
    rang = serializers.IntegerField()

class ComparaisonTemporelleSerializer(serializers.Serializer):
    """Serializer pour les comparaisons temporelles"""
    
    periode = serializers.CharField()
    indicateur = serializers.CharField()
    valeur = serializers.FloatField()
    evolution = serializers.FloatField()

class TableauCroiseSerializer(serializers.Serializer):
    """Serializer générique pour les tableaux croisés"""
    
    variable1 = serializers.CharField()
    variable2 = serializers.CharField()
    valeur1 = serializers.CharField()
    valeur2 = serializers.CharField()
    effectif = serializers.IntegerField()
    pourcentage_ligne = serializers.FloatField()
    pourcentage_colonne = serializers.FloatField()
    pourcentage_total = serializers.FloatField()

# Serializers pour les analyses avancées
class AnalyseCorrelationSerializer(serializers.Serializer):
    """Serializer pour les analyses de corrélation"""
    
    variable1 = serializers.CharField()
    variable2 = serializers.CharField()
    coefficient = serializers.FloatField()
    p_value = serializers.FloatField()
    significatif = serializers.BooleanField()

class AnalyseRegressionSerializer(serializers.Serializer):
    """Serializer pour les analyses de régression"""
    
    variable_dependante = serializers.CharField()
    variables_independantes = serializers.ListField(child=serializers.CharField())
    coefficients = serializers.DictField()
    r_squared = serializers.FloatField()
    p_values = serializers.DictField()

class PyramideAgeSerializer(serializers.Serializer):
    """Serializer pour la pyramide des âges"""
    
    age_quinquennal = serializers.IntegerField()
    hommes = serializers.IntegerField()
    femmes = serializers.IntegerField()
    pourcentage_hommes = serializers.FloatField()
    pourcentage_femmes = serializers.FloatField()

class IndicateursEconomiqueSerializer(serializers.Serializer):
    """Serializer pour les indicateurs économiques"""
    
    taux_activite = serializers.FloatField()
    taux_chomage = serializers.FloatField()
    taux_emploi = serializers.FloatField()
    ratio_dependance_economique = serializers.FloatField()

class IndicateursSociauxSerializer(serializers.Serializer):
    """Serializer pour les indicateurs sociaux"""
    
    taux_alphabetisation = serializers.FloatField()
    taux_scolarisation = serializers.FloatField()
    taux_handicap = serializers.FloatField()
    taille_moyenne_menage = serializers.FloatField()

class SyntheseRegionaleSerializer(serializers.Serializer):
    """Serializer pour la synthèse régionale"""
    
    region = serializers.IntegerField()
    population_totale = serializers.IntegerField()
    densite = serializers.FloatField()
    urbanisation = serializers.FloatField()
    indicateurs_demographiques = IndicateursDemographiquesSerializer()
    indicateurs_economiques = IndicateursEconomiqueSerializer()
    indicateurs_sociaux = IndicateursSociauxSerializer()

class RapportCompletSerializer(serializers.Serializer):
    """Serializer pour le rapport complet"""
    
    metadata = MetadataSerializer()
    statistiques_generales = StatistiquesGeneralesSerializer()
    synthese_regionale = serializers.ListField(child=SyntheseRegionaleSerializer())
    pyramide_age = serializers.ListField(child=PyramideAgeSerializer())
    analyses_thematiques = serializers.DictField()
    recommandations = serializers.ListField(child=serializers.CharField())
    date_generation = serializers.DateTimeField()


from rest_framework import serializers
from django.db.models import Count, Avg, Sum, Case, When, IntegerField, FloatField
from .models import Menage


class TailleMenageSerializer(serializers.Serializer):
    region = serializers.CharField()
    milieu = serializers.CharField()
    taille_moyenne = serializers.FloatField()


class TailleCategorieSerializer(serializers.Serializer):
    taille_categorie = serializers.CharField()
    milieu = serializers.CharField()
    effectif = serializers.IntegerField()

class EquipementSerializer(serializers.Serializer):
    equipement = serializers.CharField()
    statut = serializers.CharField()
    effectif = serializers.IntegerField()
    pourcentage = serializers.FloatField()


class EquipementCompletSerializer(serializers.Serializer):
    region = serializers.CharField()
    milieu = serializers.CharField()
    effectif = serializers.IntegerField()
    pourcentage = serializers.FloatField()


class DistanceRouteSerializer(serializers.Serializer):
    region = serializers.CharField()
    distance_moyenne = serializers.FloatField()


class ModeCuissonSerializer(serializers.Serializer):
    milieu = serializers.CharField()
    gaz = serializers.IntegerField()
    electricite = serializers.IntegerField()
    charbon = serializers.IntegerField()
    bois = serializers.IntegerField()
    total = serializers.IntegerField()

