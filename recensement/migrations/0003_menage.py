# Generated by Django 5.2.3 on 2025-07-03 11:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recensement', '0002_alter_individu_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.IntegerField(choices=[(1, 'Tanger-Tétouan-Al Hoceïma'), (2, 'Oriental'), (3, 'Fès-Meknès'), (4, 'Rabat-Salé-Kénitra'), (5, 'Béni Mellal-Khénifra'), (6, 'Casablanca-Settat'), (7, 'Marrakech-Safi'), (8, 'Drâa-Tafilalet'), (9, 'Souss-Massa'), (10, 'Guelmim-Oued Noun'), (11, 'Laâyoune-Sakia El Hamra'), (12, 'Dakhla-Oued Ed Dahab'), (99, 'Information identifiante')], verbose_name='Région')),
                ('province', models.IntegerField(choices=[(1, 'Agadir-Ida-Ou-Tanane'), (41, 'Al Haouz'), (51, 'Al Hoceïma'), (61, 'Meknès'), (81, 'Azilal'), (91, 'Béni Mellal'), (111, 'Benslimane'), (113, 'Berkane'), (117, 'Berrechid'), (121, 'Boujdour'), (131, 'Boulemane'), (141, 'Casablanca'), (151, 'Chefchaouen'), (161, 'Chichaoua'), (163, 'Chtouka-Ait Baha'), (167, 'Driouch'), (171, 'El Hajeb'), (181, 'El Jadida'), (191, 'El Kelâa des Sraghna'), (201, 'Errachidia'), (211, 'Essaouira'), (227, 'Fahs-Anjra'), (231, 'Fès'), (251, 'Figuig'), (255, 'Fquih Ben Salah'), (261, 'Guelmim'), (265, 'Guercif'), (271, 'Ifrane'), (273, 'Inezgane-Ait Melloul'), (275, 'Jerada'), (281, 'Kénitra'), (291, 'Khémisset'), (301, 'Khénifra'), (311, 'Khouribga'), (321, 'Laâyoune'), (331, 'Larache'), (351, 'Marrakech'), (355, 'Médiouna'), (363, 'Midelt'), (371, 'Mohammadia'), (381, 'Nador'), (385, 'Nouaceur'), (401, 'Ouarzazate'), (405, 'Ouezzane'), (411, 'Oujda-Angad'), (421, 'Rabat'), (427, 'Rehamna'), (431, 'Safi'), (441, 'Salé'), (451, 'Sefrou'), (461, 'Settat'), (467, 'Sidi Bennour'), (473, 'Sidi Ifni'), (481, 'Sidi Kacem'), (491, 'Sidi Slimane'), (501, 'Skhirate-Témara'), (511, 'Tanger-Assilah'), (531, 'Taounate'), (533, 'Taourirt'), (541, 'Taroudannt'), (551, 'Tata'), (561, 'Taza'), (571, 'Tétouan'), (573, "M'Diq-Fnideq"), (577, 'Tinghir'), (581, 'Tiznit'), (585, 'Youssoufia'), (587, 'Zagora'), (591, 'Moulay Yacoub'), (996, 'Tan-Tan / Assa-Zag'), (997, 'Es-Semara / Tarfaya'), (998, 'Oued Ed Dahab / Aousserd'), (999, 'Information identifiante')], verbose_name='Province')),
                ('milieu', models.IntegerField(choices=[(1, 'Urbain'), (2, 'Rural'), (9, 'Information identifiante')], verbose_name='Milieu de résidence')),
                ('numero_menage', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Numéro de ménage')),
                ('taille_menage', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Taille du ménage')),
                ('type_menage', models.IntegerField(choices=[(1, "Ménage d'une seule personne"), (2, 'Ménage nucléaire - Couple marié avec enfant(s) non marié(s)'), (3, 'Ménage nucléaire - Couple marié sans enfant'), (4, 'Ménage nucléaire - Père avec enfant(s) non marié(s)'), (5, 'Ménage nucléaire - Mère avec enfant(s) non marié(s)'), (6, 'Ménage polygame'), (7, 'Ménage élargi'), (8, 'Ménage composite'), (9, 'Non déterminé')], verbose_name='Type de ménage')),
                ('type_logement', models.IntegerField(choices=[(1, 'Villa / Étage de villa'), (2, 'Appartement'), (3, 'Maison marocaine'), (4, 'Maison sommaire / Bidonville'), (5, 'Logement rural'), (6, 'Autre'), (9, 'Non déterminé')], verbose_name='Type de logement')),
                ('materiaux_murs', models.IntegerField(choices=[(1, 'Béton armé / Briques en terre cuite / Parpaings'), (2, 'Pierres scellées avec du mortier'), (3, 'Planches de bois'), (4, 'Pierres scellées avec de la terre'), (5, 'Pisé / Briques de terre crue'), (6, 'Bois récupéré / Étain / Herbe / Bambou'), (7, 'Autres')], verbose_name='Matériaux des murs principaux')),
                ('materiaux_toit', models.IntegerField(choices=[(1, 'Dalle'), (2, 'Planches de bois / Tuiles'), (3, 'Tôle en ciment / Tôle en étain'), (4, 'Bois récupéré, Bambou ou Herbe recouverts de terre'), (5, 'Étain / Plastique / Autres matériaux récupérés'), (6, 'Autres')], verbose_name='Matériaux du toit principal')),
                ('materiaux_sol', models.IntegerField(choices=[(1, 'Carrelage / Mosaïque / Marbre'), (2, 'Mortier / Béton'), (3, 'Bois'), (4, 'Sol nu / Sol recouvert de matériaux en terre ou assimilés'), (5, 'Autre')], verbose_name='Matériaux du sol principal')),
                ('age_logement', models.IntegerField(choices=[(1, 'Moins de 10 ans'), (2, '10-19 ans'), (3, '20-49 ans'), (4, '50 ans et plus'), (9, 'Non déterminé')], verbose_name='Âge du logement')),
                ('nombre_pieces', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Nombre de pièces d'habitation")),
                ('statut_occupation', models.IntegerField(choices=[(1, 'Propriétaire'), (2, 'Locataire'), (3, 'Occupant un logement de fonction'), (4, 'Logé gratuitement'), (5, 'Autre'), (9, 'Non déterminé')], verbose_name="Statut d'occupation")),
                ('cuisine', models.IntegerField(choices=[(1, 'Privée'), (2, 'Partagée'), (3, 'Non disponible')], verbose_name='Cuisine - Disponibilité')),
                ('wc', models.IntegerField(choices=[(1, 'Privés'), (2, 'Partagés'), (3, 'Non disponibles')], verbose_name='W.-C. - Disponibilité')),
                ('baignoire_douche', models.IntegerField(choices=[(1, 'Privée'), (2, 'Partagée'), (3, 'Non disponible')], verbose_name='Baignoire / Douche - Disponibilité')),
                ('bain_local', models.IntegerField(choices=[(1, 'Privée'), (2, 'Partagée'), (3, 'Non disponible')], verbose_name='Bain local - Disponibilité')),
                ('mode_eclairage', models.IntegerField(choices=[(1, "Réseau public de distribution d'électricité (raccordement privé)"), (2, "Réseau public de distribution d'électricité (raccordement partagé)"), (3, 'Gaz (butane)'), (4, 'Lampe à huile / Bougies'), (5, 'Énergie solaire'), (6, 'Groupe électrogène'), (7, 'Autre'), (9, 'Non déterminé (hors réseau public)')], verbose_name="Mode d'éclairage")),
                ('mode_eau', models.IntegerField(choices=[(1, "Réseau public de distribution d'eau courante (raccordement privé)"), (2, "Réseau public de distribution d'eau courante (raccordement partagé)"), (3, "Fontaine / Puits / Matfia / Point d'eau (équipés)"), (4, "Vendeur d'eau potable"), (5, 'Puits / Matfia (non équipés)'), (6, 'Source / Oued / Ruisseau'), (7, 'Autre'), (9, 'Non déterminé (hors réseau public)')], verbose_name="Mode d'approvisionnement en eau")),
                ('distance_eau', models.IntegerField(choices=[(1, 'Moins de 200 m'), (2, "De 200 m à moins d'1 km"), (3, '1 km et plus'), (8, 'Non déterminée'), (9, "Ménage disposant d'un raccordement au réseau de distribution d'eau courante")], verbose_name="Distance au point d'eau")),
                ('duree_eau', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Durée nécessaire pour s'approvisionner en eau (minutes)")),
                ('evacuation_eaux_usees', models.IntegerField(choices=[(1, "Réseau public d'assainissement"), (2, 'Fosse septique'), (3, 'Puits perdu'), (4, 'Dans la nature'), (5, 'Autre')], verbose_name="Mode d'évacuation des eaux usées")),
                ('evacuation_dechets', models.IntegerField(choices=[(1, 'Bac à ordures de la commune'), (2, 'Camion de la commune / Camion privé'), (3, 'Dans la nature'), (4, 'Autre')], verbose_name="Mode d'évacuation des déchets ménagers")),
                ('utilisation_gaz', models.IntegerField(choices=[(1, 'Utilisé fréquemment'), (2, 'Utilisé occasionnellement'), (3, 'Non utilisé'), (9, 'Non déterminé')], verbose_name='Gaz - Combustible')),
                ('utilisation_electricite', models.IntegerField(choices=[(1, 'Utilisé fréquemment'), (2, 'Utilisé occasionnellement'), (3, 'Non utilisé'), (9, 'Non déterminé')], verbose_name='Électricité - Combustible')),
                ('utilisation_charbon', models.IntegerField(choices=[(1, 'Utilisé fréquemment'), (2, 'Utilisé occasionnellement'), (3, 'Non utilisé'), (9, 'Non déterminé')], verbose_name='Charbon - Combustible')),
                ('utilisation_bois', models.IntegerField(choices=[(1, 'Utilisé fréquemment'), (2, 'Utilisé occasionnellement'), (3, 'Non utilisé'), (9, 'Non déterminé')], verbose_name='Bois - Combustible')),
                ('utilisation_dejections_animales', models.IntegerField(choices=[(1, 'Utilisées fréquemment'), (2, 'Utilisées occasionnellement'), (3, 'Non utilisées'), (9, 'Non déterminées')], verbose_name='Déjections animales - Combustible')),
                ('possede_television', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Téléviseur - Possession')),
                ('possede_radio', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Radio - Possession')),
                ('possede_telephone_portable', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Téléphone portable - Possession')),
                ('possede_telephone_fixe', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Téléphone fixe - Possession')),
                ('possede_internet', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Internet - Possession')),
                ('possede_ordinateur', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Ordinateur - Possession')),
                ('possede_parabole', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Parabole - Possession')),
                ('possede_refrigerateur', models.IntegerField(choices=[(1, 'Oui'), (2, 'Non'), (9, 'Non déterminé')], verbose_name='Réfrigérateur - Possession')),
                ('nombre_camions', models.IntegerField(choices=[(0, 'Aucun'), (1, '1'), (2, '2 et plus'), (9, 'Non déterminé')], verbose_name='Nombre de camions')),
                ('nombre_voitures', models.IntegerField(choices=[(0, 'Aucun'), (1, '1'), (2, '2 et plus'), (9, 'Non déterminé')], verbose_name='Nombre de voitures')),
                ('nombre_tracteurs', models.IntegerField(choices=[(0, 'Aucun'), (1, '1'), (2, '2 et plus'), (9, 'Non déterminé')], verbose_name='Nombre de tracteurs')),
                ('nombre_motocycles', models.IntegerField(choices=[(0, 'Aucun'), (1, '1'), (2, '2 et plus'), (9, 'Non déterminé')], verbose_name='Nombre de motocycles')),
                ('distance_route', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Distance à la route goudronnée (km)')),
                ('poids', models.DecimalField(blank=True, decimal_places=15, max_digits=16, null=True, verbose_name='Poids')),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modification', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ménage',
                'verbose_name_plural': 'Ménages',
                'ordering': ['region', 'province', 'numero_menage'],
            },
        ),
    ]
