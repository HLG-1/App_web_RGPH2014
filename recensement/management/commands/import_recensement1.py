# management/commands/import_menage.py
import csv
import time
from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand
from django.db import transaction
from recensement.models import Menage  # Remplacez par le nom de votre app

class Command(BaseCommand):
    help = 'Importe les données de ménages depuis un fichier CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Chemin vers le fichier CSV')
        parser.add_argument('--batch-size', type=int, default=1000, help='Taille des lots pour l\'import')
        parser.add_argument('--skip-header', action='store_true', help='Ignorer la première ligne')
        parser.add_argument('--encoding', type=str, default='utf-8', help='Encodage du fichier CSV')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        batch_size = options['batch_size']
        skip_header = options['skip_header']
        encoding = options['encoding']
        
        self.stdout.write(f"Début de l'import depuis {csv_file}")
        self.stdout.write(f"Taille des lots: {batch_size}")
        self.stdout.write(f"Encodage: {encoding}")
        
        start_time = time.time()
        total_created = 0
        total_errors = 0
        batch = []
        
        try:
            with open(csv_file, 'r', encoding=encoding) as file:
                reader = csv.reader(file)
                
                # Ignorer l'en-tête si nécessaire
                if skip_header:
                    next(reader)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Fonction pour convertir en int (gère les décimaux)
                        def safe_int(value, default=None):
                            if not value or value == '' or value == 'NULL' or value.lower() == 'null':
                                return default
                            try:
                                return int(float(value))  # Convertir d'abord en float puis en int
                            except (ValueError, TypeError):
                                return default
                        
                        # Fonction pour convertir en int avec valeur par défaut obligatoire
                        def safe_int_required(value, default=9):
                            """Pour les champs obligatoires, utilise 9 (Non déterminé) par défaut"""
                            result = safe_int(value, default)
                            return result if result is not None else default
                        
                        def safe_decimal(value):
                            if not value or value == '' or value == 'NULL' or value.lower() == 'null':
                                return None
                            try:
                                return Decimal(str(value))
                            except (ValueError, TypeError, InvalidOperation):
                                return None
                        
                        # Vérifier que nous avons assez de colonnes
                        if len(row) < 40:  # Ajustez selon le nombre de colonnes attendues
                            self.stdout.write(f"Ligne {row_num}: Nombre de colonnes insuffisant ({len(row)})")
                            total_errors += 1
                            continue
                        
                        # Créer l'objet Menage (adapter selon l'ordre des colonnes dans votre CSV)
                        menage = Menage(
                            # Localisation - champs obligatoires
                            region=safe_int_required(row[0], 99),  # 99 = Information identifiante
                            province=safe_int_required(row[1], 999),  # 999 = Information identifiante
                            milieu=safe_int_required(row[2], 9),  # 9 = Information identifiante
                            
                            # Composition du ménage - champs obligatoires
                            numero_menage=safe_int_required(row[3], 1),
                            taille_menage=safe_int_required(row[4], 1),
                            type_menage=safe_int_required(row[5], 9),  # 9 = Non déterminé
                            
                            # Caractéristiques du logement - champs obligatoires
                            type_logement=safe_int_required(row[6], 9),  # 9 = Non déterminé
                            materiaux_murs=safe_int_required(row[7], 7),  # 7 = Autres
                            materiaux_toit=safe_int_required(row[8], 6),  # 6 = Autres
                            materiaux_sol=safe_int_required(row[9], 5),  # 5 = Autre
                            age_logement=safe_int_required(row[10], 9),  # 9 = Non déterminé
                            nombre_pieces=safe_int(row[11]),  # Peut être null
                            statut_occupation=safe_int_required(row[12], 9),  # 9 = Non déterminé
                            
                            # Équipements du logement - champs obligatoires
                            cuisine=safe_int_required(row[13], 3),  # 3 = Non disponible
                            wc=safe_int_required(row[14], 3),  # 3 = Non disponibles
                            baignoire_douche=safe_int_required(row[15], 3),  # 3 = Non disponible
                            bain_local=safe_int_required(row[16], 3),  # 3 = Non disponible
                            
                            # Services publics - champs obligatoires
                            mode_eclairage=safe_int_required(row[17], 9),  # 9 = Non déterminé (hors réseau public)
                            mode_eau=safe_int_required(row[18], 9),  # 9 = Non déterminé (hors réseau public)
                            distance_eau=safe_int_required(row[19], 8),  # 8 = Non déterminée
                            duree_eau=safe_int(row[20]),  # Peut être null
                            evacuation_eaux_usees=safe_int_required(row[21], 5),  # 5 = Autre
                            evacuation_dechets=safe_int_required(row[22], 4),  # 4 = Autre
                            
                            # Combustibles et énergie - champs obligatoires
                            utilisation_gaz=safe_int_required(row[23], 9),  # 9 = Non déterminé
                            utilisation_electricite=safe_int_required(row[24], 9),  # 9 = Non déterminé
                            utilisation_charbon=safe_int_required(row[25], 9),  # 9 = Non déterminé
                            utilisation_bois=safe_int_required(row[26], 9),  # 9 = Non déterminé
                            utilisation_dejections_animales=safe_int_required(row[27], 9),  # 9 = Non déterminées
                            
                            # Équipements électroniques - champs obligatoires
                            possede_television=safe_int_required(row[28], 9),  # 9 = Non déterminé
                            possede_radio=safe_int_required(row[29], 9),  # 9 = Non déterminé
                            possede_telephone_portable=safe_int_required(row[30], 9),  # 9 = Non déterminé
                            possede_telephone_fixe=safe_int_required(row[31], 9),  # 9 = Non déterminé
                            possede_internet=safe_int_required(row[32], 9),  # 9 = Non déterminé
                            possede_ordinateur=safe_int_required(row[33], 9),  # 9 = Non déterminé
                            possede_parabole=safe_int_required(row[34], 9),  # 9 = Non déterminé
                            possede_refrigerateur=safe_int_required(row[35], 9),  # 9 = Non déterminé
                            
                            # Moyens de transport - champs obligatoires
                            nombre_camions=safe_int_required(row[36], 9),  # 9 = Non déterminé
                            nombre_voitures=safe_int_required(row[37], 9),  # 9 = Non déterminé
                            nombre_tracteurs=safe_int_required(row[38], 9),  # 9 = Non déterminé
                            nombre_motocycles=safe_int_required(row[39], 9),  # 9 = Non déterminé
                            
                            # Accessibilité - peut être null
                            distance_route=safe_int(row[40]) if len(row) > 40 else None,
                            
                            # Métadonnées - peut être null
                            poids=safe_decimal(row[41]) if len(row) > 41 else None,
                        )
                        
                        # Validation supplémentaire des champs critiques
                        if not all([
                            menage.region and menage.region != 0,
                            menage.province and menage.province != 0,
                            menage.milieu and menage.milieu != 0,
                            menage.numero_menage and menage.numero_menage != 0,
                            menage.taille_menage and menage.taille_menage != 0
                        ]):
                            self.stdout.write(f"Ligne {row_num}: Champs obligatoires manquants")
                            total_errors += 1
                            continue
                        
                        batch.append(menage)
                        
                        # Insérer par lots pour optimiser les performances
                        if len(batch) >= batch_size:
                            try:
                                with transaction.atomic():
                                    Menage.objects.bulk_create(batch, ignore_conflicts=True)
                                total_created += len(batch)
                                batch = []
                                
                                # Afficher le progrès
                                if total_created % (batch_size * 10) == 0:
                                    elapsed = time.time() - start_time
                                    self.stdout.write(f"Importé {total_created} lignes en {elapsed:.2f}s")
                            except Exception as e:
                                self.stdout.write(f"Erreur lors de l'insertion du lot: {e}")
                                total_errors += len(batch)
                                batch = []
                    
                    except (ValueError, IndexError) as e:
                        self.stdout.write(f"Erreur ligne {row_num}: {e}")
                        total_errors += 1
                        continue
                
                # Insérer le dernier lot
                if batch:
                    try:
                        with transaction.atomic():
                            Menage.objects.bulk_create(batch, ignore_conflicts=True)
                        total_created += len(batch)
                    except Exception as e:
                        self.stdout.write(f"Erreur lors de l'insertion du dernier lot: {e}")
                        total_errors += len(batch)
                
                elapsed = time.time() - start_time
                self.stdout.write(
                    self.style.SUCCESS(f'Import terminé!')
                )
                self.stdout.write(f"Total importé: {total_created} lignes")
                self.stdout.write(f"Total erreurs: {total_errors} lignes")
                self.stdout.write(f"Temps total: {elapsed:.2f}s")
                if total_created > 0:
                    self.stdout.write(f"Vitesse: {total_created/elapsed:.0f} lignes/sec")
                
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Fichier non trouvé: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de l\'import: {e}')
            )
            
    def validate_choices(self, value, choices_dict):
        """Valide qu'une valeur existe dans les choix du modèle"""
        if value is None:
            return True
        choice_values = [choice[0] for choice in choices_dict]
        return value in choice_values