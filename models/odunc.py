"""Ödünç alma modelini tanımlar."""

from utils.dogrulama import bos_mu_kontrol

VARSAYILAN_IADE_TARIHI = None


class Odunc:
    """Bir ödünç alma kaydını temsil eder."""

    def __init__(
        self,
        odunc_id,
        uye_id,
        isbn,
        odunc_tarihi,
        iade_tarihi=VARSAYILAN_IADE_TARIHI,
    ):
        """Ödünç nesnesini başlatır.

        Args:
            odunc_id: Benzersiz ödünç kimliği
            uye_id: Ödünç alan üyenin kimliği
            isbn: Ödünç alınan kitabın ISBN'i
            odunc_tarihi: Ödünç alma tarihi (string GG.AA.YYYY)
            iade_tarihi: İade tarihi (None ise henüz iade edilmemiş)
        """
        bos_mu_kontrol(odunc_id, "Ödünç ID")
        bos_mu_kontrol(uye_id, "Üye ID")
        bos_mu_kontrol(isbn, "ISBN")
        bos_mu_kontrol(odunc_tarihi, "Ödünç tarihi")
        self.__odunc_id = str(odunc_id).strip()
        self.__uye_id = str(uye_id).strip()
        self.__isbn = str(isbn).strip()
        self.__odunc_tarihi = odunc_tarihi
        self.__iade_tarihi = iade_tarihi
        self.__aktif = iade_tarihi is None

    @property
    def odunc_id(self):
        """Ödünç kimliğini döndürür."""
        return self.__odunc_id

    @property
    def uye_id(self):
        """Üye kimliğini döndürür."""
        return self.__uye_id

    @property
    def isbn(self):
        """ISBN'i döndürür."""
        return self.__isbn

    @property
    def odunc_tarihi(self):
        """Ödünç alma tarihini döndürür."""
        return self.__odunc_tarihi

    @property
    def iade_tarihi(self):
        """İade tarihini döndürür."""
        return self.__iade_tarihi

    @iade_tarihi.setter
    def iade_tarihi(self, deger):
        """İade tarihini günceller."""
        bos_mu_kontrol(deger, "İade tarihi")
        self.__iade_tarihi = deger
        self.__aktif = False

    @property
    def aktif(self):
        """Ödüncün aktif olup olmadığını döndürür."""
        return self.__aktif

    @aktif.setter
    def aktif(self, deger):
        """Ödüncün aktiflik durumunu günceller."""
        if not isinstance(deger, bool):
            raise ValueError("Aktiflik durumu True/False olmalıdır")
        self.__aktif = deger

    def to_dict(self):
        """Ödüncü sözlük formatına dönüştürür."""
        return {
            "odunc_id": self.__odunc_id,
            "uye_id": self.__uye_id,
            "isbn": self.__isbn,
            "odunc_tarihi": self.__odunc_tarihi,
            "iade_tarihi": self.__iade_tarihi,
            "aktif": self.__aktif,
        }

    @classmethod
    def from_dict(cls, veri):
        """Sözlükten Odunc nesnesi oluşturur."""
        odunc = cls(
            veri["odunc_id"],
            veri["uye_id"],
            veri["isbn"],
            veri["odunc_tarihi"],
            veri.get("iade_tarihi"),
        )
        odunc.aktif = veri.get("aktif", True)
        return odunc

    def __str__(self):
        """Ödüncü okunabilir formatta döndürür."""
        durum = "Aktif" if self.__aktif else "İade edildi"
        iade = self.__iade_tarihi or "---"
        return (
            f"[{self.__odunc_id}] Üye:{self.__uye_id} "
            f"ISBN:{self.__isbn} "
            f"Ödünç:{self.__odunc_tarihi} "
            f"İade:{iade} [{durum}]"
        )
