# Design and sources

The homepage retains its illustrated header, contact navigation, and closing.
Project cards are not displayed because the pinned repositories below the
profile already provide those entries.

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
Its snow palette follows the owner's website. Navigation illustrations are
original SVG artwork; the former globe and filmstrip are no longer displayed.

## Jerry illustration

The owner requested the actual mouse design from the existing AstraDraw welcome
artwork, rather than a new character in a similar palette. The illustrations were
edited with the built-in image generation tool, using that welcome artwork as
the edit target: retain its round face, large oval eyes, oversized pink ears,
creamy apricot fur, blue scarf, pencil and drawing pose. Jerry is a third-party
fictional character; this personal illustration
does not imply affiliation or grant rights to the character.

Final project assets: `assets/jerry-scarf.png` (white background) and
`assets/jerry-scarf-dark.png` (dark background). They are raster illustrations,
not editable vector characters. Profile text remains separately generated SVG
lettering with equivalent accessible text in the README image descriptions.

Final prompt specification (built-in edit mode, precise-object-edit): Extract
only the exact central mouse, its blue pencil, scarf, and sheet with three colored
squares from the AstraDraw welcome banner. Preserve its face, expression,
head-to-body proportions, colors, drawing pose and dark navy contours. Remove
the surrounding snowflake friend, video icon, chart, outside arrow and star.
Reframe compactly on white; no text, checkerboard, extra accessories, or character
redesign. The matching dark edit changes only the exterior background to
`#0D1117`, keeping the character and light paper unchanged.
Two light-blue SVG snowflakes sit around the mouse in the header, matching the
profile's existing snowflake motif without adding another large illustration.

## Fonts

Comic Neue Regular and Bold are by Craig Rozynski and Hrant Papazian. The fonts and SIL Open
Font License are preserved in `assets/fonts/`. It is also used in the owner's
[AstraDraw](https://github.com/IamJerryXu/AstraDraw) visual identity.

Trebuchet MS and Songti lettering are converted to outlines using locally
installed fonts; system font binaries are not distributed. `tools/build_profile.py`
is an optional artwork source and uses `fonttools`. `PROFILE_SYSTEM_FONTS` can
select the local system-font directory. The README works without running it.
