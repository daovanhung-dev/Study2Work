import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  imports: [RouterLink],
  selector: 'study-st26-page',
  styleUrls: [
    '../../shared/ui/student-api-page.css',
    '../../shared/ui/student-api-community.css',
    './st26-page.css',
    './st26-visual.css',
    '../../../../shared/ui/student-static-screen.css',
  ],
  templateUrl: './st26-page.html',
})
export class ST26Page {}
