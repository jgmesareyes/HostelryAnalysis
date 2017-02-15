import { Component }          from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'my-app',
  template: `
    <h1>{{title}}</h1>
    <nav>
      <a routerLink="/setup" routerLinkActive="active">Setup</a>
      <a routerLink="/hotels" routerLinkActive="active">Hotels</a>
      <a routerLink="/times" routerLinkActive="active">Elapsed times</a>
      <a routerLink="/nlp" routerLinkActive="active">NLP Results</a>
    </nav>
    <router-outlet></router-outlet>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'Hostelry Analysis';
}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/