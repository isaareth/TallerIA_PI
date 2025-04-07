import numpy as np
import random
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "View the embeddings of a random movie stored in the database"

    def handle(self, *args, **kwargs):
        # ✅ Fetch all movies that have embeddings stored
        movies_with_embeddings = Movie.objects.exclude(emb=None)
        
        if not movies_with_embeddings.exists():
            self.stderr.write("❌ No movies with stored embeddings found.")
            return
        
        # ✅ Select a random movie
        movie = random.choice(movies_with_embeddings)
        
        # ✅ Convert binary embeddings back to numpy array
        embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
        
        # ✅ Display the movie title and first 5 values of its embeddings
        self.stdout.write(self.style.SUCCESS(f"🎬 Movie: {movie.title}"))
        self.stdout.write(f"🧬 Embedding (first 5 values): {embedding_vector[:5]}")


# cada vez mas personas usan ia para generar código en segudos y deasarrollar software con los resultados obtenidos 
# sin preocuparse por la logica o estructura del mismo, esta corriente es conocida como vibe coding 


# 
