"""Input doğrulama fonksiyonları."""

import re
from datetime import datetime

ISBN_UZUNLUK_10 = 10
ISBN_UZUNLUK_13 = 13
TARIH_FORMATI = "%d.%m.%Y"
EMAIL_REGEX = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
ISBN_REGEX = r'^\d{10}$|^\d{13}$'


class DogrulamaHatasi(ValueError):
    """Doğrulama işlemlerinde oluşan özel hata sınıfı."""
    pass


class KitapBulunamadiHatasi(Exception):
    """Kitap bulunamadığında fırlatılan özel hata sınıfı."""
    pass


class UyeBulunamadiHatasi(Exception):
    """Üye bulunamadığında fırlatılan özel hata sınıfı."""
    pass


class OduncLimitiAsimHatasi(Exception):
    """Ödünç limiti aşıldığında fırlatılan özel hata sınıfı."""
    pass


def bos_mu_kontrol(deger, alan_adi="Alan"):
    """Değerin boş olmadığını kontrol eder.

    Args:
        deger: Kontrol edilecek değer
        alan_adi: Hata mesajında kullanılacak alan adı

    Raises:
        DogrulamaHatasi: Değer boş ise
    """
    if deger is None or (
        isinstance(deger, str) and not deger.strip()
    ):
        raise DogrulamaHatasi(f"{alan_adi} boş olamaz")
    return True


def isbn_dogrula(isbn):
    """ISBN formatını doğrular (10 veya 13 haneli).

    Args:
        isbn: Doğrulanacak ISBN değeri

    Returns:
        Temizlenmiş ISBN string'i

    Raises:
        DogrulamaHatasi: ISBN geçersiz ise
    """
    bos_mu_kontrol(isbn, "ISBN")
    isbn_temiz = str(isbn).replace("-", "").replace(" ", "")
    if not re.match(ISBN_REGEX, isbn_temiz):
        raise DogrulamaHatasi(
            f"Geçersiz ISBN formatı: {isbn}. "
            f"10 veya 13 haneli olmalıdır."
        )
    return isbn_temiz


def tarih_dogrula(tarih_str):
    """Tarih formatını doğrular (GG.AA.YYYY).

    Args:
        tarih_str: Doğrulanacak tarih string'i

    Returns:
        datetime nesnesi

    Raises:
        DogrulamaHatasi: Tarih geçersiz ise
    """
    bos_mu_kontrol(tarih_str, "Tarih")
    try:
        return datetime.strptime(tarih_str.strip(), TARIH_FORMATI)
    except ValueError:
        raise DogrulamaHatasi(
            f"Geçersiz tarih formatı: {tarih_str}. "
            f"GG.AA.YYYY formatında giriniz."
        )


def email_dogrula(email):
    """Email adresini doğrular.

    Args:
        email: Doğrulanacak email adresi

    Returns:
        Temizlenmiş email string'i

    Raises:
        DogrulamaHatasi: Email geçersiz ise
    """
    bos_mu_kontrol(email, "Email")
    email_temiz = email.strip()
    if not re.match(EMAIL_REGEX, email_temiz):
        raise DogrulamaHatasi(
            f"Geçersiz email formatı: {email}"
        )
    return email_temiz


def yil_dogrula(yil, min_yil=1000, max_yil=2100):
    """Yayın yılını doğrular.

    Args:
        yil: Doğrulanacak yıl değeri
        min_yil: İzin verilen minimum yıl
        max_yil: İzin verilen maksimum yıl

    Returns:
        int olarak yıl

    Raises:
        DogrulamaHatasi: Yıl geçersiz ise
    """
    try:
        yil_int = int(yil)
    except (TypeError, ValueError):
        raise DogrulamaHatasi("Yıl sayısal bir değer olmalıdır")
    if not (min_yil <= yil_int <= max_yil):
        raise DogrulamaHatasi(
            f"Yıl {min_yil} ile {max_yil} arasında olmalıdır"
        )
    return yil_int
