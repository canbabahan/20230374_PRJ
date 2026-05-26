"""Kitap CRUD işlemlerini yönetir."""

from models.kitap import Kitap
from utils.dogrulama import isbn_dogrula, KitapBulunamadiHatasi
from utils.dosya_isle import dosyaya_kaydet, dosyadan_yukle

KITAP_DOSYASI = "kitaplar"


class KitapService:
    """Kitap ekleme, silme, arama ve listeleme işlemlerini yönetir."""

    def __init__(self, veri_dizini=None):
        """KitapService nesnesini başlatır.

        Args:
            veri_dizini: Veri dosyalarının saklanacağı dizin
        """
        self.__veri_dizini = veri_dizini
        self.__kitaplar = {}
        self._yukle()

    def kitap_ekle(self, isbn, kitap_adi, yazar, yil):
        """Sisteme yeni kitap ekler.

        Args:
            isbn: Kitabın ISBN numarası
            kitap_adi: Kitabın adı
            yazar: Kitabın yazarı
            yil: Yayın yılı

        Raises:
            ValueError: ISBN zaten kayıtlı ise
        """
        temiz_isbn = isbn_dogrula(isbn)
        if temiz_isbn in self.__kitaplar:
            raise ValueError(
                f"ISBN {temiz_isbn} zaten kayıtlı"
            )
        kitap = Kitap(isbn, kitap_adi, yazar, yil)
        self.__kitaplar[temiz_isbn] = kitap
        self._kaydet()
        return kitap

    def kitap_sil(self, isbn):
        """Sistemden kitap siler.

        Args:
            isbn: Silinecek kitabın ISBN'i

        Raises:
            KitapBulunamadiHatasi: Kitap bulunamazsa
            ValueError: Kitap ödünçteyse
        """
        kitap = self.kitap_getir(isbn)
        if not kitap.musait:
            raise ValueError(
                f"Kitap ödünçte olduğu için silinemez: {isbn}"
            )
        del self.__kitaplar[isbn_dogrula(isbn)]
        self._kaydet()

    def kitap_getir(self, isbn):
        """ISBN ile kitap getirir.

        Args:
            isbn: Aranacak ISBN

        Returns:
            Kitap nesnesi

        Raises:
            KitapBulunamadiHatasi: Kitap bulunamazsa
        """
        temiz_isbn = isbn_dogrula(isbn)
        if temiz_isbn not in self.__kitaplar:
            raise KitapBulunamadiHatasi(
                f"Kitap bulunamadı: {temiz_isbn}"
            )
        return self.__kitaplar[temiz_isbn]

    def kitap_ara(self, arama_terimi):
        """Kitap adı veya yazar adına göre arama yapar.

        Args:
            arama_terimi: Aranacak metin

        Returns:
            Eşleşen Kitap nesnelerinin listesi
        """
        if not arama_terimi or not arama_terimi.strip():
            return list(self.__kitaplar.values())
        terim = arama_terimi.strip().lower()
        return [
            k for k in self.__kitaplar.values()
            if terim in k.kitap_adi.lower()
            or terim in k.yazar.lower()
        ]

    def tum_kitaplari_listele(self):
        """Tüm kitapları döndürür.

        Returns:
            Kitap nesnelerinin listesi
        """
        return list(self.__kitaplar.values())

    def musait_kitaplari_listele(self):
        """Müsait kitapları döndürür."""
        return [k for k in self.__kitaplar.values() if k.musait]

    def _yukle(self):
        """Kitapları JSON dosyasından yükler."""
        ham_veri = dosyadan_yukle(KITAP_DOSYASI, self.__veri_dizini)
        self.__kitaplar = {
            isbn: Kitap.from_dict(veri)
            for isbn, veri in ham_veri.items()
        }

    def _kaydet(self):
        """Kitapları JSON dosyasına kaydeder."""
        kayit_verisi = {
            isbn: k.to_dict()
            for isbn, k in self.__kitaplar.items()
        }
        dosyaya_kaydet(KITAP_DOSYASI, kayit_verisi, self.__veri_dizini)
