import { HttpErrorResponse } from '@angular/common/http';
import { Component, EventEmitter, Input, OnChanges, OnDestroy, Output, inject, signal } from '@angular/core';
import type { Subscription } from 'rxjs';

import { isGuestResourceSuccessEnvelope } from '../../shared/models/guest-course.models';
import { GS06ResourcesService } from '../data-access/gs06-resources.service';
import type {
  GS06Resource,
  GS06ResourceScreenState,
} from '../models/gs06-resource-screen-state.model';
import { GS06ResourcePanel } from '../ui/gs06-resource-panel';

@Component({
  imports: [GS06ResourcePanel],
  selector: 'study-gs06-page',
  styleUrl: './gs06-page.css',
  templateUrl: './gs06-page.html',
})
export class GS06Page implements OnChanges, OnDestroy {
  @Input({ required: true }) courseId = '';
  private readonly data = inject(GS06ResourcesService);
  private request?: Subscription;

  readonly state = signal<GS06ResourceScreenState>({ status: 'loading' });

  ngOnChanges(): void {
    this.loadResources();
  }

  ngOnDestroy(): void {
    this.request?.unsubscribe();
  }

  loadResources(): void {
    const courseId = toSafeId(this.courseId);
    this.request?.unsubscribe();
    if (!courseId) {
      this.state.set({ status: 'invalid-course' });
      return;
    }

    this.state.set({ status: 'loading' });
    this.request = this.data.resources(courseId).subscribe({
      next: (response) => {
        const candidate: unknown = response;
        if (
          !isGuestResourceSuccessEnvelope(candidate) ||
          candidate.businessCode !== 'DESIGN_RESOURCE_RETRIEVED'
        ) {
          this.state.set({ status: 'error' });
          return;
        }
        const resources = parsePublicResources(candidate.data);
        if (!resources) {
          this.state.set({ status: 'error' });
          return;
        }
        this.state.set(
          resources.length ? { status: 'ready', resources } : { status: 'empty' },
        );
      },
      error: (error: unknown) =>
        this.state.set(
          error instanceof HttpErrorResponse && error.status === 404
            ? { status: 'invalid-course' }
            : { status: 'error' },
        ),
    });
  }
}

function toSafeId(value: unknown): string | null {
  if (typeof value !== 'string' || !/^\d+$/.test(value)) return null;
  try {
    const parsed = BigInt(value);
    return parsed > 0n && parsed <= 9_223_372_036_854_775_807n ? value : null;
  } catch {
    return null;
  }
}

function parsePublicResources(value: unknown): readonly GS06Resource[] | null {
  if (!Array.isArray(value)) return null;

  const resources: GS06Resource[] = [];
  const seenIds = new Set<number>();
  let previousId = 0;
  for (const item of value) {
    if (!isRecord(item)) return null;
    const id = item['id'];
    const name = item['name'];
    const type = item['type'];
    const url = item['url'];
    const visibility = item['visibility'];
    const lessonId = item['lesson_id'];

    if (
      !isPositiveSafeInteger(id) ||
      seenIds.has(id) ||
      id <= previousId ||
      typeof name !== 'string' ||
      !name.trim() ||
      typeof type !== 'string' ||
      !type.trim() ||
      typeof url !== 'string' ||
      !url.trim() ||
      visibility !== 'PUBLIC' ||
      (lessonId !== null && !isPositiveInteger(lessonId))
    ) {
      return null;
    }

    seenIds.add(id);
    previousId = id;
    resources.push({ id, name, type, url, visibility, lesson_id: lessonId });
  }

  return resources;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isPositiveSafeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isSafeInteger(value) && value > 0;
}

function isPositiveInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value > 0;
}
