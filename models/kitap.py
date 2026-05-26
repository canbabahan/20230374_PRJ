"""Kitap modelini tanımlar."""

from utils.dogrulama import (
    isbn_dogrula,
    bos_mu_kontrol,
    yil_dogrula,
)

GECERLI_YIL_MIN = 1000
GECERLI_YIL_MAX = 2100


class Kitap:
    """Kütüphane sistemindeki bir kitabı temsil eder."""

    def __init__(self, isbn, kitap_adi, yazar, yil):
        """Kitap nesnesini başlatır.

        Args:
            isbn: Kitabın ISBN numarası (10 veya 13 hane)
            kitap_adi: Kitabın adı
            yazar: Kitabın yazarı
            yil: Yayın yılı
        """
        self.__isbn = isbn_dogrula(isbn)
        bos_mu_kontrol(kitap_adi, "Kitap adı")
        bos_mu_kontrol(yazar, "Yazar")
        self.__kitap_adi = kitap_adi.strip()
        self.__yazar = yazar.strip()
        self.__yil = yil_dogrula(yil, GECERLI_YIL_MIN, GECERLI_YIL_MAX)
        self.__musait = True

    @property
    def isbn(self):
        """ISBN numarasını döndürür."""
        return self.__isbn

    @property
    def kitap_adi(self):
        """Kitap adını döndürür."""
        return self.__kitap_adi

    @kitap_adi.setter
    def kitap_adi(self, deger):
        """Kitap adını günceller."""
        bos_mu_kontrol(deger, "Kitap adı")
        self.__kitap_adi = deger.strip()

    @property
    def yazar(self):
        """Yazarı döndürür."""
        return self.__yazar

    @yazar.setter
    def yazar(self, deger):
        """Yazarı günceller."""
        bos_mu_kontrol(deger, "Yazar")
        self.__yazar = deger.strip()

    @property
    def yil(self):
        """Yayın yılını döndürür."""
        return self.__yil

    @property
    def musait(self):
        """Kitabın müsait olup olmadığını döndürür."""
        return self.__musait

    @musait.setter
    def musait(self, deger):
        """Kitabın müsaitlik durumunu günceller."""
        if not isinstance(deger, bool):
            raise ValueError(
                "Müsaitlik durumu True veya False olmalıdır"
            )
        self.__musait = deger

    def to_dict(self):
        """Kitabı sözlük formatına dönüştürür."""
        return {
            "isbn": self.__isbn,
            "kitap_adi": self.__kitap_adi,
            "yazar": self.__yazar,
            "yil": self.__yil,
            "musait": self.__musait,
        }

    @classmethod
    def from_dict(cls, veri):
        """Sözlükten Kitap nesnesi oluşturur.

        Args:
            veri: Kitap verilerini içeren sözlük

        Returns:
            Kitap nesnesi
        """
        kitap = cls(
            veri["isbn"],
            veri["kitap_adi"],
            veri["yazar"],
            veri["yil"],
        )
        kitap.musait = veri.get("musait", True)
        return kitap

    def __str__(self):
        """Kitabı okunabilir formatta döndürür."""
        durum = "Müsait" if self.__musait else "Ödünçte"
        return (
            f"[{self.__isbn}] {self.__kitap_adi} - "
            f"{self.__yazar} ({self.__yil}) [{durum}]"
        )

    def __repr__(self):
        """Kitabın teknik temsilini döndürür."""
        return (
            f"Kitap(isbn={self.__isbn!r}, "
            f"kitap_adi={self.__kitap_adi!r})"
        )
