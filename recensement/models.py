# models.py - Version corrigée
from django.db import models

class Individu(models.Model):
    """Modèle pour les données individuelles du recensement"""
    
    # Identification géographique - Permettre NULL
    region = models.IntegerField(verbose_name="Région", null=True, blank=True)
    province = models.IntegerField(verbose_name="Province", null=True, blank=True) 
    milieu = models.IntegerField(verbose_name="Milieu de résidence", null=True, blank=True)
    
    # Identification du ménage - Permettre NULL
    numero_menage_province = models.IntegerField(verbose_name="Numéro de ménage dans la province", null=True, blank=True)
    numero_ordre_menage = models.IntegerField(verbose_name="Numéro d'ordre dans le ménage", null=True, blank=True)
    
    # Relation avec le chef de ménage - Permettre NULL
    lien_chef_menage = models.IntegerField(verbose_name="Lien avec le chef de ménage", null=True, blank=True)
    
    # Caractéristiques démographiques de base - Permettre NULL
    nationalite = models.IntegerField(verbose_name="Nationalité", null=True, blank=True)
    sexe = models.IntegerField(verbose_name="Sexe", null=True, blank=True)
    age_simple = models.IntegerField(verbose_name="Âge simple", null=True, blank=True)
    age_quinquennal = models.IntegerField(verbose_name="Âge quinquennal", null=True, blank=True)
    etat_matrimonial = models.IntegerField(verbose_name="État matrimonial", null=True, blank=True)
    
    # Fécondité
    enfants_vivants = models.IntegerField(verbose_name="Enfants vivants", null=True, blank=True)
    enfants_decedes = models.IntegerField(verbose_name="Enfants décédés", null=True, blank=True)
    naissances_vivantes_12m = models.IntegerField(verbose_name="Naissances vivantes 12 derniers mois", null=True, blank=True)
    deces_12m = models.IntegerField(verbose_name="Décès 12 derniers mois", null=True, blank=True)
    
    # Handicap
    handicap_vision = models.IntegerField(verbose_name="Handicap (Vision)", null=True, blank=True)
    handicap_audition = models.IntegerField(verbose_name="Handicap (Audition)", null=True, blank=True)
    handicap_mobilite = models.IntegerField(verbose_name="Handicap (Mobilité)", null=True, blank=True)
    handicap_memoire = models.IntegerField(verbose_name="Handicap (Mémoire)", null=True, blank=True)
    handicap_entretien = models.IntegerField(verbose_name="Handicap (Entretien)", null=True, blank=True)
    handicap_communication = models.IntegerField(verbose_name="Handicap (Communication)", null=True, blank=True)
    situation_handicap = models.IntegerField(verbose_name="Situation de handicap", null=True, blank=True)
    
    # Éducation
    niveau_etudes = models.IntegerField(verbose_name="Niveau d'études", null=True, blank=True)
    niveau_etudes_agrege = models.IntegerField(verbose_name="Niveau d'études agriculture", null=True, blank=True)
    secteur_enseignement = models.IntegerField(verbose_name="Secteur d'enseignement", null=True, blank=True)
    scolarisation = models.IntegerField(verbose_name="Scolarisation", null=True, blank=True)
    lieu_etudes = models.IntegerField(verbose_name="Lieu d'études", null=True, blank=True)
    mode_transport_etudes = models.IntegerField(verbose_name="Mode de transport études", null=True, blank=True)
    aptitude_lecture_ecriture = models.IntegerField(verbose_name="Aptitude à lire et écrire", null=True, blank=True)
    
    # Langues
    langue_1 = models.IntegerField(verbose_name="1ère langue lue", null=True, blank=True)
    langue_2 = models.IntegerField(verbose_name="2ème langue lue", null=True, blank=True)
    langue_3 = models.IntegerField(verbose_name="3ème langue lue", null=True, blank=True)
    langue_locale_1 = models.IntegerField(verbose_name="1ère langue locale", null=True, blank=True)
    langue_locale_2 = models.IntegerField(verbose_name="2ème langue locale", null=True, blank=True)
    
    # Diplômes
    diplome_superieur_general = models.IntegerField(verbose_name="Diplôme supérieur général", null=True, blank=True)
    diplome_general = models.IntegerField(verbose_name="Diplôme général", null=True, blank=True)
    diplome_formation_professionnelle_superieur = models.IntegerField(verbose_name="Diplôme FP supérieur", null=True, blank=True)
    diplome_formation_professionnelle_general = models.IntegerField(verbose_name="Diplôme FP général", null=True, blank=True)
    diplome_formation_professionnelle_base = models.IntegerField(verbose_name="Diplôme FP de base", null=True, blank=True)
    
    # Activité économique
    type_activite = models.IntegerField(verbose_name="Type d'activité", null=True, blank=True)
    profession_superieur_general = models.IntegerField(verbose_name="Profession supérieur général", null=True, blank=True)
    profession_general = models.IntegerField(verbose_name="Profession général", null=True, blank=True)
    statut_professionnel = models.IntegerField(verbose_name="Statut professionnel", null=True, blank=True)
    activite_economique_superieur = models.IntegerField(verbose_name="Activité économique supérieur", null=True, blank=True)
    activite_economique_general = models.IntegerField(verbose_name="Activité économique général", null=True, blank=True)
    
    # Travail
    lieu_travail = models.IntegerField(verbose_name="Lieu de travail", null=True, blank=True)
    mode_transport_travail = models.IntegerField(verbose_name="Mode de transport travail", null=True, blank=True)
    
    # Données physiques
    poids = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Poids (kg)", null=True, blank=True)
    
    # Métadonnées
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'recensement_individu'
        verbose_name = 'Individu'
        verbose_name_plural = 'Individus'
        indexes = [
            models.Index(fields=['region', 'province']),
            models.Index(fields=['numero_menage_province']),
            models.Index(fields=['sexe']),
            models.Index(fields=['age_simple']),
            models.Index(fields=['niveau_etudes']),
            models.Index(fields=['type_activite']),
        ]
    
    def __str__(self):
        return f"Individu {self.numero_ordre_menage or 'N/A'} - Ménage {self.numero_menage_province or 'N/A'}"
    
    def get_sexe_display(self):
        """Affichage du sexe"""
        if self.sexe == 1:
            return "Masculin"
        elif self.sexe == 2:
            return "Féminin"
        return "Non renseigné"
    
    def get_milieu_display(self):
        """Affichage du milieu"""
        if self.milieu == 1:
            return "Urbain"
        elif self.milieu == 2:
            return "Rural"
        return "Non renseigné"
    
    def get_age_groupe(self):
        """Calcul du groupe d'âge"""
        if self.age_simple is None:
            return "Non renseigné"
        elif self.age_simple < 15:
            return "0-14 ans"
        elif self.age_simple < 65:
            return "15-64 ans"
        else:
            return "65+ ans"
        



