## Purpose • الهدف

**English**  
This script transforms the black (or near-black) text of chosen pages in a Qurʾān PDF into any color you pick.  
*Why?*  
1. **Verse-tracing practice** – Colored glyphs are faint enough to let students trace over the letters, strengthening handwriting and orthography.  
2. **Memorization aid** – Distinct hues create a visual anchor that helps the brain recall verse positions and patterns more easily.  
3. **Engaging study material** – Vibrant pages motivate learners, break the monotony of monochrome prints, and make recitation drills more enjoyable.  

**العربية**  
يُحوِّل هذا السكربت حبرَ الآيات الأسود (أو شبه الأسود) في صفحات محدَّدة من مصحف PDF إلى لون يختاره المستخدم.  
**لماذا؟**  
1. **تتبُّع الآيات** – يُصبح الخط الملون خفيفًا بحيثُ يمكن للطالب أن يخطَّ فوقه، فيتدرب على تحسين الكتابة وضبط الرسم العثماني.  
2. **تقوية الحفظ** – الألوان المختلفة تُكوِّن روابط بصرية تساعد الذاكرة على استرجاع مواضع الآيات وهيئاتها بسرعة أكبر.  
3. **تحفيز المتعلّم** – الصفحات الملوّنة تكسر رتابة الأبيض والأسود، فتجعل التلاوة والمراجعة أكثر تشويقًا ومتعة.
---

## How It Works 🔍✨

| Stage | What happens | Key Functions/Modules | Emoji-quick look |
|-------|--------------|-----------------------|------------------|
| 1️⃣ **Load & Check** | 🗂️ Reads your input PDF path and verifies the file exists. | `argparse`, `os.path.isfile` | 📂✅ |
| 2️⃣ **Page-to-Image** | 📑➜🖼️ Converts the chosen page range to high-resolution images using Poppler via **pdf2image**. | `convert_from_path` | 🖨️🖼️ |
| 3️⃣ **Detect Black Pixels** | 🎯 Creates a NumPy mask of every “almost-black” pixel (R,G,B < your `threshold`). | `numpy` 🧮 | 🕵️‍♀️⚫ |
| 4️⃣ **Re-Color** | 🎨 Swaps those black pixels for the color you picked (`--color 1..18`). | `replace_black_pixels_with_color()` | ✏️ |
| 5️⃣ **Progress Bar** | ⏳ Shows a live update so you know something’s happening! | `tqdm` | 📊🚀 |
| 6️⃣ **Save New PDF** | 💾 Merges the recolored images back into one sleek PDF. | `PIL.Image.save(..., save_all=True)` | 🗃️📥 |

---

## Why These Libraries? 🤔

- **pdf2image** 🖨️→🖼️ – Bridges Poppler & Python so we can “print” each PDF page as an image.  
- **Pillow (PIL)** 🖼️ – Lets us edit pixels & re-assemble images into a fresh PDF.  
- **NumPy** 🧮 – Lightning-fast math for masking millions of pixels.  
- **tqdm** 🚦 – Pretty progress bars keep you informed (and entertained).

---

## Command-Line Cheat-Sheet ⚡

```bash
python recolor.py \
  --input "D:/QURAN/quran_hafs_m.pdf" \
  --output "D:/QURAN/quran_hafs_colored.pdf" \
  --poppler-path "D:/poppler/bin" \
  --color 4 \            # 💛 Yellow
  --threshold 40 \       # How dark is “black”?
  --dpi 300 \            # Image sharpness
  --start-page 1 \
  --end-page 20



---

## كيف يعمل السكربت؟ 🔍✨

| المرحلة | ما الذي يحدث؟ | الدوال / المكتبات | نظرة سريعة بالرموز |
|---------|--------------|------------------|--------------------|
| 1️⃣ **التحميل والفحص** | 🗂️ يقرأ مسار ملف الـPDF ويتأكد من وجوده. | `argparse` و `os.path.isfile` | 📂✅ |
| 2️⃣ **تحويل الصفحات إلى صور** | 📑➜🖼️ يحوِّل الصفحات المحددة إلى صور عالية الدقة باستخدام Poppler عبر **pdf2image**. | `convert_from_path` | 🖨️🖼️ |
| 3️⃣ **اكتشاف البكسلات السوداء** | 🎯 ينشئ قناع NumPy لكل بكسل «شبه أسود» (R,G,B < قيمة `threshold`). | `numpy` 🧮 | 🕵️‍♀️⚫ |
| 4️⃣ **استبدال اللون** | 🎨 يبدّل تلك البكسلات باللون الذي اخترته (`--color 1..18`). | `replace_black_pixels_with_color()` | ✏️ |
| 5️⃣ **شريط التقدّم** | ⏳ يعرض تقدّمًا حيًّا لتعرف أن العمل جارٍ! | `tqdm` | 📊🚀 |
| 6️⃣ **حفظ ملف PDF الجديد** | 💾 يدمج الصور الملوَّنة في ملف PDF أنيق. | `PIL.Image.save(..., save_all=True)` | 🗃️📥 |

---

## لماذا هذه المكتبات؟ 🤔

- **pdf2image** 🖨️→🖼️ – حلقة وصل بين Poppler وPython لطباعة كل صفحة كصورة.  
- **Pillow (PIL)** 🖼️ – لتحرير البكسلات وإعادة تجميع الصور في PDF جديد.  
- **NumPy** 🧮 – رياضيات سريعة جدًا لفلترة ملايين البكسلات.  
- **tqdm** 🚦 – أشرطة تقدّم جميلة تُبقيك على اطّلاع.

---

## دليل الأوامر ⚡

```bash
python recolor.py \
  --input "D:/QURAN/quran_hafs_m.pdf" \
  --output "D:/QURAN/quran_hafs_colored.pdf" \
  --poppler-path "D:/poppler/bin" \
  --color 4 \            # 💛 أصفر
  --threshold 40 \       # ما مدى سواد «الأسود»؟
  --dpi 300 \            # وضوح الصورة
  --start-page 1 \
  --end-page 20

