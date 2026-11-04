# Tim van Helsdingen

A small static links page for **timvanhelsdingen.com**, hosted as a TrueNAS Custom App.
Dark charcoal and green, using an updated version of the original logo and Poppins typography from the previous site.
No JavaScript, database, third-party requests, or analytics. Poppins is bundled locally
under the SIL Open Font License in `assets/OFL.txt`.

Edit links and copy directly in `index.html`. All styling is in that file.

## Preview

Run `python -m http.server 4173 --bind 127.0.0.1 --directory .` and open http://127.0.0.1:4173.

## TrueNAS deployment

1. Copy the checkout to a temporary build directory on the NAS, then build the small
   static image there: `docker build -t local/timvanhelsdingen-web:latest .`.
   The Dockerfile uses a pinned nginx base image already verified on the target NAS.
2. Generate the Compose document using the NAS LAN address:

   `python tools/render_compose.py --bind <NAS-LAN-IP> > compose.generated.json`

   Use UTF-8 output if your shell defaults to UTF-16. JSON is also valid YAML.
   The image contains the page, original logo, fonts and nginx configuration.
   The target NAS has Docker Compose 2.32.3.

3. In TrueNAS Apps, install a custom app named `timvanhelsdingen-web`, using the generated document.
   For updates, replace the existing custom app's YAML with a freshly generated document.
   There are no host directories or persistent volumes to manage. When updating,
   build a new uniquely tagged image and use `--image local/timvanhelsdingen-web:<tag>`.
4. Check `http://<NAS-LAN-IP>:30080/` and `/healthz`.
5. In the existing Cloudflare Tunnel, create public hostname routes for
   `timvanhelsdingen.com` and `www.timvanhelsdingen.com` with service
   `http://<NAS-LAN-IP>:30080`. Replace only the old website's conflicting A/AAAA/CNAME
   records as needed; preserve mail and verification records.
6. Verify both public HTTPS hostnames before cancelling the old hosting account.
   Save the old website's DNS values first so the cutover can be reversed.

The web process runs without root privileges, with a read-only filesystem and a small
temporary filesystem. Port 30080 is for the LAN and the existing tunnel; it does not
need router port forwarding. The TrueNAS management interface is separate.

The nginx base image is pinned in `Dockerfile`. Compose uses a locally built image,
with pulling disabled. Rebuilding the image from this repository restores the app
if Docker images are pruned or Apps storage is migrated to a clean installation.

## Asset sources

- Logo: `https://timvanhelsdingen.com/wp-content/uploads/2022/02/tvh_logo_1.png`
- Current logo: `assets/tvh-logo-developer.png`, edited with the built-in imagegen tool.
  Edit brief: retain Tim's name and green geometric identity; change the subtitle
  to `DEVELOPER / CG GENERALIST` and keep the upper-right shape continuous.
  The original `assets/tvh-logo.png` is retained.
- Poppins regular and semibold: Google Fonts, Poppins v24. Font license: `assets/OFL.txt`.
