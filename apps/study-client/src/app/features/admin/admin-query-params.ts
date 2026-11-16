import { HttpParams } from '@angular/common/http';

export function adminQueryParams(
  values: Readonly<Record<string, string | number | null | undefined>>,
): HttpParams {
  let params = new HttpParams();
  for (const [key, value] of Object.entries(values)) {
    if (value !== undefined && value !== null && value !== '') {
      params = params.set(key, String(value));
    }
  }
  return params;
}
