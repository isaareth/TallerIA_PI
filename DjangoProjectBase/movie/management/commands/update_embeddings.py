import numpy as np
import os
from django.core.management.base import BaseCommand
from movie.models import Movie
from openai import OpenAI
from dotenv import load_dotenv

class Command(BaseCommand):
    help = 'Actualiza los embeddings de todas las películas usando OpenAI'

    def handle(self, *args, **kwargs):
        load_dotenv('./openAI.env')
        client = OpenAI(api_key=os.environ.get('openai_api_key'))

        total = Movie.objects.count()
        actualizadas = 0

        for movie in Movie.objects.all():
            if not movie.description:
                self.stdout.write(f"❌ {movie.title} no tiene descripción.")
                continue

            try:
                response = client.embeddings.create(
                    input=[movie.description],
                    model="text-embedding-3-small"
                )
                emb = np.array(response.data[0].embedding, dtype=np.float32)
                movie.emb = emb.tobytes()
                movie.save()
                actualizadas += 1
                self.stdout.write(f"✅ Embedding actualizado: {movie.title}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error con {movie.title}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"\n🎉 ¡Listo! Se actualizaron {actualizadas} de {total} películas."))
