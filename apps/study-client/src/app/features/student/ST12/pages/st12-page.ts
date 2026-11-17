import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

import { StudentApiService, type ResourceRecord } from '../../data/student-api.service';
import { StudentApiState } from '../../data/student-api-state';

@Component({
  selector: 'study-st12-page',
  styleUrls: ['./st12-page.css', '../../../../shared/ui/student-static-screen.css', '../../data/student-api-view.css'],
  templateUrl: './st12-page.html',
})
export class ST12Page implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly api = inject(StudentApiService);

  readonly resources = new StudentApiState<ResourceRecord[]>();
  readonly selectedResource = new StudentApiState<ResourceRecord>();
  lessonId = '';

  ngOnInit(): void {
    this.lessonId = this.route.snapshot.paramMap.get('lessonId') ?? '';
    if (this.lessonId) this.resources.load(this.api.getLessonResources(this.lessonId));
  }

  openResource(resource: ResourceRecord): void {
    this.selectedResource.load(this.api.getResource(String(resource.id)));
  }
}
