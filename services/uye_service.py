"""Üye işlemlerini yönetir."""

from models.uye import Uye, OgrenciUye
from utils.dogrulama import bos_mu_kontrol, UyeBulunamadiHatasi
from utils.dosya_isle import dosyaya_kaydet, dosyadan_yukle

UYE_DOSYASI = "uyeler"
UYE_TURU_OGRENCI = "ogrenci_uye"


class UyeService:
    """Üye kayıt, silme ve listeleme işlemlerini yönetir."""

    def __init__(self, veri_dizini=None):
        """UyeService nesnesini başlatır.

        Args:
            veri_dizini: Veri dosyalarının saklanacağı dizin
        """
        self.__veri_dizini = veri_dizini
        self.__uyeler = {}
        self._yukle()

    def uye_ekle(self, uye_id, ad, soyad, email):
        """Sisteme standart üye ekler.

        Args:
            uye_id: Benzersiz üye kimliği
            ad: Üyenin adı
            soyad: Üyenin soyadı
            email: Üyenin email adresi

        Raises:
            ValueError: Üye ID zaten kayıtlı ise
        """
        self._id_benzersiz_mi_kontrol(uye_id)
        uye = Uye(uye_id, ad, soyad, email)
        self.__uyeler[str(uye_id).strip()] = uye
        self._kaydet()
        return uye

    def ogrenci_uye_ekle(
        self, uye_id, ad, soyad, email, ogrenci_no, bolum
    ):
        """Sisteme öğrenci üye ekler.

        Args:
            uye_id: Benzersiz üye kimliği
            ad: Öğrencinin adı
            soyad: Öğrencinin soyadı
            email: Öğrencinin email adresi
            ogrenci_no: Öğrenci numarası
            bolum: Öğrencinin bölümü

        Raises:
            ValueError: Üye ID zaten kayıtlı ise
        """
        self._id_benzersiz_mi_kontrol(uye_id)
        uye = OgrenciUye(
            uye_id, ad, soyad, email, ogrenci_no, bolum
        )
        self.__uyeler[str(uye_id).strip()] = uye
        self._kaydet()
        return uye

    def uye_getir(self, uye_id):
        """ID ile üye getirir.

        Args:
            uye_id: Aranacak üye kimliği

        Returns:
            Uye veya OgrenciUye nesnesi

        Raises:
            UyeBulunamadiHatasi: Üye bulunamazsa
        """
        bos_mu_kontrol(uye_id, "Üye ID")
        temiz_id = str(uye_id).strip()
        if temiz_id not in self.__uyeler:
            raise UyeBulunamadiHatasi(
                f"Üye bulunamadı: {temiz_id}"
            )
        return self.__uyeler[temiz_id]

    def uye_sil(self, uye_id):
        """Sistemden üye siler.

        Args:
            uye_id: Silinecek üye kimliği
        """
        self.uye_getir(uye_id)
        del self.__uyeler[str(uye_id).strip()]
        self._kaydet()

    def tum_uyeleri_listele(self):
        """Tüm üyeleri döndürür."""
        return list(self.__uyeler.values())

    def _id_benzersiz_mi_kontrol(self, uye_id):
        """Üye ID'nin benzersiz olduğunu kontrol eder."""
        bos_mu_kontrol(uye_id, "Üye ID")
        if str(uye_id).strip() in self.__uyeler:
            raise ValueError(
                f"Üye ID '{uye_id}' zaten kayıtlı"
            )

    def _uye_nesnesini_olustur(self, veri):
        """Sözlükten doğru üye tipini oluşturur."""
        if veri.get("tur") == UYE_TURU_OGRENCI:
            return OgrenciUye.from_dict(veri)
        return Uye.from_dict(veri)

    def _yukle(self):
        """Üyeleri JSON dosyasından yükler."""
        ham_veri = dosyadan_yukle(UYE_DOSYASI, self.__veri_dizini)
        self.__uyeler = {
            uid: self._uye_nesnesini_olustur(veri)
            for uid, veri in ham_veri.items()
        }

    def _kaydet(self):
        """Üyeleri JSON dosyasına kaydeder."""
        kayit_verisi = {
            uid: u.to_dict()
            for uid, u in self.__uyeler.items()
        }
        dosyaya_kaydet(UYE_DOSYASI, kayit_verisi, self.__veri_dizini)
