import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

import { StudyIcon } from '../../../../shared/ui/study-icon';
import { AD24_SCREEN } from '../models/ad24-screen.model';

@Component({
  imports: [RouterLink, StudyIcon],
  selector: 'study-ad24-page',
  templateUrl: './ad24-page.html',
})
export class AD24Page {
  readonly definition = AD24_SCREEN;

  get filterActions() {
    return this.definition.actions?.slice(0, 3) ?? [];
  }

  get exportAction() {
    return this.definition.actions?.[3] ?? null;
  }
}
