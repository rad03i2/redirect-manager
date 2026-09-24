# Redirect Manager

A local, dependency-free Python toolkit for validating, testing, and exporting HTTP redirect rules. It helps teams catch duplicate sources, redirect loops, invalid status codes, and unsafe targets before deployment.

> **Status:** functional CLI + Python API with automated tests. No network access is required.

## English

### Why this project exists
Redirect files often grow into fragile collections of rules. A duplicate source, accidental loop, or malformed destination can break navigation or SEO. Redirect Manager provides one small, auditable tool for maintaining redirect rules and compiling them into common server formats.

### Key features
- Load redirect rules from CSV or JSON.
- Validate paths/URLs and HTTP redirect codes (`301`, `302`, `307`, `308`).
- Detect duplicate/conflicting sources and redirect cycles.
- Resolve a source through a redirect chain with a configurable hop limit.
- Export validated rules to Nginx, Apache `.htaccess`, or Netlify `_redirects` syntax.
- Human-readable and JSON validation reports.
- Local-only operation: no telemetry, API keys, or network requests.
- Cross-platform Python 3.10+ CLI and reusable API.

### Preview
```console
$ redirect-manager validate examples/redirects.csv
OK: 4 redirect rules validated; no errors found.

$ redirect-manager resolve examples/redirects.csv /old-docs
/old-docs -> /docs -> /documentation

$ redirect-manager export examples/redirects.csv --format netlify
/old-docs /docs 301
/docs /documentation 301
```

### Requirements & installation
Requires Python 3.10 or newer.

```bash
python -m pip install -e .
redirect-manager --version
```

For development:
```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

### Input formats
CSV must contain `source,target,status` headers. JSON must be an array of objects with the same keys. `status` defaults to `301` when omitted in JSON.

```csv
source,target,status
/old,/new,301
/docs,/documentation,308
```

Sources may be site paths beginning with `/` or absolute `http(s)` URLs. Targets may additionally be relative site paths. Control characters are rejected. Fragment-only targets and unsupported schemes are rejected.

### Usage
```bash
redirect-manager validate redirects.csv
redirect-manager validate redirects.json --json
redirect-manager resolve redirects.csv /old --max-hops 20
redirect-manager export redirects.csv --format nginx --output redirects.conf
redirect-manager export redirects.csv --format apache
redirect-manager export redirects.csv --format netlify
python -m redirect_manager validate redirects.csv
```

Validation exits with code `0` when valid, `1` when rule errors are found, and `2` for input/usage failures. Export refuses invalid rule sets.

### Python API
```python
from redirect_manager import load_rules, validate_rules, resolve_chain

rules = load_rules("redirects.csv")
report = validate_rules(rules)
if report.ok:
    print(resolve_chain(rules, "/old"))
