import csv, os, sys
from manage import SETTINGS_MODULE

sys.path.insert(0, "C:\\Users\\James\\Documents/IIFYM/If_it_fits_your_maccies/Website")
print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE) 
import django
django.setup()

from calculator.models import Food

with open(r"C:\Users\James\Documents\IIFYM\If_it_fits_your_maccies/Nutrition.csv") as f:
    reader = csv.reader(f)
    next(reader) # skip first line
    for row in reader:
        db_row =  Food(
        name = row[0],
        cal = row[1],
        fat = row[2],
        sfat = row[3],
        tfat = row[4],
        chol = row[5],
        salt = row[6],
        carb = row[7],
        fbr = row[8],
        sgr = row[9],
        pro = row[10],
        category = row[11]
        )
        db_row.save()

#Food.objects.all() #Query Food table