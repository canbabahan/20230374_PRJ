"""Ödünç alma ve iade işlemlerini yönetir."""

from datetime import datetime
from models.odunc import Odunc
from utils.dogrulama import (
    OduncLimitiAsimHatasi,
    KitapBulunamadiHatasi,
    UyeBulunamadiHatasi,
)
from utils.dosya_isle import dosyaya_kaydet, dosyadan_yukle

ODUNC_DOSYASI = "oduncler"
TARIH_FORMATI = "%d.%m.%Y"
ODUNC_ID_ONEKI = "ODC"


class OduncService:
    """Ödünç alma ve iade işlemlerini yönetir."""

    def __init__(self, kitap_service, uye_service, veri_dizini=None):
        """OduncService nesnesini başlatır.

        Args:
            kitap_service: KitapService örneği
            uye_service: UyeService örneği
            veri_dizini: Veri dosyalarının saklanacağı dizin
        """
        self.__kitap_service = kitap_service
        self.__uye_service = uye_service
        self.__veri_dizini = veri_dizini
        self.__oduncler = {}
        self._yukle()

    def odunc_al(self, uye_id, isbn):
        """Üye adına kitap ödünç verir.

        Args:
            uye_id: Ödünç alacak üyenin kimliği
            isbn: Ödünç alınacak kitabın ISBN'i

        Returns:
            Oluşturulan Odunc nesnesi

        Raises:
            UyeBulunamadiHatasi: Üye bulunamazsa
            KitapBulunamadiHatasi: Kitap bulunamazsa
            ValueError: Kitap müsait değilse
            OduncLimitiAsimHatasi: Limit aşılmışsa
        """
        uye = self.__uye_service.uye_getir(uye_id)
        kitap = self.__kitap_service.kitap_getir(isbn)
        self._musaitlik_kontrol(kitap)
        self._limit_kontrol(uye)
        odunc = self._odunc_kaydi_olustur(uye_id, kitap.isbn)
        kitap.musait = False
        self.__oduncler[odunc.odunc_id] = odunc
        self._kaydet()
        self.__kitap_service._kaydet()
        return odunc

    def iade_et(self, uye_id, isbn):
        """Ödünç alınan kitabı iade eder.

        Args:
            uye_id: İade edecek üyenin kimliği
            isbn: İade edilecek kitabın ISBN'i

        Returns:
            Güncellenen Odunc nesnesi

        Raises:
            ValueError: Aktif ödünç kaydı bulunamazsa
        """
        odunc = self._aktif_odunc_bul(uye_id, isbn)
        bugun = datetime.now().strftime(TARIH_FORMATI)
        odunc.iade_tarihi = bugun
        kitap = self.__kitap_service.kitap_getir(isbn)
        kitap.musait = True
        self._kaydet()
        self.__kitap_service._kaydet()
        return odunc

    def aktif_oduncleri_listele(self, uye_id=None):
        """Aktif ödünç kayıtlarını listeler.

        Args:
            uye_id: Belirli üyenin ödünçleri için (None ise tümü)

        Returns:
            Aktif Odunc nesnelerinin listesi
        """
        aktif = [o for o in self.__oduncler.values() if o.aktif]
        if uye_id is not None:
            aktif = [o for o in aktif if o.uye_id == str(uye_id)]
        return aktif

    def tum_oduncleri_listele(self):
        """Tüm ödünç kayıtlarını döndürür."""
        return list(self.__oduncler.values())

    def _musaitlik_kontrol(self, kitap):
        """Kitabın müsait olduğunu kontrol eder."""
        if not kitap.musait:
            raise ValueError(
                f"Kitap şu anda ödünçte: {kitap.isbn}"
            )

    def _limit_kontrol(self, uye):
        """Üyenin ödünç limitini aşmadığını kontrol eder."""
        aktif_sayisi = len(self.aktif_oduncleri_listele(uye.uye_id))
        if aktif_sayisi >= uye.odunc_limit_al():
            raise OduncLimitiAsimHatasi(
                f"Üye ödünç limitini aştı: {uye.uye_id} "
                f"(Limit: {uye.odunc_limit_al()})"
            )

    def _aktif_odunc_bul(self, uye_id, isbn):
        """Üyeye ait aktif ödünç kaydını bulur."""
        for odunc in self.__oduncler.values():
            if (
                odunc.aktif
                and odunc.uye_id == str(uye_id)
                and odunc.isbn == str(isbn)
            ):
                return odunc
        raise ValueError(
            f"Aktif ödünç kaydı bulunamadı: Üye={uye_id}, ISBN={isbn}"
        )

    def _odunc_kaydi_olustur(self, uye_id, isbn):
        """Yeni ödünç kaydı oluşturur."""
        bugun = datetime.now().strftime(TARIH_FORMATI)
        odunc_id = self._yeni_id_uret()
        return Odunc(odunc_id, uye_id, isbn, bugun)

    def _yeni_id_uret(self):
        """Benzersiz ödünç ID'si üretir."""
        mevcut_sayilar = [
            int(oid.replace(ODUNC_ID_ONEKI, ""))
            for oid in self.__oduncler
            if oid.startswith(ODUNC_ID_ONEKI)
            and oid[len(ODUNC_ID_ONEKI):].isdigit()
        ]
        sonraki = max(mevcut_sayilar, default=0) + 1
        return f"{ODUNC_ID_ONEKI}{sonraki:04d}"

    def _yukle(self):
        """Ödünç kayıtlarını JSON dosyasından yükler."""
        ham_veri = dosyadan_yukle(ODUNC_DOSYASI, self.__veri_dizini)
        self.__oduncler = {
            oid: Odunc.from_dict(veri)
            for oid, veri in ham_veri.items()
        }

    def _kaydet(self):
        """Ödünç kayıtlarını JSON dosyasına kaydeder."""
        kayit_verisi = {
            oid: o.to_dict()
            for oid, o in self.__oduncler.items()
        }
        dosyaya_kaydet(
            ODUNC_DOSYASI, kayit_verisi, self.__veri_dizini
        )
