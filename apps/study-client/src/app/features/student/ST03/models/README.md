# ST-03 models

ST-03 reuses `StudentProfile` from the shared Student API models. Its data-access service defines
the source-backed #14 request shape (`full_name`, `phone`, `avatar_url`) and #13 upload result
(`avatar_url`). Do not add `bio` to either request: the current API/DB source does not persist it.
