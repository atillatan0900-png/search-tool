# 🔍 DDGS Advanced File Search - v2.1.0

Güvenli, hızlı ve gelişmiş dosya arama aracı. Birden fazla dosya hosting platformunda eşzamanlı arama yapın.

**Turkish** | [English](#english) | [Deutsch](#deutsch) | [Français](#francais) | [Español](#espanol)

---

## ✨ Yeni Özellikler v2.1.0

- ⚡ **Async Search Engine** - Çok daha hızlı arama
- 🌍 **Multi-Language Support** - 5 dilde arayüz (TR, EN, DE, FR, ES)
- 💾 **Advanced Caching** - Sonuçları hızlı şekilde yeniden kullanın
- ⚙️ **YAML Config** - Kolay yapılandırma
- 🔐 **Geliştirilmiş Güvenlik** - Input validation ve rate limiting
- 📊 **Detaylı İstatistikler** - Database tabanlı istatistikler

---

## 📋 Özellikler

### Arama Yetenekleri
- 🌐 **7+ Platform** - Google Drive, Mega, Yandex, Dropbox, OneDrive, MediaFire, Solidfiles
- 📂 **Dosya Türü Araması** - Video, Müzik, E-kitap, Yazılım, Resim, Kod, Arşiv
- ⚡ **Paralel Arama** - 5 worker ile eşzamanlı platform taraması
- 💾 **Caching** - Arama sonuçlarını otomatik cache'le

### Link Yönetimi
- ✅ **Link Kontrolü** - Aktif/Bozuk durumunu kontrol et
- 📊 **Dosya Boyutu** - Her link için dosya boyutunu göster
- 🏷️ **Favori Yönetimi** - Beğendiğin linkleri kaydet
- 🔍 **Tam Metin Arama** - Veritabanında hızlı arama

### Dışa Aktarma
- 📄 **PDF Raporu** - Profesyonel PDF raporu
- 📊 **Excel Dosyası** - Düzenlenebilir Excel formatlı
- 📋 **CSV Dosyası** - Tüm uyumlu yazılımlarla açılabilir
- 🌐 **HTML Raporu** - Modern tasarımla web taramasında görüntüle
- 📦 **JSON Dosyası** - API entegrasyonları için
- 🎯 **QR Kodlar** - Linkleri QR kod olarak kaydet

### Güvenlik
- 🔒 **Input Validation** - Tüm girdiler doğrulanır
- 🛡️ **SQL Injection Koruması** - Parametrize sorgular
- 📝 **Logging** - Tüm işlemler log'lanır
- 🔑 **Rate Limiting** - API'ye aşırı yük mekanizması
- 🧹 **GDPR Uyumluluğu** - Otomatik eski veri temizleme

### Veritabanı
- 📊 **SQLite** - Veritabanında hızlı depolama
- 🔐 **Şifrelenmiş Yedekleme** - Verilerinizi güvenle saklayın
- ⚡ **WAL Modu** - Daha hızlı okuma/yazma
- 🗑️ **Otomatik Temizleme** - 30 günden eski aramaları sil

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- pip

### 1. Depo Klonla
```bash
git clone https://github.com/atillatan0900-png/search-tool.git
cd search-tool
```

### 2. Virtual Environment Oluştur
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 3. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 4. Konfigürasyonu Özelleştir (Opsiyonel)
```bash
cp config.yaml config.yaml.backup
nano config.yaml  # Ayarlarınızı değiştirin
```

---

## 💻 Kullanım

### Temel Başlangıç
```bash
python main.py
```

### Menü Seçenekleri

```
1. Basit arama         - Tüm platformlarda ara
2. Dosya türü araması  - Belirli dosya türünde ara
3. Gelişmiş arama      - Ekstra platformlar dahil
4. Linkleri kontrol et - Aktif/bozuk kontrol
5. Export et           - PDF, Excel, HTML vb.
6. İstatistikleri göster
7. Favorilere ekle
8. Privacy & Veri Kontrolü
9. Ayarlar
10. Çıkış
```

### Örnek Kullanımlar

**Örnek 1: Video Arama**
```
Seçim: 1
Ne aramak istersiniz? dune 2024
[*] 7 platform paralel taranıyor...
[✓] 45 link bulundu
```

**Örnek 2: Dosya Türüne Göre Arama**
```
Seçim: 2
Ne aramak istersiniz? python tutorial
Dosya türleri:
1. video
2. muzik
3. kitap
...
Dosya türü seç: 3
[✓] 23 e-kitap bulundu
```

**Örnek 3: Export İşlemi**
```
Seçim: 5
EXPORT SEÇENEKLERI
1. PDF Raporu
2. Excel Dosyası
...
7. Tümü
Seçim: 7
[✓] PDF oluşturuldu: export.pdf
[✓] Excel oluşturuldu: export.xlsx
...
```

---

## ⚙️ Konfigürasyon

### config.yaml Dosyası

```yaml
app:
  name: "DDGS Advanced File Search"
  version: "2.1.0"
  language: "tr"  # tr, en, de, fr, es

search:
  timeout: 10
  max_results: 100
  parallel_workers: 5
  cache_enabled: true
  cache_ttl: 3600

database:
  name: "linkler.db"
  auto_cleanup_days: 30
  backup_enabled: true

security:
  max_search_length: 200
  max_url_length: 2048
  allowed_export_formats: [pdf, excel, html, json, csv, m3u]
```

---

## 📊 Veritabanı Yapısı

### Tablolar

**linkler** - Bulunan tüm linkler
- url (benzersiz)
- platform (arandığı platform)
- arama_terimi
- tarih
- baslik
- durum (active/broken/timeout)
- dosya_boyutu
- hash_val (benzersiz kimlik)
- kategori

**aramalar** - Arama geçmişi
- terim
- tarih
- toplam_link
- platform_sayisi

**favoriler** - Kaydedilen favoriler
- url (benzersiz)
- eklenme_tarihi
- notlar

---

## 🔧 Modüller

### src/async_search.py
Asenkron arama motoru - daha hızlı sonuç

```python
from src.async_search import AsyncSearchEngine

async with AsyncSearchEngine() as engine:
    results = await engine.search_multiple_platforms(...)
```

### src/language_support.py
Çok dil desteği

```python
from src.language_support import language_manager

language_manager.set_language('en')
text = language_manager.get('app_name')
```

### src/cache_manager.py
Gelişmiş cache sistemi

```python
from src.cache_manager import cache

cache.set('my_key', value, ttl=3600)
result = cache.get('my_key')
stats = cache.get_stats()
```

### src/config_loader.py
YAML yapılandırması

```python
from src.config_loader import config

timeout = config.get('search.timeout')
config.set('search.max_results', 50)
config.save()
```

---

## 📈 İstatistikler

Veritabanında depolanan istatistikler:

```
Veritabanında:
  - Toplam link: 2.543
  - Toplam arama: 127
  - Favoriler: 45

Güncel Session:
  - Bulunan link: 89
  - Yapılan arama: 3
  - Favorilere alınan: 5

En çok sonuç veren platformlar:
  DRIVE       234 link
  MEGA        187 link
  YANDEX      145 link
```

---

## 🔐 Güvenlik Özellikleri

✅ **Input Validation**
- Arama terimleri maksimum uzunluk kontrolü
- SQL Injection koruması
- Tehlikeli karakterler filtreleme

✅ **URL Doğrulaması**
- Scheme kontrolü (http/https)
- Localhost/private IP engelleme
- Domain doğrulama

✅ **Dosya Yönetimi**
- Path traversal koruması
- Dosya adı sanitizasyonu
- Maksimum dosya boyutu kontrolü

✅ **Rate Limiting**
- 30 çağrı/60 saniye
- Otomatik bekleme mekanizması

---

## 📝 Logging

Log dosyası: `search_tool.log`

```
2026-06-07 10:30:45 - search_tool - INFO - Application started
2026-06-07 10:31:12 - search_tool - INFO - Database initialized successfully
2026-06-07 10:31:45 - search_tool - INFO - Cache SET: dune 2024 (TTL: 3600s)
```

---

## 🤝 Katkıda Bulun

Katkılarınızı bekliyoruz!

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📄 Lisans

MIT License - Detaylar için `LICENSE` dosyasına bakın

---

## 🐛 Sorun Bildir

[Issues](https://github.com/atillatan0900-png/search-tool/issues) sayfasında sorun bildirebilirsiniz.

---

## 📞 İletişim

- 👤 Author: [atillatan0900-png](https://github.com/atillatan0900-png)
- 📧 Email: atillatan0900@gmail.com

---

## 🎯 Yol Haritası

- [ ] Web arayüzü (Flask/Django)
- [ ] Mobile uygulama (React Native)
- [ ] Tor desteği
- [ ] Proxy rotasyonu
- [ ] Machine Learning ile link analizi
- [ ] Real-time sorgulama
- [ ] WebSocket desteği
- [ ] Docker container

---

<a id="english"></a>
# 🔍 DDGS Advanced File Search - v2.1.0

Secure, fast and advanced file search tool. Search simultaneously on multiple file hosting platforms.

[Full English documentation coming soon...]

---

<a id="deutsch"></a>
# 🔍 DDGS Advanced File Search - v2.1.0

Sicheres, schnelles und fortschrittliches Dateisuchewerkzeug.

[Vollständige deutsche Dokumentation folgt bald...]

---

<a id="francais"></a>
# 🔍 DDGS Advanced File Search - v2.1.0

Outil de recherche de fichiers sécurisé, rapide et avancé.

[Documentation française complète à venir...]

---

<a id="espanol"></a>
# 🔍 DDGS Advanced File Search - v2.1.0

Herramienta de búsqueda de archivos segura, rápida y avanzada.

[Documentación completa en español próximamente...]

---

**Made with ❤️ by atillatan0900-png**
