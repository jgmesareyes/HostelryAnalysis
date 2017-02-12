import { Component, OnInit }      from '@angular/core';

import { ErrorService }      from '../../services/error/error.service';


@Component({
  moduleId: module.id,
  selector: 'error',
  templateUrl: './error.component.html',
  styleUrls: [ './error.component.css' ]
})
export class ErrorComponent implements OnInit {
  errorLevel: string;

  constructor(private errorService: ErrorService) {}

  ngOnInit() {
    this.setErrorLevel();
  }

  setErrorLevel() {
    this.errorLevel = this.errorService.getErrorLevel();
  }

}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/