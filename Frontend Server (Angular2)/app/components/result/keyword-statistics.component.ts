import { Component, Input }      from '@angular/core';

import { Statistics }      from '../../models/statistic/statistics';


@Component({
  moduleId: module.id,
  selector: 'keyword-statistics',
  templateUrl: './keyword-statistics.component.html',
  styleUrls: [ './keyword-statistics.component.css' ]
})
export class KeywordStatisticsComponent {
  @Input() wordStats: Statistics;
}


/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/