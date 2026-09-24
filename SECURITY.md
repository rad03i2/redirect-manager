# Security Policy

## Scope
Redirect Manager parses local text files and emits redirect configuration. It does not make network requests or follow destinations.

## Reporting
Please report suspected vulnerabilities privately through GitHub's repository security reporting features when available. Do not include credentials, private production URLs, or other sensitive data in public issues.

## Safe use
- Treat redirect files as untrusted input and review generated configuration before deployment.
- Keep Python and your web server supported and patched.
- Do not place secrets in redirect source or target paths.
- Test generated snippets in a staging environment before production.

## السياسة الأمنية
تعمل الأداة محليًا ولا تزور الروابط. تعامل مع ملفات القواعد كمدخلات غير موثوقة، وراجع إعدادات الخادم الناتجة قبل نشرها. لا تنشر أسرارًا أو روابط خاصة في البلاغات العامة.
