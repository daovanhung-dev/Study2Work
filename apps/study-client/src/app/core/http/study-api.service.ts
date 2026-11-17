import { HttpClient } from '@angular/common/http';
import type { HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { STUDY_API_BASE_PATH, type StudyApiDescriptor } from '../constant/api.constants';
import type { ApiEnvelope } from './api-envelope';

export type { StudyApiMethod } from '../constant/api.constants';

export interface StudyApiRequestOptions {
  pathParams?: Readonly<Record<string, string | number>>;
  params?: HttpParams;
  body?: unknown;
  headers?: HttpHeaders;
}

@Injectable({ providedIn: 'root' })
export class StudyApiService {
  private readonly http = inject(HttpClient);

  /** Gửi request theo descriptor đã đăng ký và trả nguyên response envelope. */
  request<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions = {},
  ): Observable<ApiEnvelope<T>> {
    assertClientCallable(api);

    const path = resolveApiPath(api, options.pathParams);

    return this.http.request<ApiEnvelope<T>>(api.method, `${STUDY_API_BASE_PATH}${path}`, {
      body: options.body,
      headers: options.headers,
      params: options.params,
    });
  }

  /** Gửi request theo descriptor và giữ HTTP status/header cùng response envelope. */
  requestWithResponse<T>(
    api: StudyApiDescriptor,
    options: StudyApiRequestOptions = {},
  ): Observable<HttpResponse<ApiEnvelope<T>>> {
    assertClientCallable(api);

    const path = resolveApiPath(api, options.pathParams);

    return this.http.request<ApiEnvelope<T>>(api.method, `${STUDY_API_BASE_PATH}${path}`, {
      body: options.body,
      headers: options.headers,
      params: options.params,
      observe: 'response',
    });
  }
}

function assertClientCallable(api: StudyApiDescriptor): void {
  if (api.status === 'UNWIRED' || (api.status === 'SOURCE_ONLY' && api.id !== 'R-X01')) {
    throw new Error(
      `Study API #${api.id} is marked ${api.status} and cannot be requested by a screen.`,
    );
  }
}

function resolveApiPath(
  api: StudyApiDescriptor,
  pathParams: StudyApiRequestOptions['pathParams'],
): string {
  return api.path.replace(/\{([^{}]+)\}/g, (_placeholder, name: string) => {
    const value = pathParams?.[name];
    if (value === undefined) {
      throw new Error(`Missing path parameter "${name}" for Study API #${api.id}.`);
    }

    return encodeURIComponent(String(value));
  });
}
