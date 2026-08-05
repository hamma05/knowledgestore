"""
Populate the database with Arabic Islamic books.

Run from the Django project directory with:
    python knowledgestore/popultatebd.py
"""

import os
import sys
from pathlib import Path

import django


PROJECT_DIR = Path(__file__).resolve().parents[1]

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from knowledgestore.models import Book


STATIC_IMAGE_BASE = "/static/knowledgestore/images"


def static_image(filename):
    return f"{STATIC_IMAGE_BASE}/{filename}"


BOOKS_DATA = [
    {"title": "صحيح البخاري", "author": "الإمام البخاري", "price": 130.0, "urlimg": static_image("bokhari.png")},
    {"title": "صحيح مسلم", "author": "الإمام مسلم", "price": 150.0, "urlimg": static_image("moslim.jpg")},
    {"title": "سنن أبي داود", "author": "الإمام أبو داود", "price": 180.0, "urlimg": static_image("SunanAbiDaoud.jpg")},
    {"title": "جامع الترمذي", "author": "الإمام الترمذي", "price": 120.0, "urlimg": static_image("images.jpg")},
    {"title": "سنن النسائي", "author": "الإمام النسائي", "price": 140.0, "urlimg": static_image("SunanAlNisaee.jpg")},
    {"title": "سنن ابن ماجه", "author": "الإمام ابن ماجه", "price": 99.0, "urlimg": static_image("ibn maja.jpg")},
    {"title": "موطأ الإمام مالك", "author": "الإمام مالك بن أنس", "price": 28.0, "urlimg": static_image("Mowata.jpg")},
    {"title": "رياض الصالحين", "author": "الإمام النووي", "price": 90.0, "urlimg": static_image("رياض_الصالحين.jpg")},
    {"title": "الأربعون النووية", "author": "الإمام النووي", "price": 12.0, "urlimg": static_image("6740315.jpg")},
    {"title": "الأذكار", "author": "الإمام النووي", "price": 22.0, "urlimg": static_image("adhkar.jpg")},
    {"title": "بلوغ المرام", "author": "ابن حجر العسقلاني", "price": 20.0, "urlimg": static_image("549_blugalmaram_alaskalni.jpg")},
    {"title": "فتح الباري شرح صحيح البخاري", "author": "ابن حجر العسقلاني", "price": 550.0, "urlimg": static_image("fathalbari.jpg")},
    {"title": "تفسير ابن كثير", "author": "الإمام ابن كثير", "price": 48.0, "urlimg": static_image("tafssir.jpg")},
    {"title": "زاد المعاد", "author": "ابن قيم الجوزية", "price": 32.0, "urlimg": static_image("zad elamad.jpg")},
    {"title": "مدارج السالكين", "author": "ابن قيم الجوزية", "price": 34.0, "urlimg": static_image("مدارج-السالكين-لابن-القيم.webp")},
    {"title": "الوابل الصيب", "author": "ابن قيم الجوزية", "price": 18.0, "urlimg": static_image("الوابل_الصيب_من_الكلم_الطيب.jpg")},
    {"title": "الفوائد", "author": "ابن قيم الجوزية", "price": 39.0, "urlimg": static_image("كتاب_الفوائد.jpg")},
    {"title": "إغاثة اللهفان", "author": "ابن قيم الجوزية", "price": 29.0, "urlimg": static_image("ighatha.jpg")},
    {"title": "كتاب التوحيد", "author": "محمد بن عبد الوهاب", "price": 15.0, "urlimg": static_image("tawhiid.jpg")},
    {"title": "كشف الشبهات", "author": "محمد بن عبد الوهاب", "price": 14.0, "urlimg": static_image("Pages-from-شرح-كشف-الشبهات-مجلد-1445-FB_50-scaled.jpg")},
    {"title": "العقيدة الطحاوية", "author": "الإمام الطحاوي", "price": 18.0, "urlimg": static_image("ata7awia.jpg")},
    {"title": "اقتضاء الصراط المستقيم", "author": "ابن تيمية", "price": 30.0, "urlimg": static_image("30060020.jpg")},
    {"title": "منهاج المسلم", "author": "أبو بكر جابر الجزائري", "price": 23.0, "urlimg": static_image("minhaj.jpg")},
    {"title": "فقه السنة", "author": "السيد سابق", "price": 27.0, "urlimg": static_image("فقه-السنة-1-scaled.webp-64bf9bb81dfa9.webp")},
    {"title": "الرحيق المختوم", "author": "صفي الرحمن المباركفوري", "price": 24.0, "urlimg": static_image("Arraheek_Almakhtoom.jpg")},
    {"title": "السيرة النبوية لابن هشام", "author": "ابن هشام", "price": 31.0, "urlimg": static_image("SeeretIbenHisham.jpg")},
    {"title": "الشمائل المحمدية", "author": "الإمام الترمذي", "price": 21.0, "urlimg": static_image("shamail.jpg")},
    {"title": "العقيدة الواسطية", "author": "ابن تيمية", "price": 20.0, "urlimg": static_image("alwasitiya.jpg")},
    {"title": "الشفا بتعريف حقوق المصطفى", "author": "القاضي عياض", "price": 26.0, "urlimg": static_image("shifa.jpg")},
    {"title": "إحياء علوم الدين", "author": "الإمام الغزالي", "price": 120.0, "urlimg": static_image("ihya.jpg")},
]


def populate_database():
    print("=" * 60)
    print("POPULATING DATABASE WITH ISLAMIC BOOKS")
    print("=" * 60)
    print()

    created_count = 0
    updated_count = 0
    removed_duplicates_count = 0

    for book_data in BOOKS_DATA:
        matching_books = Book.objects.filter(title=book_data["title"]).order_by("id")

        if matching_books.exists():
            book = matching_books.first()
            duplicates = matching_books.exclude(id=book.id)
            duplicate_count = duplicates.count()

            if duplicate_count:
                duplicates.delete()
                removed_duplicates_count += duplicate_count

            book.author = book_data["author"]
            book.price = book_data["price"]
            book.urlimg = book_data["urlimg"]
            book.save(update_fields=["author", "price", "urlimg"])
            created = False
        else:
            book = Book.objects.create(
                title=book_data["title"],
                author=book_data["author"],
                price=book_data["price"],
                urlimg=book_data["urlimg"],
            )
            created = True

        if created:
            print(f"Created: {book.title} - {book.author}")
            created_count += 1
        else:
            print(f"Updated: {book.title} - {book.author}")
            updated_count += 1

    print()
    print("=" * 60)
    print("SUMMARY:")
    print(f"  - Created: {created_count} books")
    print(f"  - Updated: {updated_count} books")
    print(f"  - Removed duplicates: {removed_duplicates_count} books")
    print(f"  - Total in database: {Book.objects.count()} books")
    print("=" * 60)
    print()
    print("Database populated successfully!")


if __name__ == "__main__":
    populate_database()
