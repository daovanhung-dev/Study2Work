import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class LocalStorageService {
  setItem<T>(key: string, value: T): void {
    const serializedValue = JSON.stringify(value);
    if (serializedValue === undefined) {
      throw new TypeError('The value cannot be serialized to JSON.');
    }

    localStorage.setItem(key, serializedValue);
  }

  getItem<T>(key: string): T | null {
    const serializedValue = localStorage.getItem(key);
    if (serializedValue === null) {
      return null;
    }

    return JSON.parse(serializedValue) as T;
  }
}