################################################################################
##########################################################################""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Menage(models.Model):
    """
    Modèle représentant un ménage marocain avec toutes ses caractéristiques
    """
    
    # Choix pour les différentes variables
    REGION_CHOICES = [
        (1, 'Tanger-Tétouan-Al Hoceïma'),
        (2, 'Oriental'),
        (3, 'Fès-Meknès'),
        (4, 'Rabat-Salé-Kénitra'),
        (5, 'Béni Mellal-Khénifra'),
        (6, 'Casablanca-Settat'),
        (7, 'Marrakech-Safi'),
        (8, 'Drâa-Tafilalet'),
        (9, 'Souss-Massa'),
        (10, 'Guelmim-Oued Noun'),
        (11, 'Laâyoune-Sakia El Hamra'),
        (12, 'Dakhla-Oued Ed Dahab'),
        (99, 'Information identifiante'),
    ]
    
    PROVINCE_CHOICES = [
        (1, 'Agadir-Ida-Ou-Tanane'),
        (41, 'Al Haouz'),
        (51, 'Al Hoceïma'),
        (61, 'Meknès'),
        (81, 'Azilal'),
        (91, 'Béni Mellal'),
        (111, 'Benslimane'),
        (113, 'Berkane'),
        (117, 'Berrechid'),
        (121, 'Boujdour'),
        (131, 'Boulemane'),
        (141, 'Casablanca'),
        (151, 'Chefchaouen'),
        (161, 'Chichaoua'),
        (163, 'Chtouka-Ait Baha'),
        (167, 'Driouch'),
        (171, 'El Hajeb'),
        (181, 'El Jadida'),
        (191, 'El Kelâa des Sraghna'),
        (201, 'Errachidia'),
        (211, 'Essaouira'),
        (227, 'Fahs-Anjra'),
        (231, 'Fès'),
        (251, 'Figuig'),
        (255, 'Fquih Ben Salah'),
        (261, 'Guelmim'),
        (265, 'Guercif'),
        (271, 'Ifrane'),
        (273, 'Inezgane-Ait Melloul'),
        (275, 'Jerada'),
        (281, 'Kénitra'),
        (291, 'Khémisset'),
        (301, 'Khénifra'),
        (311, 'Khouribga'),
        (321, 'Laâyoune'),
        (331, 'Larache'),
        (351, 'Marrakech'),
        (355, 'Médiouna'),
        (363, 'Midelt'),
        (371, 'Mohammadia'),
        (381, 'Nador'),
        (385, 'Nouaceur'),
        (401, 'Ouarzazate'),
        (405, 'Ouezzane'),
        (411, 'Oujda-Angad'),
        (421, 'Rabat'),
        (427, 'Rehamna'),
        (431, 'Safi'),
        (441, 'Salé'),
        (451, 'Sefrou'),
        (461, 'Settat'),
        (467, 'Sidi Bennour'),
        (473, 'Sidi Ifni'),
        (481, 'Sidi Kacem'),
        (491, 'Sidi Slimane'),
        (501, 'Skhirate-Témara'),
        (511, 'Tanger-Assilah'),
        (531, 'Taounate'),
        (533, 'Taourirt'),
        (541, 'Taroudannt'),
        (551, 'Tata'),
        (561, 'Taza'),
        (571, 'Tétouan'),
        (573, 'M\'Diq-Fnideq'),
        (577, 'Tinghir'),
        (581, 'Tiznit'),
        (585, 'Youssoufia'),
        (587, 'Zagora'),
        (591, 'Moulay Yacoub'),
        (996, 'Tan-Tan / Assa-Zag'),
        (997, 'Es-Semara / Tarfaya'),
        (998, 'Oued Ed Dahab / Aousserd'),
        (999, 'Information identifiante'),
    ]
    
    MILIEU_CHOICES = [
        (1, 'Urbain'),
        (2, 'Rural'),
        (9, 'Information identifiante'),
    ]
    
    TYPE_LOGEMENT_CHOICES = [
        (1, 'Villa / Étage de villa'),
        (2, 'Appartement'),
        (3, 'Maison marocaine'),
        (4, 'Maison sommaire / Bidonville'),
        (5, 'Logement rural'),
        (6, 'Autre'),
        (9, 'Non déterminé'),
    ]
    
    MURS_CHOICES = [
        (1, 'Béton armé / Briques en terre cuite / Parpaings'),
        (2, 'Pierres scellées avec du mortier'),
        (3, 'Planches de bois'),
        (4, 'Pierres scellées avec de la terre'),
        (5, 'Pisé / Briques de terre crue'),
        (6, 'Bois récupéré / Étain / Herbe / Bambou'),
        (7, 'Autres'),
    ]
    
    TOIT_CHOICES = [
        (1, 'Dalle'),
        (2, 'Planches de bois / Tuiles'),
        (3, 'Tôle en ciment / Tôle en étain'),
        (4, 'Bois récupéré, Bambou ou Herbe recouverts de terre'),
        (5, 'Étain / Plastique / Autres matériaux récupérés'),
        (6, 'Autres'),
    ]
    
    SOL_CHOICES = [
        (1, 'Carrelage / Mosaïque / Marbre'),
        (2, 'Mortier / Béton'),
        (3, 'Bois'),
        (4, 'Sol nu / Sol recouvert de matériaux en terre ou assimilés'),
        (5, 'Autre'),
    ]
    
    AGE_LOGEMENT_CHOICES = [
        (1, 'Moins de 10 ans'),
        (2, '10-19 ans'),
        (3, '20-49 ans'),
        (4, '50 ans et plus'),
        (9, 'Non déterminé'),
    ]
    
    STATUT_OCCUPATION_CHOICES = [
        (1, 'Propriétaire'),
        (2, 'Locataire'),
        (3, 'Occupant un logement de fonction'),
        (4, 'Logé gratuitement'),
        (5, 'Autre'),
        (9, 'Non déterminé'),
    ]
    
    DISPONIBILITE_CHOICES = [
        (1, 'Privée'),
        (2, 'Partagée'),
        (3, 'Non disponible'),
    ]
    
    DISPONIBILITE_PRIV_CHOICES = [
        (1, 'Privés'),
        (2, 'Partagés'),
        (3, 'Non disponibles'),
    ]
    
    ECLAIRAGE_CHOICES = [
        (1, 'Réseau public de distribution d\'électricité (raccordement privé)'),
        (2, 'Réseau public de distribution d\'électricité (raccordement partagé)'),
        (3, 'Gaz (butane)'),
        (4, 'Lampe à huile / Bougies'),
        (5, 'Énergie solaire'),
        (6, 'Groupe électrogène'),
        (7, 'Autre'),
        (9, 'Non déterminé (hors réseau public)'),
    ]
    
    EAU_MODE_CHOICES = [
        (1, 'Réseau public de distribution d\'eau courante (raccordement privé)'),
        (2, 'Réseau public de distribution d\'eau courante (raccordement partagé)'),
        (3, 'Fontaine / Puits / Matfia / Point d\'eau (équipés)'),
        (4, 'Vendeur d\'eau potable'),
        (5, 'Puits / Matfia (non équipés)'),
        (6, 'Source / Oued / Ruisseau'),
        (7, 'Autre'),
        (9, 'Non déterminé (hors réseau public)'),
    ]
    
    DISTANCE_CHOICES = [
        (1, 'Moins de 200 m'),
        (2, 'De 200 m à moins d\'1 km'),
        (3, '1 km et plus'),
        (8, 'Non déterminée'),
        (9, 'Ménage disposant d\'un raccordement au réseau de distribution d\'eau courante'),
    ]
    
    EAUX_USEES_CHOICES = [
        (1, 'Réseau public d\'assainissement'),
        (2, 'Fosse septique'),
        (3, 'Puits perdu'),
        (4, 'Dans la nature'),
        (5, 'Autre'),
    ]
    
    DECHETS_CHOICES = [
        (1, 'Bac à ordures de la commune'),
        (2, 'Camion de la commune / Camion privé'),
        (3, 'Dans la nature'),
        (4, 'Autre'),
    ]
    
    UTILISATION_CHOICES = [
        (1, 'Utilisé fréquemment'),
        (2, 'Utilisé occasionnellement'),
        (3, 'Non utilisé'),
        (9, 'Non déterminé'),
    ]
    
    UTILISATION_FEMININ_CHOICES = [
        (1, 'Utilisées fréquemment'),
        (2, 'Utilisées occasionnellement'),
        (3, 'Non utilisées'),
        (9, 'Non déterminées'),
    ]
    
    OUI_NON_CHOICES = [
        (1, 'Oui'),
        (2, 'Non'),
        (9, 'Non déterminé'),
    ]
    
    NOMBRE_VEHICULES_CHOICES = [
        (0, 'Aucun'),
        (1, '1'),
        (2, '2 et plus'),
        (9, 'Non déterminé'),
    ]
    
    TYPE_MENAGE_CHOICES = [
        (1, 'Ménage d\'une seule personne'),
        (2, 'Ménage nucléaire - Couple marié avec enfant(s) non marié(s)'),
        (3, 'Ménage nucléaire - Couple marié sans enfant'),
        (4, 'Ménage nucléaire - Père avec enfant(s) non marié(s)'),
        (5, 'Ménage nucléaire - Mère avec enfant(s) non marié(s)'),
        (6, 'Ménage polygame'),
        (7, 'Ménage élargi'),
        (8, 'Ménage composite'),
        (9, 'Non déterminé'),
    ]
    
    # Champs du modèle
    # Localisation
    region = models.IntegerField(
        choices=REGION_CHOICES,
        verbose_name="Région"
    )
    province = models.IntegerField(
        choices=PROVINCE_CHOICES,
        verbose_name="Province"
    )
    milieu = models.IntegerField(
        choices=MILIEU_CHOICES,
        verbose_name="Milieu de résidence"
    )
    
    # Composition du ménage
    numero_menage = models.IntegerField(
        verbose_name="Numéro de ménage",
        validators=[MinValueValidator(1)]
    )
    taille_menage = models.IntegerField(
        verbose_name="Taille du ménage",
        validators=[MinValueValidator(1)]
    )
    type_menage = models.IntegerField(
        choices=TYPE_MENAGE_CHOICES,
        verbose_name="Type de ménage"
    )
    
    # Caractéristiques du logement
    type_logement = models.IntegerField(
        choices=TYPE_LOGEMENT_CHOICES,
        verbose_name="Type de logement"
    )
    materiaux_murs = models.IntegerField(
        choices=MURS_CHOICES,
        verbose_name="Matériaux des murs principaux"
    )
    materiaux_toit = models.IntegerField(
        choices=TOIT_CHOICES,
        verbose_name="Matériaux du toit principal"
    )
    materiaux_sol = models.IntegerField(
        choices=SOL_CHOICES,
        verbose_name="Matériaux du sol principal"
    )
    age_logement = models.IntegerField(
        choices=AGE_LOGEMENT_CHOICES,
        verbose_name="Âge du logement"
    )
    nombre_pieces = models.IntegerField(
        verbose_name="Nombre de pièces d'habitation",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    statut_occupation = models.IntegerField(
        choices=STATUT_OCCUPATION_CHOICES,
        verbose_name="Statut d'occupation"
    )
    
    # Équipements du logement
    cuisine = models.IntegerField(
        choices=DISPONIBILITE_CHOICES,
        verbose_name="Cuisine - Disponibilité"
    )
    wc = models.IntegerField(
        choices=DISPONIBILITE_PRIV_CHOICES,
        verbose_name="W.-C. - Disponibilité"
    )
    baignoire_douche = models.IntegerField(
        choices=DISPONIBILITE_CHOICES,
        verbose_name="Baignoire / Douche - Disponibilité"
    )
    bain_local = models.IntegerField(
        choices=DISPONIBILITE_CHOICES,
        verbose_name="Bain local - Disponibilité"
    )
    
    # Services publics
    mode_eclairage = models.IntegerField(
        choices=ECLAIRAGE_CHOICES,
        verbose_name="Mode d'éclairage"
    )
    mode_eau = models.IntegerField(
        choices=EAU_MODE_CHOICES,
        verbose_name="Mode d'approvisionnement en eau"
    )
    distance_eau = models.IntegerField(
        choices=DISTANCE_CHOICES,
        verbose_name="Distance au point d'eau"
    )
    duree_eau = models.IntegerField(
        verbose_name="Durée nécessaire pour s'approvisionner en eau (minutes)",
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    evacuation_eaux_usees = models.IntegerField(
        choices=EAUX_USEES_CHOICES,
        verbose_name="Mode d'évacuation des eaux usées"
    )
    evacuation_dechets = models.IntegerField(
        choices=DECHETS_CHOICES,
        verbose_name="Mode d'évacuation des déchets ménagers"
    )
    
    # Combustibles et énergie
    utilisation_gaz = models.IntegerField(
        choices=UTILISATION_CHOICES,
        verbose_name="Gaz - Combustible"
    )
    utilisation_electricite = models.IntegerField(
        choices=UTILISATION_CHOICES,
        verbose_name="Électricité - Combustible"
    )
    utilisation_charbon = models.IntegerField(
        choices=UTILISATION_CHOICES,
        verbose_name="Charbon - Combustible"
    )
    utilisation_bois = models.IntegerField(
        choices=UTILISATION_CHOICES,
        verbose_name="Bois - Combustible"
    )
    utilisation_dejections_animales = models.IntegerField(
        choices=UTILISATION_FEMININ_CHOICES,
        verbose_name="Déjections animales - Combustible"
    )
    
    # Équipements électroniques
    possede_television = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Téléviseur - Possession"
    )
    possede_radio = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Radio - Possession"
    )
    possede_telephone_portable = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Téléphone portable - Possession"
    )
    possede_telephone_fixe = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Téléphone fixe - Possession"
    )
    possede_internet = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Internet - Possession"
    )
    possede_ordinateur = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Ordinateur - Possession"
    )
    possede_parabole = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Parabole - Possession"
    )
    possede_refrigerateur = models.IntegerField(
        choices=OUI_NON_CHOICES,
        verbose_name="Réfrigérateur - Possession"
    )
    
    # Moyens de transport
    nombre_camions = models.IntegerField(
        choices=NOMBRE_VEHICULES_CHOICES,
        verbose_name="Nombre de camions"
    )
    nombre_voitures = models.IntegerField(
        choices=NOMBRE_VEHICULES_CHOICES,
        verbose_name="Nombre de voitures"
    )
    nombre_tracteurs = models.IntegerField(
        choices=NOMBRE_VEHICULES_CHOICES,
        verbose_name="Nombre de tracteurs"
    )
    nombre_motocycles = models.IntegerField(
        choices=NOMBRE_VEHICULES_CHOICES,
        verbose_name="Nombre de motocycles"
    )
    
    # Accessibilité
    distance_route = models.IntegerField(
        verbose_name="Distance à la route goudronnée (km)",
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    # Métadonnées
    poids = models.DecimalField(
        max_digits=16,
        decimal_places=15,
        verbose_name="Poids",
        null=True,
        blank=True
    )
    
    # Champs de gestion
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Ménage"
        verbose_name_plural = "Ménages"
        ordering = ['region', 'province', 'numero_menage']
    
    def __str__(self):
        return f"Ménage {self.numero_menage} - {self.get_region_display()}"
    
    @property
    def est_urbain(self):
        """Retourne True si le ménage est en milieu urbain"""
        return self.milieu == 1
    
    @property
    def est_rural(self):
        """Retourne True si le ménage est en milieu rural"""
        return self.milieu == 2
    
    @property
    def est_proprietaire(self):
        """Retourne True si le ménage est propriétaire de son logement"""
        return self.statut_occupation == 1
    
    @property
    def a_electricite(self):
        """Retourne True si le ménage a accès à l'électricité du réseau public"""
        return self.mode_eclairage in [1, 2]
    
    @property
    def a_eau_courante(self):
        """Retourne True si le ménage a accès à l'eau courante"""
        return self.mode_eau in [1, 2]
    
    @property
    def niveau_equipement_score(self):
        """Calcule un score d'équipement basé sur les possessions"""
        score = 0
        equipements = [
            self.possede_television,
            self.possede_radio,
            self.possede_telephone_portable,
            self.possede_telephone_fixe,
            self.possede_internet,
            self.possede_ordinateur,
            self.possede_parabole,
            self.possede_refrigerateur
        ]
        
        for equipement in equipements:
            if equipement == 1:  # Oui
                score += 1
        
        return score
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('menage_detail', args=[str(self.id)])