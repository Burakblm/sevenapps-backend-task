# SevenApps Backend Task

## Proje Hakkında

Bu proje, PDF dokümanlarını işleyerek Google Gemini AI 1.5 Flash modeli aracılığıyla kullanıcıların bu dokümanlarla ilgili sorular sormasını ve yanıtlar almasını sağlayan bir backend uygulamasıdır. Projede üç adet mikroservis bulunmaktadır:

1. **Upload Servis**: PDF dokümanlarını Google Cloud Storage'a yükler ve benzersiz bir `pdf_id` üretir.
2. **Metadata Extraction Servis**: Yüklenen PDF dokümanlarının metaverilerini çıkarır ve veritabanına kaydeder.
3. **Chat Servis**: Kullanıcıların PDF dokümanları hakkında sorular sormasını sağlar ve Gemini AI 1.5 Flash modeli aracılığıyla yanıtlar üretir.

---

## Teknik Detaylar

### Upload Servis
- **Amaç**: Kullanıcıların `/v1/pdf` üzerinden PDF dokümanlarını Google Cloud Storage'a yüklemesini sağlar.
- **İşleyiş**:
  - PDF dokümanları Google Cloud Storage'a yüklenir.
  - Apache Kafka Producer aracılığıyla Metadata Extraction Servisi'ne `pdf_id` gönderilir.
  - PostgreSQL veritabanında `pdf_id`, `pdf_name` ve `document_status=pending` içeren bir kayıt oluşturulur.

### Metadata Extraction Servis
- **Amaç**: Yüklenen PDF dokümanlarının metaverilerini çıkarmak.
- **İşleyiş**:
  - Kafka Consumer olarak çalışır ve `pdf_id` bilgilerini alır.
  - Google Cloud Storage'dan ilgili PDF dokümanını indirir.
  - PDF dokümanının metnini, sayfa sayısını ve diğer önemli bilgileri çıkarır.
  - PostgreSQL veritabanında `document_status=completed` olarak güncellenir.

### Chat Servis
- **Amaç**: Kullanıcıların PDF dokümanları hakkında sorular sormasını sağlamak.
- **İşleyiş**:
  - PostgreSQL veritabanından ilgili `pdf_id` bilgilerini alır.
  - Gemini AI 1.5 Flash modeli kullanılarak PDF hakkında sorulan sorulara yanıt üretir.
  - Kullanıcıya yanıt döndürür.

---

## Kullanım

### 1. PDF Yükleme API'si (/v1/pdf)
Bu API, kullanıcıların PDF dokümanlarını yüklemesine olanak tanır. Doküman yüklendiğinde, sistem bu dokümana özel benzersiz bir `pdf_id` üretir ve döndürür.

#### Örnek İstek
Bir PDF dokümanını yüklemek için aşağıdaki komutu kullanabilirsiniz:

```bash
curl -X POST "http://localhost/v1/pdf/" -F "file=@/path/to/your/pdf/file.pdf"
```

#### Örnek Yanıt
```json
{
    "pdf_id": "75c47c5330974d909b707674a5a87978"
}
```
---

### 2. PDF ile Sohbet API'si (/v1/chat/{pdf_id})
Bu API, yüklü PDF dokümanlarıyla ilgili sorular sormayı ve yanıt almayı sağlar. Bunun için `/v1/pdf` API'sinden alınan `pdf_id` kullanılmalıdır.

#### Örnek İstek
Bir PDF dokümanına ilişkin soru sormak için aşağıdaki komutu kullanabilirsiniz:

```bash
curl -X POST "http://localhost/v1/chat/75c47c5330974d909b707674a5a87978" -H "Content-Type: application/json" -d '{"message": "Bu PDF ne ile ilgilidir?"}'
```

#### Örnek Yanıt
```json
{
    "response": "Bu PDF, yapay zeka ve doğal dil işleme konularını içermektedir."
}
```
---

## Kurulum ve Çalıştırma

### Gereksinimler
1. **Google Gemini API Anahtarı**:
   - Google AI Studio üzerinden "Get API Key" seçeneğiyle bir API anahtarı oluşturun.
   - Anahtarınızı `docker-compose.yml` dosyasındaki `GOOGLE_GENERATIVE_AI_API` alanına ekleyin.

2. **Google Cloud Storage**:
   - Bir Storage Bucket oluşturun.
   - IAM sekmesinden bir servis hesabı oluşturun ve "Google Storage Admin" yetkisi verin.
   - Servis hesabının anahtarını `credentials.json` olarak indirin.
   - Bu dosyayı projenin ana dizinine yerleştirin ve aşağıdaki komutları çalıştırarak gerekli dizinlere kopyalayın:

```bash
cp credentials.json upload/app/services/credentials.json
cp credentials.json metadata-extraction/app/services/credentials.json
```

### Çalıştırma
1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/Burakblm/sevenapps-python-backend-task-project.git
   cd sevenapps-python-backend-task-project
   ```

2. Docker konteynerlerini başlatın:
   ```bash
   sudo docker-compose -f docker-compose-dev.yml up --build -d
   ```

Bu işlem sonrası aşağıdaki servisler çalışır durumda olacaktır:

- **Traefik**: Farklı portlardaki API'lere tek bir URL üzerinden erişim sağlar.
- **PostgreSQL**: PDF metadatalarının tutulduğu veritabanı.
- **Zookeeper ve Kafka**: Servisler arasında iletişim için mesajlaşma altyapısını sağlar.
- **Upload Servis**: `/v1/pdf` API'sini sunar.
- **Metadata Extraction Servis**: PDF metaverilerini işler ve veritabanına kaydeder.
- **Chat Servis**: PDF hakkında sorulara yanıt üretir.

---

## Canlı Uygulama

Projeyi aşağıdaki bağlantılar üzerinden deneyebilirsiniz:

- **PDF Yükleme API'si**: [http://your_vm_ip_address/v1/pdf/](http://your_vm_ip_address/v1/pdf/)
- **Chat API'si**: [http://your_vm_ip_address/v1/chat/{pdf_id}](http://your_vm_ip_address/v1/chat/{pdf_id})

Not: Google Cloud Compute Engine üzerinde yayınlanmış olan proje şu anda durdurulmuş durumda. Kendi sunucunuzun IP adresi üzerinden erişim sağlayabilirsiniz.
.
---

