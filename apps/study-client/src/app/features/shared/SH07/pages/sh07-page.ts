import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { Sh07AvailabilityNotice } from '../ui/sh07-availability-notice';

@Component({
  imports: [RouterLink, StudyIcon, Sh07AvailabilityNotice],
  selector: 'study-sh07-page',
  styleUrl: './sh07-page.css',
  templateUrl: './sh07-page.html',
})
export class SH07Page {}
