import { Component } from "@angular/core";
import { RouterOutlet } from "@angular/router";

@Component({
  selector: "db-root",
  standalone: true,
  imports: [RouterOutlet],
  template: "<router-outlet />",
})
export class AppComponent {}
