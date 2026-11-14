import { HttpClient } from '@angular/common/http';
import type { HttpHeaders, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import {
  STUDY_API_BASE_PATH,
  type StudyApiDescriptor,
} from '../constant/api.constants';
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
    if (api.status === 'UNWIRED') {
      throw new Error(`Study API #${api.id} is marked UNWIRED and cannot be requested.`);
    }

    const path = resolveApiPath(api, options.pathParams);

    return this.http.request<ApiEnvelope<T>>(api.method, `${STUDY_API_BASE_PATH}${path}`, {
      body: options.body,
      headers: options.headers,
      params: options.params,
    });
  }

  /** Returns the HTTP status as well as the response envelope. */
  requestResponse<T>(api: StudyApiDescriptor, options: StudyApiRequestOptions = {}) {
    if (api.status === 'UNWIRED') {
      throw new Error(`Study API #${api.id} is marked UNWIRED and cannot be requested.`);
    }

    const path = resolveApiPath(api, options.pathParams);
    return this.http.request<ApiEnvelope<T>>(
      api.method,
      `${STUDY_API_BASE_PATH}${path}`,
      {
        body: options.body,
        headers: options.headers,
        params: options.params,
        observe: 'response',
      },
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
