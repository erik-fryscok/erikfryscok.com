# Home Hero Portrait — Design

Related work: [GitHub issue #33](https://github.com/erik-fryscok/erikfryscok.com/issues/33)

## Goal

Add Erik's supplied portrait to the Home page hero so first-time visitors see a human presence alongside the site's professional positioning.

## Placement decision

Use the portrait on the Home page rather than the Contact page. The Home hero gives the image immediate value by humanizing the first impression and balancing the existing text-heavy opening. The Contact page remains focused on outreach methods, and the image will not be duplicated across pages.

## Visual design

- Keep the existing headline and supporting copy unchanged.
- Display the portrait as a 256px square with rounded corners and a subtle shadow.
- At widths of 768px and above, use a two-column hero with flexible copy on the left and the fixed-width portrait on the right.
- Below 768px, stack the portrait below the copy and center it, with a maximum width of 256px.
- Preserve the existing Home page spacing and all sections following the hero.

## Asset and accessibility design

- Store the supplied 1024×1024 JPEG in `src/assets/` as `erik-fryscok-portrait.jpg` so Astro manages it as a source asset.
- Render it with Astro's `Image` component as a 512×512 WebP. CSS limits the displayed size to 256px, providing enough resolution for high-density screens while reducing transfer size from the source JPEG.
- Use the alternative text: “Erik Fryscok smiling outdoors with a city street in the background.”
- Mark the above-the-fold image for eager loading and high fetch priority.

## Validation

- A Node integration test builds the real Astro site and verifies that the rendered Home page contains the optimized portrait with the approved alternative text.
- `npm run check` and `npm run build` complete without diagnostics.
- Browser inspection at 375px confirms the stacked layout has no horizontal overflow.
- Browser inspection at 1280px confirms the two-column layout and balanced hero hierarchy.

## Documentation impact

- Record the Home-page placement choice in the decision log so the Home-versus-Contact question does not need to be revisited.
- Add the user-visible portrait treatment to `CHANGELOG.md` under Unreleased.
- Link the implementation plan from `docs/README.md`.

## Out of scope

- Adding the portrait to Contact or About.
- Editing, retouching, or generating variants of the supplied image.
- Changing Home page copy, global layout width, navigation, or downstream sections.
