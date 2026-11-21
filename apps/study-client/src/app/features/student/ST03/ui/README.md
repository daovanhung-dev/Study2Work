# ST-03 UI

`pages/st03-page.html` loads the Student profile, edits `full_name` and nullable `phone`, uploads a
PNG/JPEG/WebP avatar, and saves the supported fields. Bio remains disabled because #04/#14 do not
provide persistence for it. Loading, validation, upload, save and refresh errors use separate UI
states; `pages/st03-page.css` styles the screen.
