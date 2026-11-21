# ST-02 models

The shared `StudentProfile` model mirrors the current API #04 `UserProfile`
projection. ST-02 renders only `full_name` and `email`; it does not expose
`role`/`status` as authorization state, or infer `bio`, permissions, avatar
rendering policy, or edit behavior.
