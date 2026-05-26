"""JSON tabanlı dosya okuma/yazma işlemleri."""

import json
import os

VARSAYILAN_VERI_DIZINI = "veri"
DOSYA_UZANTISI = ".json"


def _tam_yol_olustur(veri_dizini, dosya_adi):
    """Dosyanın tam yolunu oluşturur.

    Args:
        veri_dizini: Veri dizininin yolu
        dosya_adi: Dosya adı (uzantısız veya uzantılı)

    Returns:
        Tam dosya yolu string'i
    """
    if not dosya_adi.endswith(DOSYA_UZANTISI):
        dosya_adi = dosya_adi + DOSYA_UZANTISI
    return os.path.join(veri_dizini, dosya_adi)


def dizin_olustur(veri_dizini):
    """Veri dizinini oluşturur (yoksa).

    Args:
        veri_dizini: Oluşturulacak dizin yolu
    """
    if not os.path.exists(veri_dizini):
        os.makedirs(veri_dizini)


def dosyaya_kaydet(dosya_adi, veri, veri_dizini=None):
    """Veriyi JSON dosyasına kaydeder.

    Args:
        dosya_adi: Kaydedilecek dosya adı
        veri: Kaydedilecek veri (sözlük veya liste)
        veri_dizini: Veri dizini yolu (varsayılan: 'veri')
    """
    if veri_dizini is None:
        veri_dizini = VARSAYILAN_VERI_DIZINI
    dizin_olustur(veri_dizini)
    tam_yol = _tam_yol_olustur(veri_dizini, dosya_adi)
    with open(tam_yol, "w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, ensure_ascii=False, indent=2)


def dosyadan_yukle(dosya_adi, veri_dizini=None):
    """JSON dosyasından veri yükler.

    Args:
        dosya_adi: Yüklenecek dosya adı
        veri_dizini: Veri dizini yolu (varsayılan: 'veri')

    Returns:
        Yüklenen veri (sözlük veya liste); dosya yoksa boş sözlük
    """
    if veri_dizini is None:
        veri_dizini = VARSAYILAN_VERI_DIZINI
    tam_yol = _tam_yol_olustur(veri_dizini, dosya_adi)
    if not os.path.exists(tam_yol):
        return {}
    with open(tam_yol, "r", encoding="utf-8") as dosya:
        return json.load(dosya)


def dosya_sil(dosya_adi, veri_dizini=None):
    """JSON dosyasını siler (varsa).

    Args:
        dosya_adi: Silinecek dosya adı
        veri_dizini: Veri dizini yolu
    """
    if veri_dizini is None:
        veri_dizini = VARSAYILAN_VERI_DIZINI
    tam_yol = _tam_yol_olustur(veri_dizini, dosya_adi)
    if os.path.exists(tam_yol):
        os.remove(tam_yol)
