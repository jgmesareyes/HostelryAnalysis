import { Injectable }    from '@angular/core';


@Injectable()
export class ErrorService {
  errorLevel: string = 'error';

  setErrorLevel(errorLevel: string) {
  	this.errorLevel = errorLevel;
  }

  getErrorLevel() {
  	return this.errorLevel;
  }

}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/