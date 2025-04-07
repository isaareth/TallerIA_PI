import os
from django.core.management.base import BaseCommand
from movie.models import Movie
from django.conf import settings

class Command(BaseCommand):
    help = "Update movie images from media folder"

    def handle(self, *args, **kwargs):
        # 📂 Ruta a la carpeta de imágenes
        images_folder = os.path.join(settings.MEDIA_ROOT, "movie/images/")
        
        if not os.path.exists(images_folder):
            self.stderr.write(self.style.ERROR(f"Folder '{images_folder}' not found."))
            return
        
        updated_count = 0
        
        # 🔍 Recorremos todas las películas en la base de datos
        for movie in Movie.objects.all():
            expected_filename = f"m_{movie.title}.png"
            image_path = os.path.join(images_folder, expected_filename)
            
            if os.path.exists(image_path):
                # ✅ Guardamos la ruta relativa en la base de datos
                movie.image = f"movie/images/{expected_filename}"
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated: {movie.title}"))
            else:
                self.stderr.write(self.style.WARNING(f"Image not found for: {movie.title}"))

        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movie images."))
