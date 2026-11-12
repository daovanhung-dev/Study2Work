import { HttpClient } from '@angular/common/http';
import type { HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import type { ApiEnvelope } from './api-envelope';

const API_BASE_PATH = '/api/v1';

export type StudyApiMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';

export interface StudyApiRequestOptions {
  method?: StudyApiMethod;
  params?: HttpParams;
  body?: unknown;
  headers?: HttpHeaders;
}

@Injectable({ providedIn: 'root' })
export class StudyApiService {
  private readonly http = inject(HttpClient);

  /** Gọi endpoint tương đối với /api/v1 và trả nguyên response envelope. */
  request<T>(path: string, options: StudyApiRequestOptions = {}): Observable<ApiEnvelope<T>> {
    const normalizedPath = path.replace(/^\/+/, '');

    return this.http.request<ApiEnvelope<T>>(
      options.method ?? 'GET',
      `${API_BASE_PATH}/${normalizedPath}`,
      {
        body: options.body,
        headers: options.headers,
        params: options.params,
      },
    );
  }
}
