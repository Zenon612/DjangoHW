import csv
import os
from django.core.management.base import BaseCommand
from catalog.models import Phone
from slugify import slugify
from datetime import datetime


class Command(BaseCommand):
    help = "Импорт телефонов из CSV-файла в базу данных"

    def handle(self, *args, **options):
        from django.conf import settings
        csv_path = os.path.join(settings.BASE_DIR, 'phones.csv')

        self.stdout.write(f"Путь к CSV: {csv_path}")

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f"Файл {csv_path} не найден!"))
            return

        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            rows = list(reader)
            self.stdout.write(f"Найдено строк в CSV: {len(rows)}")
            
            created = 0
            updated = 0
            errors = 0

            for row in rows:
                try:
                    price_str = row.get('price', '0').strip()
                    price = int(price_str) if price_str.isdigit() else 0
                    
                    release_date_str = row.get('release_date', '').strip()
                    release_date = None
                    if release_date_str:
                        try:
                            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
                        except ValueError:
                            self.stderr.write(f"Неверный формат даты для {row.get('name')}: {release_date_str}")
                    
                    lte_exists = row.get('lte_exists', '').strip().lower() in ('true', '1', 'yes', 'да')

                    slug = slugify(row['name'])

                    phone, is_created = Phone.objects.update_or_create(
                        slug=slug,
                        defaults={
                            'name': row['name'].strip(),
                            'price': price,
                            'image': row.get('image', '').strip(),
                            'release_date': release_date,
                            'lte_exists': lte_exists,
                        }
                    )

                    if is_created:
                        created += 1
                        self.stdout.write(f"Добавлен: {phone.name}")
                    else:
                        updated += 1

                except Exception as e:
                    errors += 1
                    self.stderr.write(self.style.ERROR(f"Ошибка при импорте строки {row}: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Импорт завершён! Создано: {created}, Обновлено: {updated}, Ошибок: {errors}"
            )
        )
