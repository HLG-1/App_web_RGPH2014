# management/commands/import_recensement.py
import csv
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from recensement.models import Individu  # Remplacez par le nom de votre app

class Command(BaseCommand):
    help = 'Importe les données de recensement depuis un fichier CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Chemin vers le fichier CSV')
        parser.add_argument('--batch-size', type=int, default=1000, help='Taille des lots pour l\'import')
        parser.add_argument('--skip-header', action='store_true', help='Ignorer la première ligne')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        batch_size = options['batch_size']
        skip_header = options['skip_header']
        
        self.stdout.write(f"Début de l'import depuis {csv_file}")
        self.stdout.write(f"Taille des lots: {batch_size}")
        
        start_time = time.time()
        total_created = 0
        batch = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                
                # Ignorer l'en-tête si nécessaire
                if skip_header:
                    next(reader)
                
                for row_num, row in enumerate(reader, 1):
                    try:
                        # Fonction pour convertir en int (gère les décimaux)
                        def safe_int(value):
                            if not value or value == '':
                                return None
                            try:
                                return int(float(value))  # Convertir d'abord en float puis en int
                            except ValueError:
                                return None
                        
                        def safe_float(value):
                            if not value or value == '':
                                return None
                            try:
                                return float(value)
                            except ValueError:
                                return None
                        
                        # Créer l'objet Individu (adapter selon l'ordre des colonnes dans votre CSV)
                        individu = Individu(
                            region=safe_int(row[0]),
                            province=safe_int(row[1]),
                            milieu=safe_int(row[2]),
                            numero_menage_province=safe_int(row[3]),
                            numero_ordre_menage=safe_int(row[4]),
                            lien_chef_menage=safe_int(row[5]),
                            nationalite=safe_int(row[6]),
                            sexe=safe_int(row[7]),
                            age_simple=safe_int(row[8]),
                            age_quinquennal=safe_int(row[9]),
                            etat_matrimonial=safe_int(row[10]),
                            enfants_vivants=safe_int(row[11]),
                            enfants_decedes=safe_int(row[12]),
                            naissances_vivantes_12m=safe_int(row[13]),
                            deces_12m=safe_int(row[14]),
                            handicap_vision=safe_int(row[15]),
                            handicap_audition=safe_int(row[16]),
                            handicap_mobilite=safe_int(row[17]),
                            handicap_memoire=safe_int(row[18]),
                            handicap_entretien=safe_int(row[19]),
                            handicap_communication=safe_int(row[20]),
                            situation_handicap=safe_int(row[21]),
                            niveau_etudes=safe_int(row[22]),
                            niveau_etudes_agriculture=safe_int(row[23]),
                            secteur_enseignement=safe_int(row[24]),
                            scolarisation=safe_int(row[25]),
                            lieu_etudes=safe_int(row[26]),
                            mode_transport_etudes=safe_int(row[27]),
                            aptitude_lecture_ecriture=safe_int(row[28]),
                            langue_1=safe_int(row[29]),
                            langue_2=safe_int(row[30]),
                            langue_3=safe_int(row[31]),
                            langue_locale_1=safe_int(row[32]),
                            langue_locale_2=safe_int(row[33]),
                            diplome_superieur_general=safe_int(row[34]),
                            diplome_general=safe_int(row[35]),
                            diplome_formation_professionnelle_superieur=safe_int(row[36]),
                            diplome_formation_professionnelle_general=safe_int(row[37]),
                            diplome_formation_professionnelle_base=safe_int(row[38]),
                            type_activite=safe_int(row[39]),
                            profession_superieur_general=safe_int(row[40]),
                            profession_general=safe_int(row[41]),
                            statut_professionnel=safe_int(row[42]),
                            activite_economique_superieur=safe_int(row[43]),
                            activite_economique_general=safe_int(row[44]),
                            lieu_travail=safe_int(row[45]),
                            mode_transport_travail=safe_int(row[46]),
                            poids=safe_float(row[47]),
                        )
                        
                        batch.append(individu)
                        
                        # Insérer par lots pour optimiser les performances
                        if len(batch) >= batch_size:
                            with transaction.atomic():
                                Individu.objects.bulk_create(batch, ignore_conflicts=True)
                            total_created += len(batch)
                            batch = []
                            
                            # Afficher le progrès
                            if total_created % (batch_size * 10) == 0:
                                elapsed = time.time() - start_time
                                self.stdout.write(f"Importé {total_created} lignes en {elapsed:.2f}s")
                    
                    except (ValueError, IndexError) as e:
                        self.stdout.write(f"Erreur ligne {row_num}: {e}")
                        continue
                
                # Insérer le dernier lot
                if batch:
                    with transaction.atomic():
                        Individu.objects.bulk_create(batch, ignore_conflicts=True)
                    total_created += len(batch)
                
                elapsed = time.time() - start_time
                self.stdout.write(
                    self.style.SUCCESS(f'Import terminé avec succès!')
                )
                self.stdout.write(f"Total importé: {total_created} lignes")
                self.stdout.write(f"Temps total: {elapsed:.2f}s")
                self.stdout.write(f"Vitesse: {total_created/elapsed:.0f} lignes/sec")
                
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Fichier non trouvé: {csv_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erreur lors de l\'import: {e}')
            )