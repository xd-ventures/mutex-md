# MUTEX.md

The proposed MUTEX.md standard for coordination of autonomous coding agents through a shared text file.

The specification lives in **[mutex-md-spec.md](mutex-md-spec.md)**. Edit that file to update the standard.

- Formatted specification: https://mutex.md/
- Original Markdown: https://mutex.md/mutex-md-spec.md
- Discussion and proposals: https://github.com/xd-ventures/mutex-md/issues

## Publishing

Pull requests run the **Build specification** check. Merge a change into `main` to build and deploy the static website automatically through GitHub Actions and GitHub Pages. The Markdown is copied unchanged alongside the generated HTML. No deployment secrets are required.

GitHub Pages must use **GitHub Actions** as its publishing source. Its custom domain is `mutex.md`.

## Local preview

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements.txt
.venv/bin/python scripts/build.py
.venv/bin/python -m http.server 8000 --directory _site
```

Open http://localhost:8000/. Generated files in `_site/` are not committed.

## Domain setup

The registration stays at [register.domains](https://register.domains/). Cloudflare hosts DNS; GitHub Pages hosts the static files.

1. In the xd.ventures Cloudflare account, add `mutex.md` on the Free plan. Cloudflare assigns two nameservers to this specific zone.
2. At register.domains, open `mutex.md` and replace its nameservers with **both exact nameservers assigned by Cloudflare**. Nameservers from another Cloudflare zone must not be reused. Wait until the Cloudflare zone is active.
3. Configure these Cloudflare DNS records:

   | Type | Name | Content |
   | --- | --- | --- |
   | A | `@` | `185.199.108.153` |
   | A | `@` | `185.199.109.153` |
   | A | `@` | `185.199.110.153` |
   | A | `@` | `185.199.111.153` |
   | CNAME | `www` | `xd-ventures.github.io` |

   Initially use **DNS only** so GitHub can verify the domain and issue the origin HTTPS certificate. Use TTL Auto. No wildcard record is needed.
4. In [GitHub Pages settings](https://github.com/xd-ventures/mutex-md/settings/pages), confirm the custom domain is `mutex.md`. When the certificate is available, enable **Enforce HTTPS**.
5. Enable Cloudflare proxy on the above records and set Cloudflare SSL/TLS mode to **Full (strict)**. Enable **Always Use HTTPS**. The `www` hostname redirects to `mutex.md` through GitHub Pages.
6. Verify https://mutex.md/ and https://mutex.md/mutex-md-spec.md.

Official references: [GitHub Pages custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site), [Cloudflare nameserver setup](https://developers.cloudflare.com/dns/zone-setups/full-setup/setup/).
