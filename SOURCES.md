# Design and sources

This is Yongxue Xu's GitHub profile. Biography, interests and contact links are
drawn from the owner's public [academic homepage](https://jerrysnow.me/).
Project descriptions link to the owner's public repositories. No private drafts,
reference libraries, or unpublished research assets are included.

## Layout references

Inspected on 2026-09-10:

- [Awesome GitHub Profile README](https://github.com/abhisheknaiidu/awesome-github-profile-readme): profile layout categories and examples.
- [DenverCoder1](https://github.com/DenverCoder1/DenverCoder1): separate identity, contact, and project navigation.
- [capsule-render](https://github.com/kyechan99/capsule-render): wide SVG headers and visual page boundaries.
- [sindresorhus](https://github.com/sindresorhus/sindresorhus): a personal visual signature rather than a conventional resume page.

No third-party template code, illustrations, or logos were copied from these
references. This profile does not depend on remote badge or statistics services.
Its snow palette follows the owner's website; the globe, filmstrip, stationery,
and navigation illustrations are original SVG artwork.

## Fonts

Comic Neue Bold is by Craig Rozynski and Hrant Papazian. The font and SIL Open
Font License are preserved in `assets/fonts/`. It is also used in the owner's
[AstraDraw](https://github.com/IamJerryXu/AstraDraw) visual identity.

Trebuchet MS and Songti lettering are converted to outlines using locally
installed fonts; system font binaries are not distributed. `tools/build_profile.py`
is an optional artwork source and uses `fonttools`. `PROFILE_SYSTEM_FONTS` can
select the local system-font directory. The README works without running it.
