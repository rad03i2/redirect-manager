# Redirect Manager

A local, dependency-free Python toolkit for validating, testing, and exporting path-based HTTP redirect rules. It catches duplicate sources, loops, invalid status codes, and malformed paths before deployment.

> Functional CLI + Python API with automated tests. No network access is required.

## English

### Overview & purpose
Redirect files often become fragile collections of rules. A duplicate source, accidental loop, or malformed path can break navigation and SEO. Redirect Manager provides one small, auditable tool for maintaining exact path redirects and compiling them into common server formats.

### Key features
- Load rules from CSV or JSON.
- Validate site paths and `301`, `302`, `307`, `308` status codes.
- Detect duplicate/conflicting sources, self-redirects, and cycles.
- Resolve redirect chains with a configurable hop limit.
- Export to Nginx, Apache `.htaccess`, or Netlify `_redirects` syntax.
- Human-readable or JSON validation reports.
- Local-only: no telemetry, API keys, runtime dependencies, or network requests.
- Python 3.10+ CLI and reusable API.

### Preview
```console
$ redirect-manager validate examples/redirects.csv
OK: 4 redirect rules validated; no errors found.
$ redirect-manager resolve examples/redirects.csv /old-docs
/old-docs -> /docs -> /documentation
```

### Requirements & installation
```bash
python -m pip install -e .
redirect-manager --version
```
Requires Python 3.10 or newer.

### Input formats
CSV requires `source,target,status` headers. JSON is an array of objects with the same keys; JSON status defaults to `301`. Sources and targets are exact site paths beginning with one `/`.

```csv
source,target,status
/old,/new,301
/docs,/documentation,308
```

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
Validation exits `0` when valid, `1` for rule errors, and `2` for input/usage failures. Export refuses invalid rule sets.

### Python API
```python
from redirect_manager import load_rules, validate_rules, resolve_chain
rules = load_rules("redirects.csv")
report = validate_rules(rules)
if report.ok:
    print(resolve_chain(rules, "/old"))
```

### Configuration
No environment variables are required. CLI options control input, output format, and chain length; therefore no `.env.example` is needed.

### Project structure
```text
src/redirect_manager/   package, validation, exporters, CLI
tests/                  unit and CLI tests
examples/               safe sample rules
.github/workflows/       cross-platform CI
```

### Testing
```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```
CI runs these checks plus CLI smoke tests on Linux, Windows, and macOS.

### Security & privacy
Redirect Manager never follows destinations or makes HTTP requests. Input is untrusted text, and exporters refuse invalid rule sets. Review generated server snippets before deployment because surrounding server configuration and precedence still matter. See [SECURITY.md](SECURITY.md).

### Limitations
- Exact site paths only; wildcard/regex rules and absolute URL sources/targets are intentionally unsupported.
- It does not crawl a site or verify destination existence.
- Nginx/Apache output is a snippet for inclusion in an appropriate server configuration.
- It does not model every hosting provider's rule precedence.

### Optional roadmap
Potential additions include explicit wildcard support, additional hosting exporters, and graph visualization. Current functionality does not depend on these.

### Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

### License
MIT License. See [LICENSE](LICENSE).

### Author
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)

---

## العربية

### نظرة عامة والهدف
**Redirect Manager** أداة Python محلية وخفيفة للتحقق من قواعد إعادة توجيه مسارات المواقع واختبارها وتصديرها. تساعد على اكتشاف المصدر المكرر أو المتعارض، والتحويل إلى المسار نفسه، وحلقات التحويل، وأكواد الحالة غير المدعومة قبل النشر.

### الميزات
- قراءة CSV وJSON.
- التحقق من المسارات وأكواد `301` و`302` و`307` و`308`.
- اكتشاف التكرار والتعارض والحلقات.
- تتبع سلسلة تحويل مع حد أقصى للقفزات.
- تصدير إلى Nginx وApache وNetlify.
- تقارير نصية أو JSON.
- محلي بالكامل: بلا شبكة أو telemetry أو مفاتيح API أو اعتماديات تشغيل خارجية.
- CLI وPython API على Python 3.10 فأحدث.

### التثبيت والمتطلبات
```bash
python -m pip install -e .
redirect-manager --version
```
يتطلب Python 3.10 أو أحدث.

### صيغة الإدخال
يحتاج CSV الأعمدة `source,target,status`، وJSON عبارة عن مصفوفة كائنات بالمفاتيح نفسها، مع `301` كحالة افتراضية في JSON. المصدر والهدف في الإصدار الحالي مساران دقيقان داخل الموقع ويبدآن بـ`/` واحدة.

### الاستخدام
```bash
redirect-manager validate examples/redirects.csv
redirect-manager validate redirects.json --json
redirect-manager resolve examples/redirects.csv /old-docs
redirect-manager export examples/redirects.csv --format netlify
```

### Python API
```python
from redirect_manager import load_rules, validate_rules
rules = load_rules("redirects.csv")
print(validate_rules(rules).ok)
```

### الإعداد وبنية المشروع
لا توجد متغيرات بيئة أو أسرار مطلوبة. المصدر في `src/redirect_manager/`، والاختبارات في `tests/`، والأمثلة في `examples/`، وCI في `.github/workflows/`.

### الاختبارات
```bash
python -m unittest discover -s tests -v
python -m compileall -q src tests
```
ويشغّل CI الاختبارات وفحوص CLI على Linux وWindows وmacOS.

### الأمان والخصوصية
الأداة لا تفتح الوجهات ولا ترسل طلبات HTTP. تعامل المدخلات كنص غير موثوق، وترفض التصدير عند فشل التحقق. راجع إعداد الخادم الناتج قبل النشر لأن الإعدادات المحيطة وترتيب القواعد قد يغيران السلوك. راجع [SECURITY.md](SECURITY.md).

### القيود
الإصدار الحالي مخصص للمسارات الدقيقة فقط؛ لا يدعم wildcard أو regex أو الروابط المطلقة، ولا يفحص وجود الصفحة الهدف عبر الإنترنت، ولا يحاكي جميع قواعد الأولوية الخاصة بكل مزود استضافة. مخرجات Nginx وApache هي snippets للدمج في إعداد خادم مناسب.

### التطوير المستقبلي الاختياري
يمكن مستقبلًا إضافة wildcard بشكل صريح، ومصدّرات لمنصات إضافية، وعرض رسومي للسلاسل.

### المساهمة
راجع [CONTRIBUTING.md](CONTRIBUTING.md).

### الترخيص
MIT، راجع [LICENSE](LICENSE).

### المؤلف
**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: [@rad03i2](https://github.com/rad03i2)
