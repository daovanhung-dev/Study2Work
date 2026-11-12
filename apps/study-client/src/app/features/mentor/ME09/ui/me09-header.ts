import { Component, Input } from '@angular/core';

@Component({
  selector: 'study-me09-header',
  styleUrl: './me09-header.css',
  templateUrl: './me09-header.html',
})
export class Me09Header {
  @Input() selectedCourseId: number | null = null;
}
