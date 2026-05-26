"""Üye modellerini tanımlar (Uye ve OgrenciUye)."""

from utils.dogrulama import bos_mu_kontrol, email_dogrula

STANDART_ODUNC_LIMITI = 3
OGRENCI_ODUNC_LIMITI = 5


class Uye:
    """Kütüphane üyesini temsil eden temel sınıf."""

    ODUNC_LIMITI = STANDART_ODUNC_LIMITI

    def __init__(self, uye_id, ad, soyad, email):
        """Üye nesnesini başlatır.

        Args:
            uye_id: Benzersiz üye kimliği
            ad: Üyenin adı
            soyad: Üyenin soyadı
            email: Üyenin email adresi
        """
        bos_mu_kontrol(uye_id, "Üye ID")
        bos_mu_kontrol(ad, "Ad")
        bos_mu_kontrol(soyad, "Soyad")
        self.__uye_id = str(uye_id).strip()
        self.__ad = ad.strip()
        self.__soyad = soyad.strip()
        self.__email = email_dogrula(email)
        self.__aktif = True

    @property
    def uye_id(self):
        """Üye kimliğini döndürür."""
        return self.__uye_id

    @property
    def ad(self):
        """Adı döndürür."""
        return self.__ad

    @ad.setter
    def ad(self, deger):
        """Adı günceller."""
        bos_mu_kontrol(deger, "Ad")
        self.__ad = deger.strip()

    @property
    def soyad(self):
        """Soyadı döndürür."""
        return self.__soyad

    @soyad.setter
    def soyad(self, deger):
        """Soyadı günceller."""
        bos_mu_kontrol(deger, "Soyad")
        self.__soyad = deger.strip()

    @property
    def email(self):
        """Email adresini döndürür."""
        return self.__email

    @email.setter
    def email(self, deger):
        """Email adresini günceller."""
        self.__email = email_dogrula(deger)

    @property
    def aktif(self):
        """Üyenin aktif olup olmadığını döndürür."""
        return self.__aktif

    @aktif.setter
    def aktif(self, deger):
        """Üye aktiflik durumunu günceller."""
        if not isinstance(deger, bool):
            raise ValueError("Aktiflik durumu True/False olmalıdır")
        self.__aktif = deger

    def odunc_limit_al(self):
        """Üye için geçerli ödünç limitini döndürür."""
        return self.ODUNC_LIMITI

    def to_dict(self):
        """Üyeyi sözlük formatına dönüştürür."""
        return {
            "tur": "uye",
            "uye_id": self.__uye_id,
            "ad": self.__ad,
            "soyad": self.__soyad,
            "email": self.__email,
            "aktif": self.__aktif,
        }

    @classmethod
    def from_dict(cls, veri):
        """Sözlükten Uye nesnesi oluşturur."""
        uye = cls(
            veri["uye_id"],
            veri["ad"],
            veri["soyad"],
            veri["email"],
        )
        uye.aktif = veri.get("aktif", True)
        return uye

    def __str__(self):
        """Üyeyi okunabilir formatta döndürür."""
        durum = "Aktif" if self.__aktif else "Pasif"
        return (
            f"[{self.__uye_id}] {self.__ad} {self.__soyad} "
            f"<{self.__email}> [{durum}]"
        )

    def __repr__(self):
        """Üyenin teknik temsilini döndürür."""
        return (
            f"Uye(uye_id={self.__uye_id!r}, "
            f"ad={self.__ad!r})"
        )


class OgrenciUye(Uye):
    """Öğrenci üyeyi temsil eden sınıf; Uye'den türetilmiştir."""

    ODUNC_LIMITI = OGRENCI_ODUNC_LIMITI

    def __init__(
        self, uye_id, ad, soyad, email, ogrenci_no, bolum
    ):
        """Öğrenci üye nesnesini başlatır.

        Args:
            uye_id: Benzersiz üye kimliği
            ad: Öğrencinin adı
            soyad: Öğrencinin soyadı
            email: Öğrencinin email adresi
            ogrenci_no: Öğrenci numarası
            bolum: Öğrencinin bölümü
        """
        super().__init__(uye_id, ad, soyad, email)
        bos_mu_kontrol(ogrenci_no, "Öğrenci numarası")
        bos_mu_kontrol(bolum, "Bölüm")
        self.__ogrenci_no = str(ogrenci_no).strip()
        self.__bolum = bolum.strip()

    @property
    def ogrenci_no(self):
        """Öğrenci numarasını döndürür."""
        return self.__ogrenci_no

    @property
    def bolum(self):
        """Bölümü döndürür."""
        return self.__bolum

    def odunc_limit_al(self):
        """Öğrenci için geçerli ödünç limitini döndürür."""
        return self.ODUNC_LIMITI

    def to_dict(self):
        """Öğrenci üyeyi sözlük formatına dönüştürür."""
        veri = super().to_dict()
        veri["tur"] = "ogrenci_uye"
        veri["ogrenci_no"] = self.__ogrenci_no
        veri["bolum"] = self.__bolum
        return veri

    @classmethod
    def from_dict(cls, veri):
        """Sözlükten OgrenciUye nesnesi oluşturur."""
        uye = cls(
            veri["uye_id"],
            veri["ad"],
            veri["soyad"],
            veri["email"],
            veri["ogrenci_no"],
            veri["bolum"],
        )
        uye.aktif = veri.get("aktif", True)
        return uye

    def __str__(self):
        """Öğrenci üyeyi okunabilir formatta döndürür."""
        temel = super().__str__()
        return f"{temel} - Öğrenci: {self.__ogrenci_no} ({self.__bolum})"