```

### Configuration
No environment variables are required. CLI options control input, output format, and maximum chain length. There is intentionally no `.env` file.

### Project structure
```text
src/redirect_manager/   package, validation, exporters, CLI
tests/                  unit and CLI tests
examples/               safe sample redirect rules
.github/workflows/       CI
```

### Testing
Run `python -m unittest discover -s tests -v`. CI also compiles the package and runs CLI smoke tests on Linux, Windows, and macOS.

### Security & privacy
Redirect Manager never follows URLs or makes HTTP requests. Input is treated as untrusted text. Exporters reject invalid rules before producing configuration. Review generated server configuration before deployment; server-specific precedence and surrounding configuration still matter. See [SECURITY.md](SECURITY.md).

### Limitations
- It validates exact redirect sources; wildcard/regex redirect semantics are intentionally unsupported.
- It does not crawl a website or verify whether destinations exist.
- Generated Nginx/Apache snippets are intended to be included in an appropriate existing server configuration.
- URL normalization is deliberately conservative; semantically equivalent URLs can remain distinct.

### Optional roadmap
Possible future additions include wildcard-rule support behind an explicit mode, importers for additional hosting platforms, and graph visualization. These are not required for current functionality.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Keep changes focused, tested, dependency-light, and backward compatible where practical.

### License
MIT License. See [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)

---

## العربية

### نظرة عامة
**Redirect Manager** أداة Python محلية وخفيفة لإدارة قواعد إعادة توجيه HTTP والتحقق منها واختبار سلاسلها وتصديرها إلى صيغ خوادم شائعة. الهدف هو اكتشاف الأخطاء قبل نشر القواعد على الموقع.

### لماذا يوجد المشروع؟
ملفات إعادة التوجيه تكبر مع الوقت وقد تحتوي مصدرًا مكررًا أو حلقة تحويل أو وجهة غير صالحة، مما يسبب مشاكل للمستخدمين ومحركات البحث. يوفر المشروع فحصًا واضحًا وقابلًا للأتمتة دون الاعتماد على خدمات خارجية.

### الميزات
- قراءة القواعد من CSV أو JSON.
- التحقق من المسارات والروابط وأكواد `301` و`302` و`307` و`308`.
- اكتشاف المصادر المكررة والمتعارضة وحلقات إعادة التوجيه.
- تتبع سلسلة تحويل من مصدر معين مع حد أقصى للقفزات.
- تصدير إلى Nginx وApache `.htaccess` وNetlify `_redirects`.
- تقارير نصية أو JSON.
- عمل محلي بالكامل بلا اتصال شبكي أو مفاتيح API أو تتبع.
- CLI وPython API على Python 3.10 فأحدث.

### التثبيت
```bash
python -m pip install -e .
redirect-manager --version
```

### الاستخدام
```bash
redirect-manager validate examples/redirects.csv
redirect-manager validate redirects.json --json
redirect-manager resolve examples/redirects.csv /old-docs
redirect-manager export examples/redirects.csv --format netlify
```

يجب أن يحتوي CSV على الأعمدة `source,target,status`، أما JSON فهو مصفوفة كائنات بالمفاتيح نفسها. القيمة الافتراضية للحالة في JSON هي `301`.

### Python API
```python
from redirect_manager import load_rules, validate_rules
rules = load_rules("redirects.csv")
print(validate_rules(rules).ok)
```

### الإعداد
لا يحتاج المشروع متغيرات بيئة أو أسرارًا. جميع الخيارات تمر عبر CLI أو API.

### بنية المشروع
المصدر داخل `src/redirect_manager/`، والاختبارات داخل `tests/`، والأمثلة داخل `examples/`، وCI داخل `.github/workflows/`.

### الاختبارات
```bash
python -m unittest discover -s tests -v
```
ويشغّل CI أيضًا فحص compilation واختبارات CLI على Linux وWindows وmacOS.

### الأمان والخصوصية
الأداة لا تفتح الروابط ولا ترسل طلبات HTTP. المدخلات تعامل كنص غير موثوق، ولا يتم التصدير عند وجود أخطاء تحقق. يجب مراجعة إعداد الخادم الناتج قبل النشر لأن ترتيب قواعد الخادم وإعداداته المحيطة قد يغيران السلوك. راجع [SECURITY.md](SECURITY.md).

### القيود
لا يدعم الإصدار الحالي wildcard أو regex redirects، ولا يفحص وجود الصفحة الهدف عبر الإنترنت، كما أن تطبيع الروابط متحفظ عمدًا. ملفات Nginx وApache الناتجة عبارة عن snippets يجب دمجها في إعداد خادم مناسب.

### التطوير المستقبلي الاختياري
يمكن مستقبلًا إضافة وضع صريح لقواعد wildcard، ومستوردات لمنصات إضافية، وعرض رسومي لسلاسل التحويل.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md). يفضل إبقاء التغييرات مركزة ومختبرة وقليلة الاعتماديات.

### الترخيص
المشروع مرخص بترخيص MIT. راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)
