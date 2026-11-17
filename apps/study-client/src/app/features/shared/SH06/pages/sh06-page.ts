import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-sh06-page',
  styleUrl: './sh06-page.css',
  templateUrl: './sh06-page.html',
})
export class SH06Page {}
