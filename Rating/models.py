from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


# Erweiterung des User Models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()

    def __str__(self) -> str:
        return self.user.username


# Klasse für die Bierstile: Pils, Kölsch, Weizen, etc.
class Beertype(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brewing_type = models.CharField(max_length=255)
    Color = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self) -> str:
        return self.name


# Klasse für die Basisdaten der Brauereien bzw. Hersteller der Biere
class Brewery(models.Model):
    name = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    founded_year = models.IntegerField()
    description = models.TextField()
    thumbnail = models.ImageField(
        upload_to="BreweryPictures/",
        blank=True,
        null=True
    )
 
    def __str__(self):
        return self.name


# Klasse für die Basisdaten der einzelnen Biersorten
class Beer(models.Model):
    # Primärschlüssel
    id = models.AutoField(primary_key=True)
    approvalstatus = models.BooleanField(default=False)

    # Brauerei -> Fremdschlüssel des Typs Brauerei
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=100)

    # Stil -> Pils, Kölsch...
    style = models.ForeignKey(Beertype, on_delete=models.CASCADE)

    # Volumenprozent Alkoholgehalt
    alcohol_content = models.DecimalField(max_digits=4, decimal_places=2)

    # Die Stammwürze des Biers.
    original_gravity = models.DecimalField(max_digits=4, decimal_places=2)

    # Empfohlene Trinktemperatur
    recommended_serving_temperature = models.IntegerField()

    # Biobier
    is_organic = models.BooleanField()

    # Klarheit des Bieres
    clarity = models.CharField(max_length=100)

    # Die verwendete Hefe für das Bier.
    yeast = models.CharField(max_length=100)

    # Glutenfrei
    is_gluten_free = models.BooleanField()

    # Freitext für eine Beschreibung
    description = models.TextField()
    
    #Zähler für die Anzahl von Bewertungen
    ratings_count = models.IntegerField(default=0, blank=True, null=True)
    
    #Zähler für die Anzahl von 'recommendet' in Bewertungen
    recommended_count = models.IntegerField(default=0, blank=True, null=True)
    
  
    def __str__(self):
        return f"{self.display_name}"


# Klasse für die Bewertungen
class Rating(models.Model):
    # Bezug auf das Bier
    beer = models.ForeignKey(Beer, on_delete=models.CASCADE)

    # Bezug auf den bewertenden User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Color (1-10)
    Color = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Entry (1-10)
    Entry = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Körper (1-10)
    body = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Abgang (1-10)
    finish = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Kohlensäure (1-10)
    carbonation = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Säure (1-10)
    acidity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Bitterkeit (1-10)
    bitterness = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Süffigkeit (1-10)
    drinkability = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    # Price (1: €, 2: €€, 3: €€€)
    price = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(3)]
    )
    
    # Empfohlen: Ja/Nein
    recommended = models.BooleanField()

    #Zeitstempel
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.beer} Rating by {self.user.username}"

    class Meta:
        unique_together = ('beer', 'user')


class Recommendation(models.Model):
    #Name der Empfehlung
    name = models.CharField(max_length=255, unique=True)
    
    #Primary Key
    id = models.AutoField(primary_key=True)
    
    #Link auf empfohlenes Bier
    beer = models.ForeignKey('Beer', on_delete=models.CASCADE)

    # Anzeige im Admin Panel soll name der Recommendation sein
    def __str__(self):
        return f"{self.name}"
    

class BlogEntry(models.Model):
    #Primary Key
    id = models.AutoField(primary_key=True)

    #Titel
    title = models.CharField(max_length=200)
    
    #Inhalt
    content = models.TextField()

    #Erstellungs Zeitstempel
    created_at = models.DateTimeField(auto_now_add=True)
    
    #Autor -> User Bezug
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #Zähler für Upvotes
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


    #Methode für Upvotes
    def upvote(self):
        self.upvotes += 1
        self.save()


#Klasse für Sprüche
class Phrase(models.Model):
    #Primary Key
    id = models.AutoField(primary_key=True)

    #Spruch
    phrase = models.CharField(max_length=400)

    #Zur Benutzung in Fließtext
    intextphrase = models.CharField(max_length=400)

    def __str__(self) -> str:
        return self.phrase