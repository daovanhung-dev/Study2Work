import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudentPublicFrame } from '../../../../shared/ui/student-public-frame';

@Component({
  imports: [RouterLink, StudentPublicFrame],
  selector: 'study-st07-page',
  templateUrl: './st07-page.html',
})
export class ST07Page {}
